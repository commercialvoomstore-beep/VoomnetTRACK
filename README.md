# VOOMNET Track — Suivi des dépenses de déplacement

Application web **autonome** (un seul fichier, 100 % hors-ligne) pour piloter les
dépenses de mobilité de VOOMNET : déplacements, services, collaborateurs, coûts et
rapports mensuels exportables en PDF.

> Plateforme RH de pilotage — une seule interface centralisée.
> *« Votre partenaire à votre service ».*

---

## Livrable

| Fichier | Rôle |
|---|---|
| **`index.html`** | L'application complète (≈ 780 Ko). Aucune installation, aucun serveur, aucune ressource externe : ouvrez-la dans un navigateur. |
| `README_VOOMNET.md` | Documentation détaillée : architecture RH, palette, prompts de génération, historique v2 → v3.10. |

## Utilisation

1. Ouvrir **`index.html`** dans un navigateur récent (Chrome, Edge, Firefox, Safari).
2. Saisir les identifiants communiqués par la Direction *(ils ne sont volontairement
   présents ni dans ce dépôt, ni dans l'interface)*.
3. Enregistrer un déplacement, filtrer par service, puis générer le **rapport mensuel PDF**.
   Le PDF, le CSV et le JSON sont enregistrés **sur l'appareil de l'utilisateur**.

Les données restent **en local sur l'appareil** (aucun envoi vers un serveur).
C'est une application de suivi interne : elle ne nécessite aucune connexion internet.

## Structure du projet

```
index.html                  ← livrable : application complète et autonome
build.py                    ← assemble src/ + assets/ en index.html (logos en data-URI)
serve.py                    ← serveur d'aperçu local sans cache (PORT=8080 par défaut)
src/                        ← sources séparées, assemblées par build.py
  part1_head.html           ← design system, typographies, animations (véhicule)
  part2_body.html           ← écran d'accès, header, sidebar, vues
  part3_core.js.html        ← session, comptes, données, services, icônes
  part3b_dash.js.html       ← tableaux de bord, graphiques, filtres
  part4_pdf.js.html         ← moteur PDF maison (aucune bibliothèque externe)
  _archive/                 ← patchs historiques des versions v3.x (archive)
assets/                     ← logos des services, police Inter, favicons
identite-visuelle/          ← kit de marque VOOMNET Track (PNG/JPG, 400 → 1600 px)
exemples/                   ← exemple de rapport mensuel généré
uploads/                    ← visuels sources fournis par la Direction
test/                       ← scripts de contrôle automatisé (Playwright) et maquettes
```

## Reconstruire `index.html`

```bash
python3 build.py          # assemble src/ + assets/ → index.html
PORT=8080 python3 serve.py  # aperçu local sans cache
```

Après toute modification de `src/`, relancer `build.py` puis **recharger sans cache**
(Ctrl + Shift + R), l'application embarquant ses ressources en `data:`.

## Sécurité

- Aucun mot de passe n'est stocké **en clair** : seules des empreintes sont conservées.
- Aucun identifiant n'est affiché sur l'écran de connexion.
- Aucun accès anonyme (« consultation ») n'existe : toute entrée exige une authentification.
- Aucune ressource externe (CDN, police distante) : l'application ne fuit rien vers l'extérieur.

## Contrôles

`test/ui_v2.py` déroule un parcours complet dans un navigateur headless (connexion,
enregistrement d'un déplacement, filtres, exports PDF/CSV, verrouillage, déconnexion,
responsive) et se termine par `erreurs : aucune`.

---

*VOOMNET Track v3.10 — Abidjan, Côte d'Ivoire.*
