#!/usr/bin/env node
/* ============================================================================
   Données de départ : collaborateurs, véhicules, comptes d'accès.

   Les mots de passe NE SONT PAS écrits dans ce fichier : ils arrivent par
   variables d'environnement puis sont hachés (scrypt) avant insertion.

   Usage :
     DATABASE_URL="…" SEED_RH_PASSWORD="…" SEED_ADMIN_PASSWORD="…" node db/seed.js
   ============================================================================ */
"use strict";
const { Client } = require("pg");
const crypto = require("crypto");

const hacher = (pwd) => {
  const sel = crypto.randomBytes(16).toString("hex");
  return "scrypt$" + sel + "$" + crypto.scryptSync(String(pwd), sel, 64).toString("hex");
};

const { COLLABS, VEHICULES } = require("./seed-data");



(async () => {
  const cs = process.env.DATABASE_URL;
  if (!cs) { console.error("✗ DATABASE_URL manquant."); process.exit(1); }
  const pwdRh = process.env.SEED_RH_PASSWORD;
  const pwdAdmin = process.env.SEED_ADMIN_PASSWORD;
  if (!pwdRh || !pwdAdmin) {
    console.error("✗ SEED_RH_PASSWORD et SEED_ADMIN_PASSWORD sont requis (aucun mot de passe n'est écrit dans le code).");
    process.exit(1);
  }
  const ssl = /sslmode=require|neon\.tech/.test(cs) ? { rejectUnauthorized: false } : false;
  const client = new Client({ connectionString: cs, ssl, connectionTimeoutMillis: 15000 });

  try {
    await client.connect();

    for (const c of COLLABS) {
      await client.query(
        `INSERT INTO collaborateurs (id, nom, service_id, actif, email, telephone)
         VALUES ($1,$2,$3,true,$4,$5)
         ON CONFLICT (id) DO UPDATE SET nom = EXCLUDED.nom, service_id = EXCLUDED.service_id,
           email = EXCLUDED.email, telephone = EXCLUDED.telephone, maj_le = now()`,
        [c.id, c.nom, c.service, c.email, c.telephone]);
    }
    console.log("✓ collaborateurs :", COLLABS.length);

    for (const v of VEHICULES) {
      await client.query(
        `INSERT INTO vehicules (id, plaque, marque, modele, type, annee, km, service_id, etat, entretien, note)
         VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)
         ON CONFLICT (id) DO UPDATE SET plaque = EXCLUDED.plaque, marque = EXCLUDED.marque,
           modele = EXCLUDED.modele, type = EXCLUDED.type, annee = EXCLUDED.annee, km = EXCLUDED.km,
           service_id = EXCLUDED.service_id, etat = EXCLUDED.etat, entretien = EXCLUDED.entretien,
           note = EXCLUDED.note, maj_le = now()`,
        [v.id, v.plate, v.marque, v.modele, v.type, v.annee, v.km, v.service, v.state, v.entretien, v.note]);
    }
    console.log("✓ véhicules :", VEHICULES.length);

    /* Comptes : créés s'ils n'existent pas ; le mot de passe déjà défini n'est
       JAMAIS écrasé (on conserve l'empreinte d'origine pour la réinitialisation). */
    const comptes = [
      { id: "rh",    login: "rh",    nom: "Service Ressources Humaines", role: "Responsable RH",     admin: false, pwd: pwdRh },
      { id: "admin", login: "admin", nom: "Administrateur VOOMNET",      role: "Administrateur RH",  admin: true,  pwd: pwdAdmin }
    ];
    for (const c of comptes) {
      const h = hacher(c.pwd);
      const r = await client.query(
        `INSERT INTO comptes (id, identifiant, nom, role, admin, actif, mot_de_passe_hash, mot_de_passe_defaut_hash)
         VALUES ($1,$2,$3,$4,$5,true,$6,$6)
         ON CONFLICT (id) DO UPDATE SET nom = EXCLUDED.nom, role = EXCLUDED.role, admin = EXCLUDED.admin,
           mot_de_passe_defaut_hash = COALESCE(comptes.mot_de_passe_defaut_hash, EXCLUDED.mot_de_passe_defaut_hash),
           maj_le = now()
         RETURNING (xmax = 0) AS cree`,
        [c.id, c.login, c.nom, c.role, c.admin, h]);
      console.log("  compte", c.login, r.rows[0].cree ? "créé" : "déjà présent (mot de passe inchangé)");
    }
  } catch (e) {
    console.error("✗ échec :", e.message);
    process.exitCode = 1;
  } finally {
    await client.end().catch(() => {});
  }
})();
