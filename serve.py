#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Serveur de prévisualisation VOOMNET Track.

Sert le dossier courant en forçant l'absence de cache :
  Cache-Control: no-store, no-cache, must-revalidate, max-age=0
Ainsi, chaque rechargement de l'aperçu affiche la DERNIÈRE version du fichier,
sans jamais resservir une ancienne copie depuis le cache du navigateur.
"""
import http.server
import socketserver
import sys
import os

PORT = int(os.environ.get("PORT", "8000"))
ROOT = os.environ.get("ROOT", os.getcwd())


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


class ReusableTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    with ReusableTCPServer(("0.0.0.0", PORT), NoCacheHandler) as httpd:
        print(f"VOOMNET Track — aperçu sans cache sur le port {PORT} (racine : {ROOT})", flush=True)
        httpd.serve_forever()
