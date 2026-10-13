#!/usr/bin/env node
/* ============================================================================
   Application du schéma sur la base ciblée par DATABASE_URL.
   Idempotent : ne supprime ni n'écrase aucune donnée existante.

   Usage :
     DATABASE_URL="postgres://…" node db/migrate.js
   ============================================================================ */
"use strict";
const fs = require("fs");
const path = require("path");
const { Client } = require("pg");

(async () => {
  const cs = process.env.DATABASE_URL;
  if (!cs) {
    console.error("✗ DATABASE_URL manquant.");
    console.error('  Exemple : DATABASE_URL="postgres://user:motdepasse@host/neondb?sslmode=require" node db/migrate.js');
    process.exit(1);
  }
  const sql = fs.readFileSync(path.join(__dirname, "schema.sql"), "utf8");
  const ssl = /sslmode=require|neon\.tech/.test(cs) ? { rejectUnauthorized: false } : false;
  const client = new Client({ connectionString: cs, ssl, connectionTimeoutMillis: 15000 });

  try {
    await client.connect();
    const { rows } = await client.query("SELECT current_database() AS base, current_user AS utilisateur");
    console.log("→ base :", rows[0].base, "| utilisateur :", rows[0].utilisateur);

    const avant = await client.query(`SELECT count(*)::int AS n FROM information_schema.tables WHERE table_schema='public'`);
    await client.query(sql);
    const apres = await client.query(`SELECT count(*)::int AS n FROM information_schema.tables WHERE table_schema='public'`);

    const tables = await client.query(
      `SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name`);
    console.log("✓ schéma appliqué — tables présentes :", tables.rows.map(r => r.table_name).join(", "));
    console.log("  (avant : " + avant.rows[0].n + " table(s), après : " + apres.rows[0].n + ")");

    const c = await client.query(`SELECT count(*)::int AS n FROM comptes`);
    const s = await client.query(`SELECT count(*)::int AS n FROM services`);
    const t = await client.query(`SELECT count(*)::int AS n FROM transports`);
    const d = await client.query(`SELECT count(*)::int AS n FROM deplacements`);
    console.log(`  comptes : ${c.rows[0].n} | services : ${s.rows[0].n} | transports : ${t.rows[0].n} | déplacements : ${d.rows[0].n}`);
    if (c.rows[0].n === 0) console.log("  ℹ aucun compte : lancez « node db/seed.js » pour créer les accès.");
  } catch (e) {
    console.error("✗ échec :", e.message);
    process.exitCode = 1;
  } finally {
    await client.end().catch(() => {});
  }
})();
