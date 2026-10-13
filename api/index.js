/* ============================================================================
   API VOOMNET Track — une seule fonction serverless (Vercel) qui route tout.
   Chaque route vérifie elle-même la session ET le rôle : le navigateur ne
   décide jamais de ses droits.
   ============================================================================ */
"use strict";
const { query, avecTransaction } = require("./_lib/db");
const {
  hacherMotDePasse, verifierMotDePasse, creerSession, sessionDepuisRequete,
  fermerSession, purgerSessionsExpirees, journaliser, ipDe,
  essaisBloques, noterEchec, reinitialiserEssais, MAX_ESSAIS
} = require("./_lib/auth");
const { ok, erreur, lireCorps, texte, nombre, booleen, dateISO } = require("./_lib/http");

/* ------------------------------- Helpers --------------------------------- */
function cheminEtQuery(req) {
  const url = new URL(req.url, "http://x");
  let chemin = url.pathname.replace(/^\/api/, "");
  if (!chemin.startsWith("/")) chemin = "/" + chemin;
  return { chemin: chemin.replace(/\/+$/, "") || "/", q: url.searchParams };
}

async function exigerSession(req, res) {
  const s = await sessionDepuisRequete(req);
  if (!s) { erreur(res, 401, "Session invalide ou expirée. Reconnectez-vous.", "NON_AUTHENTIFIE"); return null; }
  return s;
}
async function exigerAdmin(req, res) {
  const s = await exigerSession(req, res);
  if (!s) return null;
  if (!s.compte.admin) { erreur(res, 403, "Action réservée à l'administrateur.", "ROLE_INSUFFISANT"); return null; }
  return s;
}

/* --------------------- Conversion lignes SQL → app ----------------------- */
const LIGNE_DEPLACEMENT = r => ({
  id: r.id, date: r.date instanceof Date ? r.date.toISOString().slice(0, 10) : String(r.date).slice(0, 10),
  service: r.service_id, agent: r.agent, motif: r.motif || "",
  from: r.origine || "", to: r.destination || "",
  transport: r.transport || "", vehicule: r.vehicule || "",
  km: r.km === null ? "" : r.km, montant: r.montant === null ? 0 : Number(r.montant),
  statut: r.statut || "A_REGLE", justif: r.justif || "NON", note: r.note || "",
  created: r.cree_le ? r.cree_le.toISOString() : undefined,
  updated: r.maj_le ? r.maj_le.toISOString() : undefined
});
const LIGNE_COLLABORATEUR = r => ({ id: r.id, nom: r.nom, service: r.service_id, actif: !!r.actif,
  email: r.email || "", telephone: r.telephone || "" });
const LIGNE_VEHICULE = r => ({ id: r.id, plate: r.plaque, marque: r.marque, modele: r.modele, type: r.type,
  annee: r.annee, km: r.km, service: r.service_id, state: r.etat, entretien: r.entretien,
  note: r.note || "" });
const LIGNE_COMPTE_PUBLIC = r => ({ id: r.id, login: r.identifiant, label: r.nom, role: r.role,
  admin: !!r.admin, actif: !!r.actif, derniereConnexion: r.derniere_connexion_le ? r.derniere_connexion_le.toISOString() : null });

