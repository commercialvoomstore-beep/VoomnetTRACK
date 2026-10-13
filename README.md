# VOOMNET Track — Suivi des dépenses de déplacement

Application web de pilotage de la mobilité VOOMNET : déplacements, services, collaborateurs,
coûts et rapports mensuels PDF — **reliée à une base PostgreSQL (Neon)** et déployée sur **Vercel**.

> Une seule interface RH centralisée. *« Votre partenaire à votre service ».*

---

## Architecture

```
Navigateur  ──►  index.html (interface, une seule page, sans dépendance externe)
                     │  requêtes /api/*
                     ▼
             Vercel (fonction serverless  api/index.js)
                     │  protocole PostgreSQL + TLS
                     ▼
             Neon — base PostgreSQL (source de vérité unique)
```

* **Authentification 100 % serveur** : mots de passe hachés en **scrypt** en base, jetons de
  session aléatoires stockés **hachés** (SHA-256), expiration et révocation effectives.
* **Le rôle est relu en base à chaque requête** : le navigateur ne décide jamais de ses droits.
* **Aucun secret dans le navigateur** : ni mot de passe, ni empreinte — le fichier livré peut
  être public sans risque.
* **Écritures journalisées** : chaque ajout / modification / suppression / connexion est tracé
  dans la table `journal` (qui, quoi, quand, depuis quelle adresse).
* **Suppression douce** : un déplacement supprimé est marqué `supprime_le`, jamais détruit.

## Mise en service

### 1. Base de données (Neon)

```bash
export DATABASE_URL="postgres://user:motdepasse@ep-xxx-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require"
node db/migrate.js                                    # crée les tables (idempotent, ne détruit rien)
SEED_RH_PASSWORD="…" SEED_ADMIN_PASSWORD="…" node db/seed.js   # comptes + référentiels
```
La chaîne de connexion se trouve dans Neon → **Connect** → *Connection string* (celle du
**pooler**, avec `-pooler`, adaptée au serverless).

### 2. Déploiement (Vercel)

1. Importer le dépôt `commercialvoomstore-beep/VoomnetTRACK`.
2. **Settings → Environment Variables** : `DATABASE_URL` = la chaîne Neon ci-dessus
   (l'intégration Neon la renseigne automatiquement dans la plupart des cas).
3. Déployer. Vérifier ensuite : `https://<votre-domaine>/api/health` doit répondre
   `{"ok":true,"base":"connectee"}`.

### 3. Développement local

```bash
npm install
DATABASE_URL="postgres://postgres@127.0.0.1:5432/voomnet" node db/migrate.js
DATABASE_URL="…" node dev-server.js          # http://localhost:8090 — statique + API, comme sur Vercel
```

## Contrôles

| Suite | Objet |
|---|---|
| `test/cloud_test.py` | **22 contrôles** : sécurité des routes, connexion, écriture réelle en base, journal, révocation de session, aucune empreinte exposée, refus de fonctionner sans base. |
| `test/ui_v2.py` | Parcours visuel complet (splash, vues, filtres, exports PDF/CSV, déconnexion, responsive). |

## Structure

```
index.html            application complète (auto-portante, hors bibliothèques)
api/index.js          API : santé, authentification, déplacements, collaborateurs, véhicules,
                      paramètres, comptes, journal — une fonction, plusieurs routes
api/_lib/             connexion PostgreSQL, sessions/scrypt, utilitaires HTTP
db/schema.sql         schéma (idempotent) + référentiels services / transports / paramètres
db/migrate.js         application du schéma      db/seed.js  comptes et données de départ
dev-server.js         serveur local identique au comportement Vercel
src/                  sources de l'interface (assemblées par build.py)  •  assets/  logos & police
identite-visuelle/    kit de marque   •   exemples/  rapport type   •   test/  contrôles
```

## Sécurité — ce qui est garanti

* Aucun mot de passe en clair, nulle part ; aucun identifiant affiché sur l'écran de connexion.
* Aucune route de données accessible sans jeton valide (401), aucune route d'administration
  sans rôle ADMIN vérifié en base (403).
* Limitation des tentatives de connexion et journalisation des échecs.
* Aucun CDN ni ressource externe : l'interface ne parle qu'à votre propre API.

---

*VOOMNET Track v3.11 — Abidjan, Côte d'Ivoire.*
