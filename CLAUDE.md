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
- `tools/check_site.py` — vérifications structurelles. À lancer après toute
  modification : `python tools/check_site.py`.
- `assets/cv.pdf`, `assets/book.pdf` — documents téléchargeables. **Fournis par
  Alexandre**, jamais générés ici. Les noms de fichiers sont fixes : pour publier une
  nouvelle version, on remplace le fichier, on ne renomme pas.
- `assets/img/` — photos des projets, référencées depuis les 5 pages.
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

- Langue du site : **français**, avec les apostrophes typographiques (`’` dans les
  sources d'origine ; l'ASCII `'` est utilisé dans le HTML pour rester simple).
- Structure de `index.html` : une `<section id="...">` par bloc, chacune reprise
  dans le sommaire de la sidebar (`.side-nav`) — ajouter une section implique
  d'ajouter son lien de sommaire.
- Les couleurs passent par les variables CSS de `:root` (`--bleu`, `--bleu-fonce`,
  `--vert`…). Ne pas coder de couleur en dur.
- Les cartes projet utilisent `.carte` ; le chiffre de résultat en vert est
  `.resultat` et doit rester factuel (unités produites, taux de SAV…).
- Responsive : un seul point de rupture, `@media (max-width:980px)`, qui fait
  passer la sidebar en bandeau horizontal et les grilles en une colonne.

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
   des `title`s, la présence de meta description, et l'identité du menu entre les 5
   pages.
2. Vérifier visuellement le rendu des 5 pages en desktop et en mobile 375 px — seul
   point que le script ne couvre pas.
