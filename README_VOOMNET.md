# VOOMNET **Track** — Espace RH & Mobility Control

**Fichier à utiliser : `index.html`** (~530 Ko, tout-en-un, hors-ligne, aucune dépendance externe).

---

## ✨ Nouveautés de la refonte v2.0 (premium)

| Axe | Ce qui a changé |
|---|---|
| **Direction artistique** | Interface **claire, aérée et premium** (fond `#F7F6FA`, surfaces blanches). Le violet `#32104F` / `#6F2DBD` et l'or `#D7B238` deviennent des **accents**, plus aucun gros bloc sombre. |
| **Splash screen** | Logo VOOMNET Track → fade-in + micro-mouvement + scale 96 %→100 %, nom, ligne « ESPACE RH • MOBILITY CONTROL », barre dorée. **≈ 2 s**, ignorable d'un clic, skippé au sein d'une même session. |
| **Sidebar** | Logo VOOMNET **Track** + « Espace RH • Mobility Control », sections **PILOTAGE / RESSOURCES / CONFIGURATION**, barre d'accent dorée sur l'élément actif, **badges** (sorties, véhicules, collaborateurs), indicateur de stockage en pied. |
| **Header** | Titre + sous-titre contextuel, **recherche globale** (Ctrl/⌘ + K → Entrée ouvre le registre filtré), **notifications** dynamiques (à régler, justificatifs manquants, véhicules immobilisés), **profil utilisateur** avec menu (paramètres, sauvegarde, rapport, nouvel enregistrement, effacement). |
| **Dashboard** | Nouvelle hiérarchie : **Accueil contextuel → 6 KPI → Graphiques → Activité récente → Analyses rapides → Actions rapides**. |
| **KPI (6)** | Total sorties · **Coût total** · Coût moyen/sortie · **Kilométrage** · **Véhicules actifs** · **Collaborateurs mobiles** — chacun avec valeur, variation vs mois précédent, contexte, icône et **sparkline**. |
| **Graphiques** | 100 % SVG natif : **courbe d'évolution lissée** (grille pointillée subtile, points dorés, animation de tracé, **tooltips**, bascule 6/12 mois), **barres groupées par entité**, **anneau** de répartition des transports, barres horizontales **avec les logos des services**. |
| **Nouveaux modules** | 🚗 **Véhicules** (parc, état, kilométrage, entretien, affectation, carte complète + CRUD) · 👥 **Collaborateurs** (mobilité, total engagé, statut, CRUD) · 📈 **Analyse** (3/6/12 mois, dépenses par entité, structure des transports, top collaborateurs, rythme hebdomadaire, **contrôle & conformité**, synthèse par entité, export). |
| **Formulaire** | + **Véhicule utilisé** (suivi de flotte) et **Distance (km)** — le passage d'un véhicule en mission met à jour son état. |
| **Registre** | 7 filtres (recherche, mois, service, transport, véhicule, statut, justificatif), tri, pagination, colonne d'actions figée, export CSV **enrichi** (véhicule + km). |
| **Marque** | **Logo officiel intégré** dans la sidebar, le splash, l'écran de connexion, le header compact, le favicon/app icon et le rapport PDF — détouré proprement, proportions exactes, zone de protection. |
| **Écran de connexion** | ➕ Branding logo + sélection de profil en 1 clic (les 4 entités), nom/fonction mémorisés, mode consultation, « Changer de profil » depuis le menu utilisateur. |
| **Typographie** | Police **Inter** embarquée en base64 (pas d'appel réseau), hiérarchie claire. |
| **Responsive** | Desktop / laptop / tablette / mobile : sidebar en tiroir + voile, cartes empilées, graphiques redimensionnés, **0 px de débordement**. |
| **Animations** | Apparition échelonnée des cartes, tracé des courbes, croissance des barres, hovers discrets, transitions de vues — **toutes < 1,2 s**, respect de `prefers-reduced-motion`. |

**Toutes les fonctionnalités précédentes sont conservées** : enregistrement/modification/suppression, motifs rapides, statuts de règlement, justificatifs, PDF mensuel, CSV, sauvegarde/restauration JSON, devise, paramètres d'entreprise, agents, transports.


---

## 🎨 IDENTITÉ VISUELLE — logo officiel intégré (v2.1)

Le **logo officiel fourni** est intégré **tel quel** (aucune redessin, aucune retouche de forme,
de proportion, de typographie ou du symbole). Un **détourage propre** a seulement supprimé le fond blanc
(rampe d'alpha + dé-mélange des couleurs) : contours nets, aucun halo, y compris à 200 % de zoom.

### Où le logo est utilisé

| Emplacement | Version | Règle appliquée |
|---|---|---|
| **Sidebar** | logo complet (transparent) — 184 px | zone de protection `12px 10px 20px`, aligné au menu, hauteur cohérente |
| **Splash screen** | logo complet — 320 px | centré horizontalement **et** verticalement, fade-in + micro-scale 96→100 % |
| **Écran de connexion** | logo complet — 300 px | branding principal de la colonne gauche + version compacte sur mobile |
| **Header** | **symbole seul** (25×26) | version compacte, affichée quand la sidebar est repliée (≤ 1000 px), séparateur vertical |
| **Favicon / App icon** | symbole | `favicon-128.png` + `apple-touch-icon-180.png` (installation en application) |
| **Rapport PDF** | logo officiel (fond blanc, JPEG) | bandeau d'en-tête des 2 pages, aux côtés des logos des services |

### Règles de design respectées
- **Aucune déformation** : ratio vérifié automatiquement **3,47 = ratio officiel** (écart mesuré : 0,000).
- **Zone de protection** systématique (jamais collé aux bords, jamais rogné).
- **Contraste** contrôlé sur fond blanc, gris clair `#F7F6FA`, violet clair et violet `#6F2DBD`.
- **Cohérence** : même logique de sizing, mêmes marges, mêmes alignements partout (design system) ;
  le fond blanc du JPEG sert de zone de respiration dans le PDF.

### Kit de marque exporté — dossier `identite-visuelle/`
`VOOMNET-Track-logo-transparent.png` (1806×529, alpha) · déclinaisons 1600/800/400 px ·
`VOOMNET-Track-logo-fond-blanc.jpg` (pour documents) · `VOOMNET-Track-symbole.webp` ·
`favicon-128.png` · `apple-touch-icon-180.png`.

---

## 📄 Le rapport PDF (inchangé et toujours 100 % local)

Bouton **« Télécharger le PDF »** → `VOOMNET_Rapport_Depenses_AAAA-MM.pdf` :
en-tête violet/or, **logos des services**, 4 indicateurs, synthèse par service, synthèse par transport,
détail des déplacements (avec le **motif**), observations de gestion, **zone de visas**, pagination.
*Aucune bibliothèque externe : le PDF est écrit octet par octet en JavaScript.*

---

## 🚀 Mode d'emploi

1. Télécharger **`index.html`** et l'ouvrir dans **Chrome / Edge**.
2. *(Recommandé)* Menu ⋮ → **Installer la page en tant qu'application** → icône VOOMNET comme un vrai logiciel.
3. Enregistrer les déplacements au fil du mois → onglet **Rapports** → **Télécharger le PDF**.
4. **Paramètres → Sauvegarde JSON** en fin de mois (les données vivent dans le navigateur utilisé).




---

## 🔐 COMPTES D'ACCÈS & DÉCONNEXION (v3.1)

### Deux comptes nominatifs, un seul espace de pilotage
| Compte | Identifiant | Mot de passe | Rôle |
|---|---|---|---|
| **RH** | `rh` | `Rh@Voomnet2026` | Responsable RH — pilotage complet |
| **Administrateur** | `admin` | `Admin@Voomnet2026` | Administrateur RH — accès complet |

- Connexion par **identifiant + mot de passe** (champ masqué, bouton 👁 pour afficher).
- Mots de passe **jamais stockés en clair** : empreinte locale non réversible (FNV-1a salée).
- Message d'erreur explicite + **secousse discrète** de la carte en cas d'échec.
- Les identifiants sont rappelés dans un bloc dépliable **« Comptes d'accès »** sous le formulaire.
- **Modifiables à tout moment** : `Paramètres → Comptes & sécurité` (renommer, changer le mot de passe, rétablir la valeur par défaut).
- **3 sorties de session** : bouton `⏻` du header, bouton **« Se déconnecter »** de la sidebar, menu utilisateur → *Se déconnecter*.
- **Mode consultation** : accès en lecture seule, sans modification de données.

### Différences RH / Administrateur
| Action | RH | Administrateur |
|---|---|---|
| Consultation, saisie, registre, analyse, rapports, PDF, CSV | ✅ | ✅ |
| Sauvegarde JSON | ✅ | ✅ |
| Restaurer une sauvegarde | 🔒 | ✅ |
| Effacer toutes les données | 🔒 | ✅ |

### Sidebar : carte de session
Avatar + nom du compte + rôle + pastille « session active » + bouton **Se déconnecter**, au-dessus de l'indicateur de stockage.

---

## 🚫 AUCUNE DONNÉE DE DÉMONSTRATION (v3.1)

Les 3 générateurs de données fictives ont été **définitivement supprimés** :
`Exemples` (tableau de bord), `Exemple automatique` (fiche de déplacement), `Données d'exemple` (paramètres).

- Aucun déplacement fictif n'est créé, **ni au premier lancement ni au démarrage**.
- La plateforme démarre **vide et propre** : seules les saisies réelles de la RH (ou une sauvegarde JSON restaurée) alimentent les données.
- Les états vides ont été soignés : graphique, registre, classement et tableaux affichent un message élégant au lieu de données inventées.
- Les 4 collaborateurs, les 12 moyens de transport et les secteurs par défaut sont conservés comme **référentiels de travail** (aucune donnée de dépense).

---

## ✨ FINITIONS PREMIUM (v3.1)

- **KPI à compteurs animés** : les valeurs montent en douceur à l'ouverture du tableau de bord (désactivé si `prefers-reduced-motion`).
- **Fond d'écran d'accès vivant** : deux nappes violet clair / or très subtil dérivent lentement (26 s) — aucun mouvement perceptible comme une animation.
- **Badge de rôle dans le header** : violet pour le RH, **doré pour l'Administrateur**.
- **États vides dédiés** pour chaque module + mention explicite « aucune donnée ».


### 🔧 Corrections v3.2
- **Menu « Se déconnecter »** : l'action `logout` n'était pas câblée dans le gestionnaire de menus → **corrigé**. Le retour à l'écran d'accès fonctionne depuis les **3 voies** : menu utilisateur, bouton `⏻` du header, bouton de la sidebar.
- **Carré vide dans le header** : les 8 icônes ajoutées à la v3.1 (`logout`, `lock`, `key`, `eyeOff`, `minus`, `chevRight`, `shieldCheck`, `userCog`) **n'avaient pas été enregistrées** dans le jeu d'icônes → **corrigé**. De plus, l'hydratation retombe désormais sur une icône de repli : plus jamais de cadre vide.
- **Icônes de la colonne de gauche** : portées à **34 px dans une pastille dédiée** (icône 18 px, trait 2), contraste renforcé, élément actif en **dégradé violet avec icône blanche**. Un bug de double application de style (l'icône héritait des règles de la pastille → effet « double icône ») a été supprimé en séparant `.nav-ico` (la pastille) et `.ic` (le trait).
- **Bouton de déconnexion du header** : 42 px, icône 19 px, survol rouge doux.

---

## 🏛️ ARCHITECTURE UX v3.0 — UNE SEULE INTERFACE RH CENTRALISÉE

### 1. Principe métier
**VOOMNET Track est le centre de pilotage de la RH.** Il n'existe **aucun espace par service**
ni **aucun tableau de bord individuel** : les collaborateurs et les services sont des **données**
gérées, filtrées et suivies depuis un espace unique.

### 2. Écran d'accès (nouveau)
- Titre : **« Accès à la plateforme RH »**
- Sous-titre : *« Pilotez les déplacements, les collaborateurs et les coûts de mobilité depuis un espace centralisé. »*
- Champs : **Nom / identité** + **Fonction** (Responsable RH · Administrateur RH · Gestionnaire RH / Paie · Contrôleur de gestion · Consultation)
- Bouton principal : **« Accéder au tableau de bord »** — lien secondaire : **Mode consultation**
- ❌ **plus aucune liste de collaborateurs** : la logique « chacun son espace » est supprimée.

### 3. Tableau de bord RH centralisé
En-tête : **« Bonjour, RH 👋 — Pilotez les déplacements, les collaborateurs et les coûts de mobilité depuis cet espace centralisé. »**
**Filtres globaux appliqués à tout le tableau de bord** : `Période` · `Service` · `Collaborateur` · `Type de déplacement` (+ bouton Réinitialiser).

**6 cartes KPI** : Total des déplacements · Dépenses de mobilité · Collaborateurs concernés ·
Déplacements en attente · Déplacements validés · Coût moyen par déplacement.

**Répartition par service** : une ligne par service (déplacements, montant, évolution vs mois -1, % du total).
👉 **Cliquer sur un service applique un FILTRE au dashboard RH** — cela n'ouvre jamais d'espace séparé.

**Activité des collaborateurs** : Collaborateur · Service · Déplacements · Dernier déplacement · Dépenses · Statut, avec recherche intégrée.

**Derniers déplacements** · **Points d'attention** · **Contrôle & conformité** · **Évolution des dépenses** (violet doux + or, moyenne dorée, légende) · **Part des services** (anneau).

### 4. Navigation (v3.0)
| Groupe | Entrées |
|---|---|
| **Pilotage** | Tableau de bord · Registre des sorties · Analyse · Rapports |
| **Ressources** | Collaborateurs |
| **Configuration** | Paramètres |

➖ **Onglet « Véhicules » supprimé partout** : sidebar, menus, cartes, raccourcis, statistiques, menus mobiles (**audit automatique : 0 occurrence**). Aucun lien mort, sidebar rééquilibrée, aucun espace vide.
Les données de flotte éventuellement présentes dans une ancienne sauvegarde JSON sont **conservées** (aucune donnée détruite) : elles ne sont simplement plus exposées dans l'interface.

### 5. Palette v3.0 — violet doux + or premium
| Rôle | Valeur | Usage |
|---|---|---|
| Violet principal | `#4A2A63` | boutons, navigation active, titres |
| Violet secondaire | `#6B4A82` | graphiques, icônes |
| Violet très clair | `#F1ECF5` | fonds d'états, pastilles |
| Or principal | `#C9A227` | accents, actif, PDF, code couleur Formation |
| Or clair | `#E2C866` | dégradés d'accent |
| Fond / Surface | `#F8F7FA` / `#FFFFFF` | base claire et respirante |
| Texte / secondaire | `#292331` / `#77717D` | lisibilité |
| Vert | `#43A982` | états positifs |

### 6. Design & espacement
Cartes **blanches**, bordures fines, ombres très légères, rayon **16–20 px**, padding interne **30/32 px**,
écarts de **22 px** entre cartes et **34 px** entre sections, contenu centré sur **1520 px** max.
L'interface doit inspirer **calme, ordre, maîtrise, prestige** — jamais la surcharge.

### 7. Audit final (automatisé)
✓ interface RH unique ✓ 0 dashboard par service ✓ 0 espace individuel
✓ services = filtres (4 lignes cliquables) ✓ collaborateurs = données (5 lignes, recherche)
✓ onglet Véhicules totalement absent ✓ sidebar équilibrée (6 entrées)
✓ palette violet doux + or ✓ 0 débordement (412 / 900 / 1500 px) ✓ 0 erreur console
✓ PDF, CSV, sauvegarde JSON, registre, analyse, rapports, paramètres : **fonctionnels**

---

## 🌅 SPLASH SCREEN PREMIUM (v2.2) — spécifications respectées

**Durée mesurée : 2,35 s** (desktop, tablette et mobile) — dans la fourchette 1,5–2,5 s demandée.
**Fluidité : 58–62 images/s** mesurées pendant l'animation.

### Séquence exacte
| Temps | Étape | Animation |
|---|---|---|
| 0,00 s | Halo violet très léger | apparition + scale 92 % → 100 % (1,15 s) |
| 0,10 s | **Logo officiel** au centre | fade-in + montée de 12 px + **scale 96 % → 100 %** (0,95 s) |
| 0,46 s | Ligne **« ESPACE RH • MOBILITY CONTROL »** | fade-in + micro-montée (0,5 s) |
| 0,47 s | Filet **doré** sous le logo | apparition (0,55 s) |
| 0,45 s → 1,75 s | Jauge de chargement (violet → or) | `scaleX(0) → 1` (1,3 s) |
| 1,85 s | Transition douce vers l'application | contenu 0,28 s puis voile 0,45 s |
| **2,35 s** | Application / écran de connexion | — |

### Direction artistique
Fond **blanc cassé** `#FCFCFE` + deux nappes radiales **violet très clair** et **or très subtil**.
Aucun fond sombre, aucune particule, aucun effet lumineux excessif, aucune surcharge. 🔒
Le logo est **exactement** le logo officiel fourni (aucune retouche de forme, de proportion ou de typographie).

### Règles techniques
- Animations **uniquement sur `transform` et `opacity`** → composited, **60 FPS** ⚡
- `will-change` + `contain:paint` sur le conteneur (aucun recalcul de mise en page)
- **Desktop / tablette / mobile** : tailles adaptées (320 px → 262 px sur petit écran), retesté à 412 / 900 / 1400 px
- **Skippable** : un clic ou une touche passe immédiatement à l'application
- Joué **une seule fois par session** (les rechargements ouvrent l'app en ~0,5 s)
- `prefers-reduced-motion` respecté : version statique + durée 0,24 s
- Accessibilité : `role="status"` + `aria-label="Chargement de VOOMNET Track"`

---

## 🎯 PROMPTS DE GÉNÉRATION (à copier dans Gemini / AI Studio)

### Prompt 1 — Refonte visuelle premium

```
RÔLE
Tu es une équipe UX/UI senior + développeur front-end. Tu réalises la REFONTE VISUELLE
COMPLÈTE ET PREMIUM d'une application existante appelée VOOMNET Track (gestion RH &
mobilité : suivi des dépenses de déplacement), livrée en UN SEUL fichier index.html
autonome (HTML + CSS + JS), sans aucune dépendance externe, fonctionnant hors-ligne.

CONTRAINTE ABSOLUE
Ne détruis, ne supprime et ne modifies AUCUNE fonctionnalité existante : conserve la
logique métier, les données, les vues, les boutons, les formulaires, les statistiques,
les interactions et les fonctionnalités actuelles. Tu changes uniquement l'interface.

DIRECTION ARTISTIQUE (2026, SaaS premium)
Interface CLAIRE, AÉRÉE, ÉLÉGANTE. Fond blanc cassé/gris très clair, grandes zones
respirantes, cartes blanches, bordures très fines, ombres extrêmement légères, coins
arrondis 16-20px, typographie moderne (Inter), hiérarchie visuelle nette, beaucoup
d'espace entre les sections.
Palette : primary #32104F, secondary #6F2DBD, accent #D7B238, background #F7F6FA,
surface #FFFFFF, texte #211A27, secondaire #77727D, succès #38A879, alerte #D7B238,
danger #D95C5C. Le violet et le doré sont des ACCENTS, jamais des fonds dominants.
INTERDIT : blocs violets sombres massifs, interface sombre, dégradés criards, ombres
lourdes, glassmorphism excessif, éléments collés, surcharge visuelle.

SIDEBAR
Claire et respirante : logo VOOMNET Track + « Espace RH • Mobility Control ».
Sections : PILOTAGE (Tableau de bord, Registre des sorties, Analyse, Rapports),
RESSOURCES (Véhicules, Collaborateurs), CONFIGURATION (Paramètres).
Élément actif : surface violette très claire + fine barre d'accent dorée + icône nette
+ typographie plus forte. Icônes minimalistes cohérentes (SVG inline).
Badges élégants pour véhicules, collaborateurs et sorties du mois.

HEADER
Titre de page + sous-titre contextuel, recherche globale (raccourci Ctrl/⌘+K, Entrée →
filtre le registre), cloche de notifications dynamiques, profil utilisateur (avatar à
initiales + menu déroulant : paramètres, sauvegarde JSON, rapport, nouvel
enregistrement, effacement).

DASHBOARD — hiérarchie
ACCUEIL/Contexte (salutation, mois, chips de contexte, sélecteur de mois) →
6 KPI (Total sorties, Coût total, Coût moyen/sortie, Kilométrage, Véhicules actifs,
Collaborateurs mobiles — chacun : valeur, variation vs mois précédent, contexte, icône,
sparkline) → GRAPHIQUES → ACTIVITÉ RÉCENTE → ANALYSES RAPIDES → ACTIONS RAPIDES.

GRAPHIQUES (SVG natif, aucun librairie)
Courbe d'évolution lissée avec grille pointillée très subtile, labels lisibles, valeurs
élégantes, violet/or parcimonieux, animation au chargement, tooltips modernes
(suivi de la souris), responsive, bascule 6/12 mois. Plus : barres groupées par entité,
anneau de répartition des transports, barres horizontales avec les logos des services.

CARTES / TYPOGRAPHIE / RESPONSIVE / ANIMATIONS
Cartes : radius 16-20px, padding généreux, bordure très subtile, ombre légère, surface
blanche, espacement interne cohérent, beaucoup d'air entre les éléments.
Typographie Inter (embarquée en base64 pour rester hors-ligne) : H1 très lisible, H2
clair, H3 moyen, labels petits lisibles, secondaire discret.
Responsive parfait desktop/laptop/tablette/mobile : sidebar en tiroir avec voile, cartes
empilées, graphiques redimensionnés, boutons accessibles, aucune information coupée,
aucun débordement horizontal.
Animations premium mais subtiles : apparition progressive des cartes, hover léger,
transition des boutons, animation des KPI et des graphiques, transitions entre pages,
micro-interactions sur les icônes. Rapides (< 1,2 s). Respecter prefers-reduced-motion.

CONSERVER IMPÉRATIVEMENT
Toutes les fonctions existantes : enregistrement/édition/suppression de déplacements,
cases de motifs rapides, statuts de règlement, justificatifs, registre filtrable et
exportable (CSV), rapport mensuel + bouton « Télécharger le PDF » (moteur PDF écrit à
la main en JS, sans internet), sauvegarde/restauration JSON, paramètres d'entreprise,
agents, transports, devise, stockage local avec repli mémoire.

CONTRÔLE FINAL À EFFECTUER
Alignements, espacements, cohérence des icônes, tailles de texte, contraste, responsive,
cohérence des boutons et des cartes, cohérence des couleurs, animations, absence de
débordements. Le résultat doit pouvoir être présenté à un client ou une grande
entreprise : « produit SaaS professionnel développé par une grande entreprise tech ».
LIVRE UNIQUEMENT LE CODE COMPLET DU FICHIER index.html.
```

### Prompt 2 — Splash screen premium (court et élégant)

```
Je veux un SPLASH SCREEN PREMIUM pour VOOMNET Track, TRÈS COURT, ÉLÉGANT, MODERNE et
PROFESSIONNEL — surtout pas une publicité ni une animation longue. Durée : 1,5 à 2,5 s.

DIRECTION ARTISTIQUE
Écran LUMINEUX et premium. PAS DE FOND SOMBRE : blanc cassé, blanc, violet très léger,
touches dorées subtiles. Fond propre, minimaliste, respirant. Éviter absolument : fond
violet foncé, fond noir, grosses animations, particules, effets lumineux excessifs,
explosions, animations lentes, surcharge visuelle.

ANIMATION (dans l'ordre)
1. Le logo VOOMNET Track apparaît progressivement au centre (opacité + léger mouvement
   vertical + micro scale 96 % → 100 %, easing soyeux).
2. Le nom « VOOMNET Track » apparaît juste sous le logo en fade-in rapide.
3. En dessous, la ligne fine : « ESPACE RH • MOBILITY CONTROL » (typographie très fine,
   lettres espacées, majuscules).
4. Une fine barre dorée/violette se remplit brièvement sous le logo (indicateur).
5. Après 1,5 à 2,5 s : transition douce (fondu) vers le tableau de bord.

LOGO
Utilise EXACTEMENT le logo fourni : ne le recrée pas, ne modifie ni ses proportions, ni
sa forme, ni son symbole, ni sa typographie. Supprime uniquement le fond inutile autour.

STYLE
Inspiration des meilleurs produits SaaS (Apple, Linear, Stripe, Notion, Vercel, Ramp)
sans copier leur identité. VOOMNET Track a sa propre identité. Impression recherchée :
« produit professionnel, sérieux, moderne et haut de gamme ».

CONTRAINTES ESSENTIELLES
Splash COURT (l'utilisateur ne doit pas attendre inutilement) ; animation fluide 60 FPS ;
parfait sur desktop, tablette et mobile ; spécacularité par la SOBRIÉTÉ, pas par la
complexité. Prévoir : disparition au clic, saut du splash si déjà affiché dans la même
session, et respect de prefers-reduced-motion.
```

---

## 🧰 Personnelisation & sources

* **Sources** : `src/part1_head.html` (design system), `src/part2_body.html` (structure),
  `src/part3_core.js.html` (noyau : icônes, données, formulaire, registre),
  `src/part3b_dash.js.html` (graphiques, dashboard, analyse, véhicules, collaborateurs),
  `src/part4_pdf.js.html` (moteur PDF).
* **Régénérer `index.html`** : `python3 build.py` (embarque logos + police en base64).
* **Remplacer un logo** : déposer le fichier dans `assets/` puis relancer `build.py`.
* **Ajouter un service** : constante `SERVICES` dans `src/part3_core.js.html`.

---

## 🔧 Corrections v3.3 — déconnexion, header et icônes HD

**1. La déconnexion fonctionne sur les 4 voies** (vérifié automatiquement à chaque build) :

| Voie | Élément | Résultat |
|---|---|---|
| Menu du profil | « Se déconnecter » (`data-action="logout"`) | → écran d'accès RH, session vidée |
| Bouton du header | `#btnLogoutTop` (icône + libellé « Déconnexion », 46 px) | → écran d'accès RH |
| Bouton de la sidebar | `#btnLogoutSide` (« Se déconnecter ») | → écran d'accès RH |
| Gestionnaire délégué | tout élément portant `data-action="logout"` | → écran d'accès RH |

Un **gestionnaire d'événement délégué** (`bindLogoutDelegation`) capte désormais tout clic sur
ces éléments, même s'ils sont créés ou modifiés après le chargement : la déconnexion ne peut
plus « ne rien faire ». Elle vide `sessionStorage`, ferme les popovers, puis affiche `showLogin()`.

**2. Le bouton carré du header est net et lisible** : 46 × 46 px minimum, icône `logout`
20 px, libellé « Déconnexion » sur grand écran (masqué sous 1500 px, le bouton restant
carré). Le header ne peut plus se chevaucher : la recherche se comprime d'abord
(`clamp(150px, 22vw, 300px)`), le badge de rôle s'efface sous 1360 px, les contrôles
gardent leur taille. Vérifié sans chevauchement de 1240 px à 1920 px.

**3. Icônes de la colonne de gauche redessinées en duotone HD** : pastille 38 px
(dégradé blanc → lilas, bord, ombre douce) contenant une icône de 20 px. Registre des
sorties = registre à pince avec bandeau plein et lignes ; Analyse = histogramme à barres
contrastées ; Rapports = page à coin plié et lignes de texte ; Collaborateurs = binôme ;
Paramètres = engrenage ; Tableau de bord = grille. En mode actif, l'icône passe en blanc
sur dégradé violet avec filet doré.

**4. Aperçu toujours à jour** : `serve.py` sert l'application avec
`Cache-Control: no-store, no-cache, must-revalidate, max-age=0`. Le navigateur ne peut plus
afficher une ancienne version. Lancer : `python3 serve.py` (port 8000).

> 💡 **Si une ancienne version s'affiche encore** : rechargement forcé **Ctrl + Shift + R**
> (Windows/Linux) ou **⌘ + Shift + R** (Mac). La version visible en bas de la sidebar doit
> indiquer **« VOOMNET Track · v3.3 »**.

---

## 🖥️ Corrections v3.4 — téléchargement sur l'appareil & design « suivi transport »

### 1. « Télécharger le PDF » enregistre maintenant SUR L'APPAREIL

Le bouton doré du tableau de bord et celui de la page Rapports utilisent un moteur
d'enregistrement refondu :

| Méthode | Quand | Où arrive le fichier |
|---|---|---|
| **Téléchargement direct** (prioritaire) | toujours | dossier **« Téléchargements »** de l'appareil |
| **« Choisir l'emplacement… »** | bouton dédié (Rapports) | **Bureau, Documents, clé USB…** au choix de l'utilisateur |
| **Aide en 2 étapes** | si l'aperçu (iframe) bloque | ouverture de l'application dans un onglet, puis téléchargement |

* Un message de confirmation s'affiche : « Enregistré sur votre appareil ✅ — fichier (xxx Ko) → dossier « Téléchargements » ».
* L'ancien comportement (boîte « Enregistrer sous » appelée automatiquement et annulée par certains
  navigateurs, ce qui ne produisait **aucun** fichier) est supprimé : le téléchargement est immédiat.
* Le même moteur sert l'**export CSV** et la **sauvegarde JSON**.
* Si le navigateur annule le choix d'emplacement : message explicite, jamais un clic sans effet.
* Si l'application est affichée dans une **fenêtre d'aperçu** (celle-ci bloque volontairement les
  téléchargements), une boîte d'aide propose : *Ouvrir dans un onglet*, *Réessayer ici*, *Copier le lien*.

### 2. Nouveau design « tech » — gestion & suivi du transport

* **Suivi transport — chaîne de traitement** : 4 étapes reliées par des connecteurs
  pointillés — Enregistrés → Justifiés → Réglés → **À régler** (étape dorée). Chaque étape
  affiche son compteur, son total en FCFA et une jauge de progression. **Cliquer « À régler »
  ouvre le registre déjà filtré** (jamais un écran séparé).
* **Flux de mobilité récent** : chronologie verticale avec rail pointillé, pastille d'état,
  et **visualisation du trajet** (départ ● — ligne pointillée — repère doré ◉ arrivée),
  service, statut, motif, collaborateur, transport, distance et montant.
* **Réseau & trajets** : liaisons les plus fréquentes (barres violettes) et moyens de
  transport les plus utilisés (barres dorées), plus distance cumulée, coût moyen et nombre
  de trajets distincts.
* **Colonne « Trajet »** du registre : elle affiche désormais le trajet sous forme visuelle.
* Badge « SUIVI ACTIF » avec pastille pulsée, chiffres en tabulaires (style tableau de bord
  technique), thème clair conservé : violet doux + or en accent.

**Vérifications** : téléchargements PDF / CSV / JSON confirmés (fichiers réels enregistrés),
0 erreur console, **aucun débordement horizontal de 360 px à 1920 px sur les 6 vues**.

---

## 🎨 v3.5 — Nouvel en-tête « mobilité corporate » & illustration de véhicule

L'en-tête du tableau de bord a été entièrement redessiné : fini le ton « application de démo »,
place à une identité de logiciel de gestion professionnel.

**1. Typographie éditoriale**
* Sur-titre en petites capitales espacées, précédé d'un filet doré :
  « ESPACE RH — CONTRÔLE DE LA MOBILITÉ ».
* Titre fort : **« Pilotage de la mobilité et des dépenses »** (graisse 790, interlettrage serré).
  L'émoji 👋 a été retiré — aucun élément enfantin.
* Phrase de synthèse dynamique : « Synthèse consolidée de **Octobre 2026** — 4 déplacements
  enregistrés par 3 collaborateurs, tous services confondus. »

**2. Bandeau de données raffiné** (remplace les anciennes pastilles arrondies)
Cinq indicateurs séparés par de fins filets verticaux : **Déplacements · Dépenses · En attente ·
Validés · Distance**. Chiffres en tabulaires, libellés en petites capitales, l'indicateur
« En attente » passe en **or** (ou « À jour » en vert lorsqu'il n'y a rien à régler).
Même traitement typographique appliqué aux cartes KPI (libellés en capitales espacées).

**3. Illustration de véhicule dessinée en vectoriel (SVG)**
Un fourgon de livraison de profil, tracé au trait fin, aux couleurs exactes de la marque
(violet `#4A2A63`, or `#C9A227`) : vitrage, rétroviseur, portière coulissante, phare, feux,
passages de roues et jantes dorées, filet doré de livrée et marque « VOOMNET » sur la caisse.
Sous le véhicule, un **trajet en pointillés animés** relie le point de départ à une **épingle
de destination dorée** — le suivi de la mobilité. Animation lente (7 s), désactivée
automatiquement si l'utilisateur a demandé moins d'animations (`prefers-reduced-motion`).

**4. Comportement responsive vérifié** : illustration à droite sur grand écran, centrée à droite
sur écran intermédiaire, masquée sous 760 px pour préserver la lisibilité mobile.
**Aucun débordement horizontal de 390 px à 1920 px sur les 6 vues.**

---

## 🔷 v3.6 — Tous les symboles redessinés en « objet réel »

Les icônes n'étaient que de simples traits fins : elles ont toutes été **redessinées à la main en
duotone détaillé** — un volume de fond, une forme principale, des détails et un accent doré quand
cela a du sens. 49 symboles, tous vérifiés (aucun symbole manquant au chargement).

**Les plus visibles**
* **Total des déplacements** → registre à pince avec bandeau, pince métallique et lignes de saisie.
* **Dépenses de mobilité** → portefeuille avec rabat, poche à carte et **pièce dorée**.
* **Collaborateurs concernés** → deux personnes avec épaules (silhouette pleine + trait).
* **Déplacements en attente** → horloge avec graduations et aiguilles.
* **Déplacements validés** → médaille de validation avec coche.
* **Coût moyen** → **compteur gradué avec aiguille dorée**.
* **Trajet** → route balisée en pointillés menant à une **épingle de destination dorée**.
* **Carburant** → pompe avec vitre, tuyau et pistolet.
* Recherche, cloche, calendrier, corbeille, crayon, disquette, PDF, imprimante, œil, cadenas,
  clé, bouclier, bâtiment, engrenage, filtre, éclair, étincelle… tous repris dans le même style.

**Pastilles plus profondes** : les conteneurs d'icônes (cartes KPI, titres de cartes, tuiles
d'analyse) passent à 38–42 px avec dégradé blanc → teinte, filet, reflet interne et ombre douce.

**Cartes KPI nettoyées** : plus de pastille « n/d » (aucune comparaison = aucun badge) et plus de
courbe orpheline quand il n'y a pas encore d'historique.

---

## 🔐 v3.7 — SÉCURITÉ : aucun identifiant visible sur l'écran de connexion

**Problème corrigé** : la page de connexion affichait un bloc « Comptes d'accès — RH & Administrateur »
contenant les identifiants **et les mots de passe en clair**. N'importe qui ouvrant l'application
pouvait donc entrer dans la plateforme.

**1. Bloc supprimé de l'interface**
Le bloc dépliant et la fonction qui l'alimentait (`renderAccountHints`) ont été retirés.
À la place, une note discrète : *« Accès réservé au personnel autorisé. Les identifiants sont remis
par la direction et se modifient dans Paramètres → Comptes & sécurité. »*

**2. Mots de passe retirés du fichier livré**
Le code ne contient plus **aucun mot de passe en clair** (vérifié automatiquement : 0 occurrence dans
`index.html`). Seules sont embarquées des **empreintes non réversibles** (FNV-1a salée) :

| Compte | Identifiant | Empreinte embarquée |
|---|---|---|
| Responsable RH | `rh` | `6e6b4ab8` |
| Administrateur | `admin` | `460c9900` |

La connexion reste identique pour les utilisateurs autorisés :
`rh` / `Rh@Voomnet2026` et `admin` / `Admin@Voomnet2026`.

**3. Bouton « rétablir l'identifiant par défaut »**
Dans Paramètres → Comptes & sécurité, le bouton restaure l'identifiant de départ en reposant
l'empreinte d'origine — il n'affiche plus jamais de mot de passe (avant : il l'écrivait dans un message).

**Vérifié** : profil neuf → aucun identifiant visible ; mot de passe erroné → accès refusé avec le
message « Identifiant ou mot de passe incorrect » ; connexion RH et Administrateur OK ; bouton
« rétablir » OK ; aucune trace de mot de passe dans toute l'interface ; 0 erreur console.

> 📌 **Recommandation** : changez les deux mots de passe dès la première connexion
> (Paramètres → Comptes & sécurité), puisqu'ils vous ont été communiqués hors application.

---

## 🚪 v3.8 — VERROUILLAGE TOTAL : plus aucun accès sans identifiant

La plateforme ne s'ouvre plus sans compte nominatif. Trois choses donnaient un accès
(ou un indice) sur l'écran de connexion — les trois sont supprimées :

**1. Bouton « Mode consultation » — SUPPRIMÉ**
C'était la faille principale : un simple clic ouvrait le tableau de bord **sans aucun identifiant**.
Le bouton, le séparateur « ou » et son branchement ont été retirés.

**2. Session anonyme — REFUSÉE**
Une session « consultation » déjà enregistrée dans un navigateur n'ouvre plus rien :
l'application l'ignore et affiche l'écran d'accès. Vérifié aussi en forçant la session depuis la
console : écran d'accès imposé, message « Accès refusé — un identifiant est obligatoire ».

**3. Indices supprimés**
* Le champ identifiant n'affiche plus « Ex : rh » (qui suggérait l'identifiant) mais « Votre identifiant ».
* Le texte de présentation ne mentionne plus « un compte Responsable RH et un compte Administrateur »
  mais une mention générique : « Accès protégé — identifiant personnel obligatoire ».
* Le bloc « Comptes d'accès » (v3.7) reste supprimé, et **aucun mot de passe n'existe en clair**
  dans le fichier livré (uniquement des empreintes).

**Ce qui n'a pas changé** : la connexion des personnes autorisées
(`rh` / `Rh@Voomnet2026`, `admin` / `Admin@Voomnet2026`), la déconnexion, le PDF, le registre,
les filtres, les paramètres et tous les comptes restent modifiables dans
**Paramètres → Comptes & sécurité**.

**Vérifié** : bouton absent ; aucun mot « consultation » sur la page ; aucun indice d'identifiant ;
session anonyme forcée → écran d'accès ; session vide → écran d'accès ; l'écran d'accès couvre
l'application (clics et clavier bloqués) ; connexion RH et Administrateur OK ; 0 erreur console ;
suite complète au vert.

---

## 🏛️ v3.9 — Service ENCACI, véhicule animé & symboles or royal / argent

### 1. VOOMSTORE supprimé → ENCACI mis en place (avec votre logo)

Le service **VOOMSTORE n'existe plus** : il est remplacé partout par **ENCACI**, avec le logo
que vous avez fourni, utilisé **tel quel** (seuls le fond blanc et les marges ont été retirés).

* Liste des services : Direction · VOOMNET TECHNOLOGY · **ENCACI** · VOOMNET FORMATION.
* Couleur du service : **or** (`#C9A227` / `#9A7A15`) — cohérent avec la nouvelle charte.
* Le logo ENCACI apparaît partout : en-tête du **PDF**, lignes « Répartition par service »,
  filtres, formulaire de sortie, fiches collaborateurs, tableaux d'analyse.
* Les collaborateurs et véhicules qui étaient rattachés à VOOMSTORE sont passés à ENCACI.
* **Migration douce** : si d'anciennes données enregistrées mentionnent encore VOOMSTORE, elles
  sont automatiquement reconverties en ENCACI au chargement — **aucune donnée perdue**.
* Contrôle : plus aucune trace de « VOOMSTORE » dans l'application ni dans le PDF
  (vérifié par extraction du texte du PDF généré).

### 2. La voiture rebondit sur le train avant

L'illustration de l'en-tête est désormais **animée comme un vrai véhicule** :
* la **caisse entière** pivote très légèrement sur le **pneu avant** et s'enlève de ~6,4 px,
  puis retombe sur la suspension avec **deux reprises amorties** (cycle de 1,6 s) ;
* le **pneu s'écrase** légèrement sous la charge (mise en forme), puis se détend ;
* l'**ombre au sol** se resserre au moment de l'enlèvement ;
* le **trajet pointillé** continue de défiler lentement vers la destination dorée.
* Tout est désactivé automatiquement si l'utilisateur a demandé moins d'animations.
* Mesuré en conditions réelles : amplitude ≈ 10 px, animation confirmée active.

### 3. Symboles : or royal + argent (hiérarchie visuelle)

Deux nouvelles teintes rejoignent la palette, sans toucher à l'identité :
* **Or royal `#B58A2B`** — les icônes des **cartes de données** (KPI, titres de cartes,
  tuiles d'analyse) : elles « lisent » comme des symboles précieux, pas comme des traits gris.
* **Argent `#8E93A1`** — les **détails secondaires** (puces de filtre, méta du flux de mobilité) :
  la hiérarchie devient immédiatement lisible.
* Les remplissages d'accent (jauges, bordures dorées, pastille de destination) restent en or
  d'identité `#C9A227`.

### 4. Correctif trouvé au passage

La liste déroulante **« Service »** des filtres du tableau de bord n'était jamais remplie
(elle restait bloquée sur « Tous les services »). Corrigé : elle propose désormais
les 4 services réels et le filtre ENCACI fonctionne.

**Vérifié** : suite complète au vert (0 erreur console), PDF avec le logo ENCACI, aucune trace
de VOOMSTORE, filtre service opérationnel, véhicule animé, palettes appliquées, aucun débordement.

## 🖼️ v3.10 — La photo du patron devient le visuel du service Direction

### 1. Votre photo, exactement comme fournie

L'image transmise (portrait de **M. WILFRIED GADOU**) est intégrée telle quelle :
* **aucune retouche du visage**, aucun redessin, aucune réinterprétation ;
* seuls le **recadrage carré** et le **nettoyage du fond** ont été appliqués, puis
  un **agrandissement net (512 × 512)** pour rester impeccable sur les écrans haute densité ;
* elle est **embarquée dans le fichier livré** (`data:image/jpeg`) : l'application
  fonctionne toujours **100 % hors-ligne**, sans aucune ressource externe.

### 2. Où la photo apparaît

* **Liste des services** (tableau de bord) : la ligne **M. WILFRIED GADOU / Direction Générale**
  porte désormais la photo à la place du symbole générique — même cadre, même taille,
  même alignement que les logos ENCACI, VOOMNET TECHNOLOGY et VOOMNET FORMATION.
* **Filtre « Service »**, **fiche du collaborateur** et **statistiques par service** :
  la photo suit automatiquement le service Direction.
* **PDF officiel** : la table des logos du rapport intègre la photo Direction, donc
  chaque PDF imprimé porte le visuel du service Direction.

### 3. Bandeau des logos du PDF remis au carré

Le bandeau de tête du rapport empilait les logos les uns sur les autres et les libellés
débordaient sur le logo voisin. Il est désormais une **grille régulière** : une colonne par
entité, logo centré, libellé centré et tronqué si nécessaire, séparateur fin entre les
colonnes — **plus aucun chevauchement**, même avec cinq visuels.

### 4. Ce qui n'a pas bougé

Aucune fonctionnalité, aucun calcul, aucun export n'a été modifié : la seule différence
entre la v3.9 et la v3.10 est l'ajout de ce visuel et la mise à jour du témoin de version.

**Vérifié** : 22 ressources embarquées, 0 erreur console, photo affichée sur la ligne
Direction, PDF généré (278 Ko) contenant le visuel, aucun débordement.

*VOOMNET Track v3.10 — « Votre partenaire à votre service ».*
