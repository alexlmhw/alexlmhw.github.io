# CLAUDE.md

## Le projet

Site vitrine personnel d'Alexandre Lemaire, ingénieur électronique senior.
Hébergé par GitHub Pages sur https://alexlmhw.github.io — la branche `main` est
publiée telle quelle, sans build ni générateur de site.

## Structure

- `index.html` — accueil. Contenu complet : réalisations, prototypes, parcours,
  formation, compétences, téléchargements.
- `bugali.html`, `monimalz.html`, `fer-a-fileter.html`, `outils.html` — pages de
  détail. Elles partagent le gabarit de `outils.html` (head, sidebar, footer).
- `assets/style.css` — **tous** les styles, partagés par les 5 pages. Aucun
  `<style>` inline ne doit réapparaître dans une page.
- `404.html` — page servie par GitHub Pages pour toute adresse inconnue. Même
  gabarit que les pages de détail, mais **aucune entrée de menu marquée active**
  (elle ne figure pas dans le menu) et un `<meta name="robots" content="noindex">`.
  `check_site.py` la traite via `PAGES_SANS_ENTREE_MENU`.
- Les `<img>` portent des attributs `width`/`height` égaux aux dimensions réelles
  du fichier : ils donnent son ratio au navigateur avant chargement et évitent que
  la page sursaute. La règle globale `img{height:auto}` empêche toute déformation.
- `tools/check_site.py` — vérifications structurelles. À lancer après toute
  modification : `python tools/check_site.py`.
- `assets/cv.pdf`, `assets/book.pdf` — documents téléchargeables. **Fournis par
  Alexandre**, jamais générés ici. Les noms de fichiers sont fixes : pour publier une
  nouvelle version, on remplace le fichier, on ne renomme pas.
- `assets/img/` — photos des projets, référencées depuis les 5 pages.
- `assets/img/partage.jpg` — **image d'aperçu au partage** (Open Graph), 1200×630.
  C'est elle qui s'affiche quand le lien est posté sur LinkedIn, Slack ou envoyé par
  mail. Générée à partir de `bugali.jpg`, sans recadrage. Pour la remplacer, garder
  le format 1200×630 et le même nom de fichier.
- `favicon.ico` (racine) et `assets/img/apple-touch-icon.png` — icônes d'onglet.
- `Input/` — **gitignoré**. Sources de travail d'Alexandre (CV `.docx`, book `.pptx`).
  C'est la référence de contenu : le site doit refléter le CV le plus récent qui s'y
  trouve. Ne jamais committer ce dossier.

## Le menu est dupliqué — règle impérative

Le site est en HTML pur, sans générateur : le menu existe en **5 exemplaires
identiques**, délimités par `<!-- MENU:DEBUT -->` et `<!-- MENU:FIN -->`.

**Ajouter, renommer ou retirer une entrée de menu impose de modifier les 5
fichiers :** `index.html`, `bugali.html`, `monimalz.html`, `fer-a-fileter.html`,
`outils.html`.

Seule différence autorisée entre les cinq : le `class="actif"` sur le lien de la
page courante. `tools/check_site.py` vérifie cette identité et échoue sinon.

## Conventions

- Langue du site : **français**, avec les apostrophes typographiques `’` partout
  dans le texte visible et dans les attributs porteurs de texte (`alt`, `title`,
  `aria-label`, `content`). L'apostrophe ASCII `'` ne doit plus apparaître dans le
  HTML des 5 pages — elle reste normale dans le code (`tools/check_site.py`) et
  dans ce fichier. En rédigeant une nouvelle page, écrire directement `’`.
- **Aucun tiret cadratin `—`** dans les 5 pages ni dans `404.html` : ni dans le
  texte visible, ni dans les attributs porteurs de texte. Selon le rôle qu'il
  jouait, écrire `·` (titre, nom de projet, entrée de menu : « Bugali · console »),
  `:` (étiquette de liste : « <b>Conception</b> : protos complets… ») ou une simple
  virgule (incise en pleine phrase). Attention à ne pas créer ainsi un second `:`
  dans la même phrase. Le tiret demi-cadratin `–` reste, lui, en place pour les
  plages de dates (« 2019 – 2021 »). `tools/check_site.py` échoue si un `—`
  réapparaît ; il reste normal dans le code et dans ce fichier.
- Structure de `index.html` : une `<section id="...">` par bloc. La plupart sont
  reprises dans la liste d'ancres de la sidebar (`.side-nav`) — ajouter une section
  de contenu implique en général d'ajouter son lien. Exceptions : `#haut` (le hero)
  et `#cequejefais` n'ont pas de lien dédié, la liste commence à `#realisations`.
