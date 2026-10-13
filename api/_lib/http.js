/* ============================================================================
   Petits utilitaires HTTP partagés par toutes les routes de l'API.
   ============================================================================ */
"use strict";

function json(res, status, obj, extraHeaders) {
  const corps = JSON.stringify(obj);
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("X-Content-Type-Options", "nosniff");
  if (extraHeaders) for (const k in extraHeaders) res.setHeader(k, extraHeaders[k]);
  res.end(corps);
}

function ok(res, obj) { json(res, 200, obj); }
function erreur(res, status, message, code) {
  json(res, status, { erreur: message, code: code || status });
}

async function lireCorps(req) {
  /* Vercel (Node) peut déjà avoir analysé le corps JSON. */
  if (req.body && typeof req.body === "object" && !Buffer.isBuffer(req.body)) return req.body;
  if (typeof req.body === "string") { try { return JSON.parse(req.body); } catch (_) { return {}; } }
  if (Buffer.isBuffer(req.body)) { try { return JSON.parse(req.body.toString("utf8")); } catch (_) { return {}; } }
  const morceaux = [];
  for await (const m of req) morceaux.push(m);
  const txt = Buffer.concat(morceaux).toString("utf8");
  if (!txt) return {};
  try { return JSON.parse(txt); } catch (_) { return null; }
}

/* --- Conversions sûres : aucune valeur libre ne part dans une colonne --- */
function texte(valeur, max = 500) {
  if (valeur === undefined || valeur === null) return null;
  const s = String(valeur).trim();
  return s.length > max ? s.slice(0, max) : s;
}
function nombre(valeur) {
  if (valeur === undefined || valeur === null || valeur === "") return null;
  const n = Number(String(valeur).replace(",", "."));
  return Number.isFinite(n) ? n : null;
}
function booleen(valeur) {
  return valeur === true || valeur === "true" || valeur === 1 || valeur === "1";
}
function dateISO(valeur) {
  const s = texte(valeur, 10);
  if (!s) return null;
  return /^\d{4}-\d{2}-\d{2}$/.test(s) ? s : null;
}

module.exports = { json, ok, erreur, lireCorps, texte, nombre, booleen, dateISO };