/* ================================ ROUTES ================================= */
async function route(req, res) {
  const { chemin, q } = cheminEtQuery(req);
  const methode = req.method.toUpperCase();

  /* --- Santé (publique, sans données sensibles) --- */
  if (chemin === "/health" && methode === "GET") {
    try {
      const { rows } = await query("SELECT now() AS maintenant, current_database() AS base");
      return ok(res, { ok: true, base: "connectee", base_nom: rows[0].base, heure: rows[0].maintenant, version: "3.11.0" });
    } catch (e) {
      return erreur(res, 503, "Base de données injoignable : " + (e.message || e.code), "BASE_INJOIGNABLE");
    }
  }

  /* --- Connexion --- */
  if (chemin === "/auth/login" && methode === "POST") {
    const corps = await lireCorps(req);
    if (!corps) return erreur(res, 400, "Requête illisible.", "CORPS_INVALIDE");
    const identifiant = (texte(corps.identifiant, 120) || "").toLowerCase();
    const motDePasse = String(corps.motDePasse || "");
    if (!identifiant || !motDePasse) return erreur(res, 400, "Identifiant et mot de passe requis.", "CHAMPS_MANQUANTS");

    const cle = ipDe(req) + "|" + identifiant;
    if (essaisBloques(cle) >= MAX_ESSAIS) {
      await journaliser(null, "connexion_bloquee", identifiant, { raison: "trop de tentatives" }, req);
      return erreur(res, 429, "Trop de tentatives. Réessayez dans quelques minutes.", "TROP_DE_TENTATIVES");
    }

    const { rows } = await query(`SELECT * FROM comptes WHERE lower(identifiant) = $1`, [identifiant]);
    const compte = rows[0];
    const valide = compte && compte.actif && verifierMotDePasse(motDePasse, compte.mot_de_passe_hash);
    if (!valide) {
      noterEchec(cle);
      await journaliser(null, "connexion_refusee", identifiant, null, req);
      return erreur(res, 401, "Identifiant ou mot de passe incorrect.", "IDENTIFIANTS_INVALIDES");
    }
    reinitialiserEssais(cle);
    const { jeton, expire } = await creerSession(compte, req);
    await journaliser({ login: compte.identifiant }, "connexion", compte.identifiant,
      { role: compte.role, admin: !!compte.admin }, req);
    purgerSessionsExpirees();
    return ok(res, { jeton, expireLe: expire, profil: LIGNE_COMPTE_PUBLIC(compte) });
  }

  /* --- Session courante --- */
  if (chemin === "/auth/session" && methode === "GET") {
    const s = await exigerSession(req, res); if (!s) return;
    return ok(res, { profil: s.compte, expireLe: s.expireLe });
  }

  /* --- Déconnexion --- */
  if (chemin === "/auth/logout" && methode === "POST") {
    const s = await sessionDepuisRequete(req);
    await fermerSession(req);
    if (s) await journaliser(s.compte, "deconnexion", s.compte.login, null, req);
    return ok(res, { ok: true });
  }

  /* --- État complet (lecture) --- */
  if (chemin === "/state" && methode === "GET") {
    const s = await exigerSession(req, res); if (!s) return;
    const [services, collabs, vehicules, deplacements, params, comptes, transports] = await Promise.all([
      query(`SELECT * FROM services ORDER BY ordre, id`),
      query(`SELECT * FROM collaborateurs ORDER BY nom`),
      query(`SELECT * FROM vehicules ORDER BY plaque`),
      query(`SELECT * FROM deplacements WHERE supprime_le IS NULL ORDER BY date DESC, cree_le DESC`),
      query(`SELECT cle, valeur FROM parametres`),
      query(`SELECT * FROM comptes ORDER BY role, identifiant`),
      query(`SELECT * FROM transports ORDER BY ordre, libelle`)
    ]);
    const parametres = {}; params.rows.forEach(r => { parametres[r.cle] = r.valeur; });
    return ok(res, {
      services: services.rows.map(r => ({ id: r.id, code: r.code, name: r.nom, short: r.libelle_court,
        role: r.role, color: r.couleur, color2: r.couleur2, logo: r.logo, icon: r.icone })),
      collaborateurs: collabs.rows.map(LIGNE_COLLABORATEUR),
      vehicules: vehicules.rows.map(LIGNE_VEHICULE),
      deplacements: deplacements.rows.map(LIGNE_DEPLACEMENT),
      transports: transports.rows.map(r => r.libelle),
      parametres,
      comptes: comptes.rows.map(LIGNE_COMPTE_PUBLIC)
    });
  }

  /* --- Déplacements --- */
  if (chemin === "/deplacements" && methode === "POST") {
    const s = await exigerSession(req, res); if (!s) return;
    const c = await lireCorps(req); if (!c) return erreur(res, 400, "Requête illisible.", "CORPS_INVALIDE");
    const id = texte(c.id, 40) || ("D" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6));
    const d = dateISO(c.date) || new Date().toISOString().slice(0, 10);
    const { rows } = await query(
      `INSERT INTO deplacements (id, date, service_id, agent, motif, origine, destination, transport, vehicule, km, montant, statut, justif, note, cree_par)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15)
       ON CONFLICT (id) DO UPDATE SET
         date=EXCLUDED.date, service_id=EXCLUDED.service_id, agent=EXCLUDED.agent, motif=EXCLUDED.motif,
         origine=EXCLUDED.origine, destination=EXCLUDED.destination, transport=EXCLUDED.transport,
         vehicule=EXCLUDED.vehicule, km=EXCLUDED.km, montant=EXCLUDED.montant, statut=EXCLUDED.statut,
         justif=EXCLUDED.justif, note=EXCLUDED.note, maj_le=now(), supprime_le=NULL
       RETURNING *`,
      [id, d, texte(c.service, 40), texte(c.agent, 120), texte(c.motif, 200), texte(c.from, 120),
       texte(c.to, 120), texte(c.transport, 120), texte(c.vehicule, 120), nombre(c.km),
       nombre(c.montant) || 0, texte(c.statut, 20), texte(c.justif, 10), texte(c.note, 500), s.compte.login]
    );
    await journaliser(s.compte, "deplacement_ajout", id, { montant: rows[0].montant, service: rows[0].service_id }, req);
    return ok(res, { deplacement: LIGNE_DEPLACEMENT(rows[0]) });
  }

  const mDepl = chemin.match(/^\/deplacements\/([^/]+)$/);
  if (mDepl) {
    const s = await exigerSession(req, res); if (!s) return;
    const id = decodeURIComponent(mDepl[1]);
    if (methode === "PATCH" || methode === "PUT") {
      const c = await lireCorps(req); if (!c) return erreur(res, 400, "Requête illisible.", "CORPS_INVALIDE");
      const champs = {
        date: dateISO(c.date), service_id: texte(c.service, 40), agent: texte(c.agent, 120),
        motif: texte(c.motif, 200), origine: texte(c.from, 120), destination: texte(c.to, 120),
        transport: texte(c.transport, 120), vehicule: texte(c.vehicule, 120), km: nombre(c.km),
        montant: nombre(c.montant), statut: texte(c.statut, 20), justif: texte(c.justif, 10), note: texte(c.note, 500)
      };
      const sets = [], vals = [];
      let i = 1;
      for (const k in champs) { if (champs[k] !== null) { sets.push(k + " = $" + i++); vals.push(champs[k]); } }
      if (!sets.length) return erreur(res, 400, "Aucune donnée à mettre à jour.", "RIEN_A_MODIFIER");
      vals.push(id);
      const { rows } = await query(`UPDATE deplacements SET ${sets.join(", ")}, maj_le=now() WHERE id = $${i} RETURNING *`, vals);
      if (!rows[0]) return erreur(res, 404, "Déplacement introuvable.", "INTROUVABLE");
      await journaliser(s.compte, "deplacement_modif", id, { champs: Object.keys(champs).filter(k => champs[k] !== null) }, req);
      return ok(res, { deplacement: LIGNE_DEPLACEMENT(rows[0]) });
    }
    if (methode === "DELETE") {
      /* suppression douce : la donnée reste récupérable, rien n'est détruit */
      const { rows } = await query(`UPDATE deplacements SET supprime_le = now(), maj_le = now() WHERE id = $1 RETURNING id`, [id]);
      if (!rows[0]) return erreur(res, 404, "Déplacement introuvable.", "INTROUVABLE");
      await journaliser(s.compte, "deplacement_suppression", id, null, req);
      return ok(res, { ok: true, id });
    }
  }

  /* --- Collaborateurs --- */
  if (chemin === "/collaborateurs" && methode === "POST") {
    const s = await exigerSession(req, res); if (!s) return;
    const c = await lireCorps(req); if (!c) return erreur(res, 400, "Requête illisible.", "CORPS_INVALIDE");
    const nom = texte(c.nom, 120);
    if (!nom) return erreur(res, 400, "Le nom est obligatoire.", "CHAMP_MANQUANT");
    const id = texte(c.id, 40) || ("C" + Date.now().toString(36));
    const { rows } = await query(
      `INSERT INTO collaborateurs (id, nom, service_id, actif, email, telephone)
       VALUES ($1,$2,$3,$4,$5,$6)
       ON CONFLICT (id) DO UPDATE SET nom=EXCLUDED.nom, service_id=EXCLUDED.service_id,
         actif=EXCLUDED.actif, email=EXCLUDED.email, telephone=EXCLUDED.telephone, maj_le=now()
       RETURNING *`,
      [id, nom, texte(c.service, 40), c.actif === undefined ? true : booleen(c.actif), texte(c.email, 160), texte(c.telephone, 40)]
    );
    await journaliser(s.compte, "collaborateur_ajout", id, { nom }, req);
    return ok(res, { collaborateur: LIGNE_COLLABORATEUR(rows[0]) });
  }
  const mCollab = chemin.match(/^\/collaborateurs\/([^/]+)$/);
  if (mCollab) {
    const s = await exigerSession(req, res); if (!s) return;
    const id = decodeURIComponent(mCollab[1]);
    if (methode === "PATCH" || methode === "PUT") {
      const c = await lireCorps(req); if (!c) return erreur(res, 400, "Requête illisible.", "CORPS_INVALIDE");
      const { rows } = await query(
        `UPDATE collaborateurs SET nom = COALESCE($2,nom), service_id = COALESCE($3,service_id),
           actif = COALESCE($4,actif), email = COALESCE($5,email), telephone = COALESCE($6,telephone), maj_le = now()
         WHERE id = $1 RETURNING *`,
        [id, texte(c.nom, 120), texte(c.service, 40), c.actif === undefined ? null : booleen(c.actif),
         texte(c.email, 160), texte(c.telephone, 40)]
      );
      if (!rows[0]) return erreur(res, 404, "Collaborateur introuvable.", "INTROUVABLE");
      await journaliser(s.compte, "collaborateur_modif", id, null, req);
      return ok(res, { collaborateur: LIGNE_COLLABORATEUR(rows[0]) });
    }
    if (methode === "DELETE") {
      const { rows } = await query(`UPDATE collaborateurs SET actif = false, maj_le = now() WHERE id = $1 RETURNING id`, [id]);
      if (!rows[0]) return erreur(res, 404, "Collaborateur introuvable.", "INTROUVABLE");
      await journaliser(s.compte, "collaborateur_desactivation", id, null, req);
      return ok(res, { ok: true, id });
    }
  }

  /* --- Véhicules --- */
  if (chemin === "/vehicules" && methode === "POST") {
    const s = await exigerSession(req, res); if (!s) return;
    const c = await lireCorps(req); if (!c) return erreur(res, 400, "Requête illisible.", "CORPS_INVALIDE");
    const id = texte(c.id, 40) || ("V" + Date.now().toString(36));
    const { rows } = await query(
      `INSERT INTO vehicules (id, plaque, marque, modele, type, annee, km, service_id, etat, entretien, note)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)
       ON CONFLICT (id) DO UPDATE SET plaque=EXCLUDED.plaque, marque=EXCLUDED.marque, modele=EXCLUDED.modele,
         type=EXCLUDED.type, annee=EXCLUDED.annee, km=EXCLUDED.km, service_id=EXCLUDED.service_id,
         etat=EXCLUDED.etat, entretien=EXCLUDED.entretien, note=EXCLUDED.note, maj_le=now()
       RETURNING *`,
      [id, texte(c.plate, 20), texte(c.marque, 60), texte(c.modele, 60), texte(c.type, 40),
       nombre(c.annee), nombre(c.km), texte(c.service, 40), texte(c.state, 40), dateISO(c.entretien), texte(c.note, 300)]
    );
    await journaliser(s.compte, "vehicule_ajout", id, { plaque: rows[0].plaque }, req);
    return ok(res, { vehicule: LIGNE_VEHICULE(rows[0]) });
  }
  const mVehi = chemin.match(/^\/vehicules\/([^/]+)$/);
  if (mVehi) {
    const s = await exigerSession(req, res); if (!s) return;
    const id = decodeURIComponent(mVehi[1]);
    if (methode === "PATCH" || methode === "PUT") {
      const c = await lireCorps(req); if (!c) return erreur(res, 400, "Requête illisible.", "CORPS_INVALIDE");
      const { rows } = await query(
        `UPDATE vehicules SET plaque = COALESCE($2,plaque), marque = COALESCE($3,marque), modele = COALESCE($4,modele),
           type = COALESCE($5,type), annee = COALESCE($6,annee), km = COALESCE($7,km), service_id = COALESCE($8,service_id),
           etat = COALESCE($9,etat), entretien = COALESCE($10,entretien), note = COALESCE($11,note), maj_le = now()
         WHERE id = $1 RETURNING *`,
        [id, texte(c.plate, 20), texte(c.marque, 60), texte(c.modele, 60), texte(c.type, 40), nombre(c.annee),
         nombre(c.km), texte(c.service, 40), texte(c.state, 40), dateISO(c.entretien), texte(c.note, 300)]
      );
      if (!rows[0]) return erreur(res, 404, "Véhicule introuvable.", "INTROUVABLE");
      await journaliser(s.compte, "vehicule_modif", id, null, req);
      return ok(res, { vehicule: LIGNE_VEHICULE(rows[0]) });
    }
    if (methode === "DELETE") {
      const { rows } = await query(`DELETE FROM vehicules WHERE id = $1 RETURNING id`, [id]);
      if (!rows[0]) return erreur(res, 404, "Véhicule introuvable.", "INTROUVABLE");
      await journaliser(s.compte, "vehicule_suppression", id, null, req);
      return ok(res, { ok: true, id });
    }
  }

  /* --- Paramètres --- */
  if (chemin === "/parametres" && methode === "PUT") {
    const s = await exigerSession(req, res); if (!s) return;
    const c = await lireCorps(req); if (!c) return erreur(res, 400, "Requête illisible.", "CORPS_INVALIDE");
    await avecTransaction(async (client) => {
      for (const cle in c) {
        if (typeof c[cle] === "object" && !Array.isArray(c[cle])) continue;
        await client.query(
          `INSERT INTO parametres (cle, valeur, maj_le) VALUES ($1,$2,now())
           ON CONFLICT (cle) DO UPDATE SET valeur = EXCLUDED.valeur, maj_le = now()`,
          [texte(cle, 60), JSON.stringify(c[cle])]
        );
      }
    });
    await journaliser(s.compte, "parametres_modif", null, { cles: Object.keys(c) }, req);
    return ok(res, { ok: true });
  }

  /* --- Comptes (administration) --- */
  const mCompte = chemin.match(/^\/comptes\/([^/]+)(\/mot-de-passe|\/reinitialiser)?$/);
  if (mCompte) {
    const s = await exigerAdmin(req, res); if (!s) return;
    const id = decodeURIComponent(mCompte[1]);
    const action = mCompte[2];

    if (action === "/mot-de-passe" && (methode === "POST" || methode === "PUT")) {
      const c = await lireCorps(req);
      const pwd = String((c && c.motDePasse) || "");
      if (pwd.length < 6) return erreur(res, 400, "Le mot de passe doit contenir au moins 6 caractères.", "MOT_DE_PASSE_COURT");
      const { rowCount } = await query(`UPDATE comptes SET mot_de_passe_hash = $2, maj_le = now() WHERE id = $1`,
        [id, hacherMotDePasse(pwd)]);
      if (!rowCount) return erreur(res, 404, "Compte introuvable.", "INTROUVABLE");
      await query(`UPDATE sessions SET revoquee_le = now() WHERE compte_id = $1 AND revoquee_le IS NULL`, [id]);
      await journaliser(s.compte, "compte_mot_de_passe", id, { sessions_revoquees: true }, req);
      return ok(res, { ok: true, note: "Mot de passe modifié. Les sessions actives de ce compte ont été révoquées." });
    }

    if (action === "/reinitialiser" && methode === "POST") {
      const { rowCount } = await query(
        `UPDATE comptes SET mot_de_passe_hash = COALESCE(mot_de_passe_defaut_hash, mot_de_passe_hash), maj_le = now()
         WHERE id = $1`, [id]);
      if (!rowCount) return erreur(res, 404, "Compte introuvable.", "INTROUVABLE");
      await query(`UPDATE sessions SET revoquee_le = now() WHERE compte_id = $1 AND revoquee_le IS NULL`, [id]);
      await journaliser(s.compte, "compte_reinitialisation", id, null, req);
      return ok(res, { ok: true });
    }

    if (methode === "PATCH" || methode === "PUT") {
      const c = await lireCorps(req); if (!c) return erreur(res, 400, "Requête illisible.", "CORPS_INVALIDE");
      const login = c.login === undefined ? null : (texte(c.login, 40) || "").toLowerCase();
      if (login !== null && login.length < 3) return erreur(res, 400, "Identifiant trop court (3 caractères minimum).", "IDENTIFIANT_COURT");
      if (login) {
        const dbl = await query(`SELECT id FROM comptes WHERE lower(identifiant) = $1 AND id <> $2`, [login, id]);
        if (dbl.rowCount) return erreur(res, 409, "Cet identifiant est déjà utilisé.", "IDENTIFIANT_PRIS");
      }
      const { rows } = await query(
        `UPDATE comptes SET identifiant = COALESCE($2,identifiant), nom = COALESCE($3,nom),
           role = COALESCE($4,role), actif = COALESCE($5,actif), maj_le = now()
         WHERE id = $1 RETURNING *`,
        [id, login, texte(c.label, 120), texte(c.role, 80), c.actif === undefined ? null : booleen(c.actif)]
      );
      if (!rows[0]) return erreur(res, 404, "Compte introuvable.", "INTROUVABLE");
      if (c.actif !== undefined && !booleen(c.actif)) {
        await query(`UPDATE sessions SET revoquee_le = now() WHERE compte_id = $1 AND revoquee_le IS NULL`, [id]);
      }
      await journaliser(s.compte, "compte_modif", id, { champs: Object.keys(c) }, req);
      return ok(res, { compte: LIGNE_COMPTE_PUBLIC(rows[0]) });
    }
  }

  /* --- Journal administratif (admin uniquement) --- */
  if (chemin === "/journal" && methode === "GET") {
    const s = await exigerAdmin(req, res); if (!s) return;
    const limite = Math.min(Number(q.get("limite") || 200), 500);
    const { rows } = await query(
      `SELECT id, at, compte_identifiant, action, cible, details, ip FROM journal ORDER BY id DESC LIMIT $1`, [limite]);
    return ok(res, { entrees: rows, total: rows.length });
  }

  /* --- Sessions actives (informations de sécurité) --- */
  if (chemin === "/sessions" && methode === "GET") {
    const s = await exigerAdmin(req, res); if (!s) return;
    const { rows } = await query(
      `SELECT s.id, s.compte_id, c.identifiant, s.cree_le, s.expire_le, s.revoquee_le, s.ip IS NOT NULL AND s.ip <> '' AS avec_ip
         FROM sessions s JOIN comptes c ON c.id = s.compte_id
        WHERE s.revoquee_le IS NULL AND s.expire_le > now()
        ORDER BY s.cree_le DESC LIMIT 100`);
    return ok(res, { sessions: rows });
  }

  return erreur(res, 404, "Route inconnue : " + methode + " " + chemin, "ROUTE_INCONNUE");
}

/* ============================ POINT D'ENTRÉE ============================= */
module.exports = async (req, res) => {
  try {
    await route(req, res);
  } catch (e) {
    const code = e && e.code === "NO_DATABASE_URL" ? 500 : 500;
    if (process.env.NODE_ENV !== "production") console.error("[api]", e);
    if (!res.headersSent) {
      erreur(res, code, "Erreur serveur : " + (e.message || "inconnue"),
        e && e.code ? e.code : "ERREUR_SERVEUR");
    }
  }
};
