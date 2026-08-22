# Site vitrine — Alexandre Lemaire

Site statique (un seul fichier HTML + un dossier d'assets), sans framework ni build. Il suffit de le déposer sur n'importe quel hébergeur statique.

## Structure

```
site/
├── index.html                          ← la page (design + contenu)
└── assets/
    ├── cv.pdf                          ← bouton « CV (PDF) »
    ├── book.pdf                        ← bouton « Book · Portfolio (PDF) »
    ├── cv-ats.pdf                      ← bouton « CV ATS (PDF) »
    ├── CV_ATS_Alexandre_Lemaire.docx   ← bouton « DOCX » du CV ATS
    └── img/                            ← photos des projets
```

## Mettre à jour les fichiers téléchargeables

Les boutons pointent vers des **noms de fichiers fixes**. Pour mettre à jour un document, il suffit de **remplacer le fichier par un nouveau portant le même nom** — aucun besoin de toucher au HTML :

- Nouveau CV → exporter en PDF et l'enregistrer sous `assets/cv.pdf`
- Nouveau book → exporter le PowerPoint en PDF et l'enregistrer sous `assets/book.pdf`
- Nouveau CV ATS → `assets/cv-ats.pdf` (et `assets/CV_ATS_Alexandre_Lemaire.docx` pour la version Word)

Puis re-déployer (glisser-déposer sur Netlify, ou `git push` pour GitHub Pages).

## Déployer

### Option A — Netlify Drop (le plus simple, 2 minutes, gratuit)

1. Aller sur https://app.netlify.com/drop
2. Glisser-déposer le dossier `site/` entier dans la page
3. C'est en ligne. Créer un compte (gratuit) pour garder l'URL et pouvoir re-déployer plus tard. L'URL peut être personnalisée (ex. `alexandre-lemaire.netlify.app`) dans *Site settings → Change site name*.

### Option B — GitHub Pages (gratuit, pratique avec ton compte GitHub)

1. Créer un dépôt sur https://github.com/new — par exemple `alexlmhw.github.io` (le site sera alors à `https://alexlmhw.github.io`), public.
2. Uploader le **contenu** du dossier `site/` à la racine du dépôt (bouton *Add file → Upload files* : glisser `index.html`, le dossier `assets`).
3. Dans *Settings → Pages*, vérifier que la source est `main` / racine. Le site est en ligne au bout d'une à deux minutes.
4. Pour une mise à jour : remplacer le fichier concerné dans le dépôt (re-upload), c'est tout.

### Domaine personnalisé (optionnel)

Un domaine comme `alexandre-lemaire.fr` (~7 €/an chez OVH, Gandi…) peut être branché sur Netlify comme sur GitHub Pages via leurs réglages *Custom domain*.

## Notes

- Les vidéos Monimalz sont des lecteurs YouTube intégrés (elles ne s'affichent qu'en ligne ou avec une connexion internet). La vidéo Bugali est lue depuis hammerchmidt.com (format webm/AV1 — sur les navigateurs qui ne le lisent pas, l'image de couverture reste affichée).
- La police (Lato) est chargée depuis Google Fonts.
- Le design reprend la DA du book : mêmes couleurs, même hiérarchie, mêmes contenus.
