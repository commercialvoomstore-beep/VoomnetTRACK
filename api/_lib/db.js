/* ============================================================================
   Connexion PostgreSQL — compatible Neon (Vercel) et PostgreSQL local.
   La chaîne de connexion est lue dans la variable d'environnement DATABASE_URL
   et n'est JAMAIS exposée au navigateur.
   ============================================================================ */
"use strict";
const { Pool } = require("pg");

let pool = null;

function chaine() {
  const cs = process.env.DATABASE_URL || process.env.POSTGRES_URL || "";
  if (!cs) {
    const e = new Error("DATABASE_URL absent : renseignez la chaîne de connexion Neon.");
    e.code = "NO_DATABASE_URL";
    throw e;
  }
  return cs;
}

function getPool() {
  if (pool) return pool;
  const cs = chaine();
  /* Neon impose TLS ; en local (postgres://…@127.0.0.1) on reste en clair. */
  const besoinSSL = /sslmode=require|neon\.tech|sslmode=prefer/.test(cs);
  pool = new Pool({
    connectionString: cs,
    ssl: besoinSSL ? { rejectUnauthorized: false } : false,
    max: 3,                      /* serverless : peu de connexions, libérées vite */
    idleTimeoutMillis: 8000,
    connectionTimeoutMillis: 12000,
    allowExitOnIdle: true
  });
  pool.on("error", () => { /* une connexion oisive peut tomber : on laisse le pool se reconstruire */ });
  return pool;
}

async function query(text, params) {
  return getPool().query(text, params);
}

async function avecTransaction(fn) {
  const client = await getPool().connect();
  try {
    await client.query("BEGIN");
    const r = await fn(client);
    await client.query("COMMIT");
    return r;
  } catch (e) {
    try { await client.query("ROLLBACK"); } catch (_) {}
    throw e;
  } finally {
    client.release();
  }
}

module.exports = { getPool, query, avecTransaction };
