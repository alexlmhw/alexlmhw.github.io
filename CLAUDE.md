# CLAUDE.md

## Le projet

Site vitrine personnel d'Alexandre Lemaire, ingénieur électronique senior.
Hébergé par GitHub Pages sur https://alexlmhw.github.io — la branche `main` est
publiée telle quelle, sans build ni générateur de site.

## Structure

- `index.html` — **tout le site**. Page unique, CSS inline dans un `<style>`,
  aucune dépendance JS. La seule ressource externe est la police Lato (Google Fonts).
- `assets/cv.pdf`, `assets/book.pdf` — documents téléchargeables. **Fournis par
  Alexandre**, jamais générés ici. Les noms de fichiers sont fixes : pour publier une
  nouvelle version, on remplace le fichier, on ne renomme pas.
- `assets/img/` — photos des projets, référencées depuis `index.html`.
- `Input/` — **gitignoré**. Sources de travail d'Alexandre (CV `.docx`, book `.pptx`).
  C'est la référence de contenu : le site doit refléter le CV le plus récent qui s'y
  trouve. Ne jamais committer ce dossier.

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

Pas de tests ni de build. Après modification :

1. Ouvrir `index.html` dans un navigateur, vérifier desktop et mobile.
2. Vérifier que chaque `src`/`href` vers `assets/` pointe vers un fichier existant.
3. Vérifier que chaque ancre `#...` du sommaire correspond à une section.