- **Sur l'accueil, `.side-nav` est imbriqué dans le menu, juste sous « Accueil »**,
  en retrait derrière un filet : une seule rubrique de navigation, les 5 pages en
  gras et les sections de l'accueil en secondaire sous la première. Il n'y a pas de
  titre « Sommaire » séparé. Les 4 pages de détail n'ont pas ce sous-bloc.
- Ce sous-bloc est **le seul écart autorisé** entre les 5 copies du menu. Il doit
  être encadré par `<!-- SOUS-MENU:DEBUT -->` et `<!-- SOUS-MENU:FIN -->` :
  `check_site.py` le retire avant de comparer les menus. Tout ce qui est en dehors
  de ces marqueurs, à l'intérieur de `MENU:DEBUT`/`MENU:FIN`, doit rester
  strictement identique sur les 5 pages.
- Les couleurs passent par les variables CSS de `:root` (`--bleu`, `--bleu-fonce`,
  `--vert`…). Ne pas coder de couleur en dur.
- Les cartes projet utilisent `.carte` ; le chiffre de résultat en vert est
  `.resultat` et doit rester factuel (unités produites, taux de SAV…).
- **La sidebar est en deux morceaux**, et c'est volontaire : `<aside class="sidebar">`
  (photo, nom, menu) avant `<main>`, et `<aside class="sidebar-bas">` (contact,
  téléchargements) **après** `</main>`. La grille `.page` les replace par zones :
  côte à côte dans la colonne gauche en desktop, mais en mobile le bloc du bas
  passe sous le contenu. Sans ça, la sidebar mangeait tout le premier écran d'un
  téléphone (703 px sur 812) et le titre n'apparaissait qu'après défilement.
- Le fond coloré de la colonne gauche et son filet sont peints par un dégradé sur
  `.page`, pas par les deux `<aside>` : sinon il aurait fallu les étirer sur toute
  la hauteur de la page, ce qui replaçait le contact tout en bas.
- Responsive : un seul point de rupture, `@media (max-width:980px)`, qui fait
  passer la sidebar en bandeau horizontal et les grilles en une colonne.

## Partage et accessibilité — à ne pas casser

Chaque page porte, en plus de son `<title>` et de sa `meta description` :

- un bloc **Open Graph** (`og:title`, `og:description`, `og:url`, `og:image`) et un
  `rel="canonical"`. Sans lui, un lien partagé sur LinkedIn s'affiche en URL nue.
  `og:url` et `og:image` sont les **seules URL absolues** autorisées du site.
- un **lien d'évitement** `<a class="saut" href="#contenu">` en tout début de
  `<body>`, et l'ancre correspondante `<main id="contenu">`.
- une **hiérarchie de titres continue** : pas de saut `h1 → h3`. Les libellés
  « Rôle / Équipe / Stack » des pages de détail sont des `<h2>` stylés petits par
  `.meta-bloc h2`, et non des `<h4>`.

`check_site.py` vérifie ces trois points sur les 5 pages. Une nouvelle page qui les
oublie fait échouer la vérification.

## Règles de contenu

- **Ne pas inventer de liens externes ni de chiffres.** Tout ce qui est publié doit
  venir du CV ou du book dans `Input/`. En cas de doute sur une URL, ne pas mettre
  de lien.
- Pas de noms de tiers sur le site public : les références (anciens collègues)
  figurent dans le CV et le book, volontairement pas sur la page.
- La liquidation de Bugali est mentionnée dans le CV mais **pas** sur le site ; la
  période 2025–2026 s'y intitule simplement « Indépendant ».

## Vérification

Après toute modification :

1. `python tools/check_site.py` — vérifie automatiquement : les 5 pages
   attendues, les liens internes (`src`/`href` vers `assets/`), les ancres, l'unicité
   des `title`s, la présence de meta description, l'absence d'apostrophe droite
   et de tiret cadratin, et l'identité du menu entre les 5 pages.
2. Vérifier visuellement le rendu des 5 pages en desktop et en mobile 375 px — seul
   point que le script ne couvre pas.
