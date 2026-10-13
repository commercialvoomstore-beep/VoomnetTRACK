#!/usr/bin/env node
/* ============================================================================
   Serveur de développement local — reproduit exactement ce que fait Vercel :
     • les fichiers statiques (index.html, assets…) sont servis à la racine
     • tout ce qui commence par /api/ passe par la même fonction serverless
   Usage :  DATABASE_URL="postgres://…" node dev-server.js   (PORT=8090)
   ============================================================================ */
"use strict";
const http = require("http");
const fs = require("fs");
const path = require("path");
const handler = require("./api/index.js");

const PORT = Number(process.env.PORT || 8090);
const ROOT = __dirname;

const TYPES = {
  ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8",
  ".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml", ".woff2": "font/woff2", ".pdf": "application/pdf", ".ico": "image/x-icon"
};

const serveur = http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://" + (req.headers.host || "localhost"));

  if (url.pathname === "/api" || url.pathname.startsWith("/api/")) {
    res.setHeader("Cache-Control", "no-store");
    try { return await handler(req, res); }
    catch (e) {
      res.statusCode = 500;
      res.setHeader("Content-Type", "application/json; charset=utf-8");
      return res.end(JSON.stringify({ erreur: "Erreur serveur locale : " + e.message }));
    }
  }

  let rel = decodeURIComponent(url.pathname);
  if (rel === "/") rel = "/index.html";
  const fichier = path.join(ROOT, rel);
  if (!fichier.startsWith(ROOT) || rel.startsWith("/api") || /(^|\/)(\.git|node_modules|db|api)(\/|$)/.test(rel)) {
    res.statusCode = 403; return res.end("Interdit");
  }
  fs.readFile(fichier, (err, data) => {
    if (err) { res.statusCode = 404; return res.end("Fichier introuvable : " + rel); }
    res.statusCode = 200;
    res.setHeader("Content-Type", TYPES[path.extname(fichier).toLowerCase()] || "application/octet-stream");
    res.setHeader("Cache-Control", "no-store, must-revalidate");
    res.end(data);
  });
});

serveur.listen(PORT, "0.0.0.0", () => {
  console.log("VOOMNET Track — développement local sur le port " + PORT);
  console.log("  application : http://localhost:" + PORT + "/index.html");
  console.log("  API         : http://localhost:" + PORT + "/api/health");
  console.log("  base        : " + (process.env.DATABASE_URL ? "DATABASE_URL définie" : "DATABASE_URL ABSENTE ⚠"));
});
