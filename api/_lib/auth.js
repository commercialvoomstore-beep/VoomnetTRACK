/* ============================================================================
   Authentification & sessions — 100 % côté serveur.
   - mots de passe hachés en scrypt (jamais stockés ni renvoyés en clair)
   - jetons de session aléatoires, stockés hachés (SHA-256) en base
   - le rôle est TOUJOURS relu en base : le navigateur ne décide de rien
   ============================================================================ */
"use strict";
const crypto = require("crypto");
const { query } = require("./db");

const DUREE_SESSION_H = Number(process.env.SESSION_HOURS || 12);

/* ---- Mots de passe ---------------------------------------------------- */
function hacherMotDePasse(motDePasse) {
  const sel = crypto.randomBytes(16).toString("hex");
  const h = crypto.scryptSync(String(motDePasse), sel, 64).toString("hex");
  return "scrypt$" + sel + "$" + h;
}
function verifierMotDePasse(motDePasse, stocke) {
  if (!stocke || typeof stocke !== "string") return false;
  const p = stocke.split("$");
  if (p.length !== 3 || p[0] !== "scrypt") return false;
  const calc = crypto.scryptSync(String(motDePasse), p[1], 64);
  const ref = Buffer.from(p[2], "hex");
  if (ref.length !== calc.length) return false;
  return crypto.timingSafeEqual(ref, calc);
}

/* ---- Jetons de session ------------------------------------------------ */
function sha256(txt) { return crypto.createHash("sha256").update(txt).digest("hex"); }

async function creerSession(compte, req) {
  const jeton = crypto.randomBytes(32).toString("base64url");
  const expire = new Date(Date.now() + DUREE_SESSION_H * 3600 * 1000);
  await query(
    `INSERT INTO sessions (jeton_hash, compte_id, expire_le, ip, agent)
     VALUES ($1,$2,$3,$4,$5)`,
    [sha256(jeton), compte.id, expire, ipDe(req), String(req.headers["user-agent"] || "").slice(0, 300)]
  );
  await query(`UPDATE comptes SET derniere_connexion_le = now() WHERE id = $1`, [compte.id]);
  return { jeton, expire };
}

async function sessionDepuisRequete(req) {
  const h = String(req.headers.authorization || "");
  const m = h.match(/^Bearer\s+(.+)$/i);
  if (!m) return null;
  const { rows } = await query(
    `SELECT s.id AS session_id, s.expire_le, c.id, c.identifiant, c.nom, c.role, c.admin, c.actif
       FROM sessions s JOIN comptes c ON c.id = s.compte_id
      WHERE s.jeton_hash = $1 AND s.revoquee_le IS NULL AND s.expire_le > now()`,
    [sha256(m[1].trim())]
  );
  const r = rows[0];
  if (!r) return null;
  if (!r.actif) return null;                 /* compte désactivé → session morte */
  return {
    sessionId: r.session_id,
    expireLe: r.expire_le,
    compte: { id: r.id, login: r.identifiant, label: r.nom, role: r.role, admin: !!r.admin }
  };
}

async function fermerSession(req) {
  const h = String(req.headers.authorization || "");
  const m = h.match(/^Bearer\s+(.+)$/i);
  if (!m) return false;
  const r = await query(`UPDATE sessions SET revoquee_le = now() WHERE jeton_hash = $1 AND revoquee_le IS NULL`,
    [sha256(m[1].trim())]);
  return r.rowCount > 0;
}

async function purgerSessionsExpirees() {
  try { await query(`DELETE FROM sessions WHERE expire_le < now() - interval '7 days'`); } catch (_) {}
}

function ipDe(req) {
  const f = String(req.headers["x-forwarded-for"] || "").split(",")[0].trim();
  return f || (req.socket && req.socket.remoteAddress) || "";
}

/* ---- Journal administratif -------------------------------------------- */
async function journaliser(compte, action, cible, details, req) {
  try {
    await query(
      `INSERT INTO journal (compte_identifiant, action, cible, details, ip)
       VALUES ($1,$2,$3,$4,$5)`,
      [compte ? compte.login || compte.identifiant || null : null, action, cible || null,
       details ? JSON.stringify(details) : null, req ? ipDe(req) : null]
    );
  } catch (_) { /* la journalisation ne doit jamais bloquer l'action */ }
}

/* ---- Limitation des tentatives de connexion ---------------------------- */
const essais = new Map();               /* clé ip|identifiant → {n, jusqua} */
const MAX_ESSAIS = Number(process.env.MAX_LOGIN_TRIES || 8);
const FENETRE_MS = 10 * 60 * 1000;

function essaisBloques(cle) {
  const e = essais.get(cle);
  if (!e) return 0;
  if (Date.now() > e.jusqua) { essais.delete(cle); return 0; }
  return e.n;
}
function noterEchec(cle) {
  const e = essais.get(cle) || { n: 0, jusqua: Date.now() + FENETRE_MS };
  e.n += 1; e.jusqua = Date.now() + FENETRE_MS;
  essais.set(cle, e);
}
function reinitialiserEssais(cle) { essais.delete(cle); }

module.exports = {
  hacherMotDePasse, verifierMotDePasse, creerSession, sessionDepuisRequete,
  fermerSession, purgerSessionsExpirees, journaliser, ipDe,
  essaisBloques, noterEchec, reinitialiserEssais, MAX_ESSAIS
};
