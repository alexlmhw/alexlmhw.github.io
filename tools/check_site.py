#!/usr/bin/env python3
"""Verifications structurelles du site alexlmhw.github.io.

Aucune dependance externe. Lancer depuis la racine du depot :
    python tools/check_site.py
Code de sortie 0 si tout passe, 1 sinon.
"""
import os
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

# Complete au fil des taches du plan.
PAGES_ATTENDUES = ["index.html", "outils.html", "bugali.html", "monimalz.html", "fer-a-fileter.html"]

# Active a la tache 10, quand les 5 pages portent le meme menu.
VERIFIER_MENU = True
MENU_DEBUT = "<!-- MENU:DEBUT -->"
MENU_FIN = "<!-- MENU:FIN -->"

# Sous-bloc autorise a differer d'une page a l'autre : la liste d'ancres imbriquee
# sous "Accueil", presente uniquement sur index.html. Il est retire avant de
# comparer les menus, mais les 5 liens de page restent, eux, strictement identiques.
SOUS_MENU_DEBUT = "<!-- SOUS-MENU:DEBUT -->"
SOUS_MENU_FIN = "<!-- SOUS-MENU:FIN -->"
MOTIF_SOUS_MENU = re.compile(
    re.escape(SOUS_MENU_DEBUT) + ".*?" + re.escape(SOUS_MENU_FIN), re.S
)

MOTIF_RESSOURCE = re.compile(r'''(?:src|href|poster)\s*=\s*(["'])((?:(?!\1).)*)\1''')
MOTIF_TITRE = re.compile(r"<title>(.*?)</title>", re.S)
MOTIF_DESC = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"')
MOTIF_ID = re.compile(r'id\s*=\s*"([^"]+)"')
MOTIF_MENU_LIEN = re.compile(r'<a\s+href=(["\'])([^\1]+?)\1([^>]*)>')
# Attributs dont la valeur est du texte lu par un humain ou un moteur.
MOTIF_ATTR_TEXTE = re.compile(r'\b(alt|title|aria-label|content)="([^"]*)"')

erreurs = []


def erreur(page, message):
    erreurs.append("{} : {}".format(page, message))


def est_externe(cible):
    return (
        cible.startswith("http://")
        or cible.startswith("https://")
        or cible.startswith("//")
        or cible.startswith("mailto:")
        or cible.startswith("tel:")
        or cible.startswith("data:")
    )


def bloc_menu(texte):
    debut = texte.find(MENU_DEBUT)
    fin = texte.find(MENU_FIN)
    if debut == -1 or fin == -1:
        return None
    brut = texte[debut + len(MENU_DEBUT):fin]
    # Retire le sous-bloc d'ancres, autorise a n'exister que sur l'accueil.
    brut = MOTIF_SOUS_MENU.sub("", brut)
    # Neutralise le marquage de la page courante et les espaces.
    brut = brut.replace(' class="actif"', "").replace(" actif", "")
    return " ".join(brut.split())


def entree_active(texte):
    """Renvoie la liste des href marques actif dans le bloc menu brut (non neutralise)."""
    debut = texte.find(MENU_DEBUT)
    fin = texte.find(MENU_FIN)
    if debut == -1 or fin == -1:
        return None
    brut = texte[debut + len(MENU_DEBUT):fin]
    # Le sous-bloc d'ancres ne participe pas au marquage de la page courante.
    brut = MOTIF_SOUS_MENU.sub("", brut)
    return [href for _, href, reste in MOTIF_MENU_LIEN.findall(brut) if 'class="actif"' in reste]


def existe_sensible_casse(chemin_relatif):
    """Existence de fichier verifiee composant par composant sur le systeme de
    fichiers reel, pour ne pas dependre de l'insensibilite a la casse de
    Windows (GitHub Pages sert le site depuis Linux, sensible a la casse)."""
    courant = RACINE
    for partie in Path(chemin_relatif).parts:
        if not courant.is_dir():
            return False
        try:
            noms = os.listdir(courant)
        except OSError:
            return False
        if partie not in noms:
            return False
        courant = courant / partie
    return courant.is_file()


def main():
    # 1. Les pages attendues existent.
    for nom in PAGES_ATTENDUES:
        if not existe_sensible_casse(nom):
            erreur(nom, "page attendue absente")

    # 1b. Aucune page HTML a la racine qui ne soit pas enregistree dans
    # PAGES_ATTENDUES : sinon elle n'est jamais verifiee (liens, ancres,
    # titre, description, identite du menu).
    for chemin in sorted(RACINE.iterdir()):
        if chemin.is_file() and chemin.suffix == ".html" and chemin.name not in PAGES_ATTENDUES:
            erreur(chemin.name, "page HTML presente a la racine mais absente de PAGES_ATTENDUES")

    pages = [p for p in PAGES_ATTENDUES if existe_sensible_casse(p)]
    titres = {}
    menus = {}

    for nom in pages:
        texte = (RACINE / nom).read_text(encoding="utf-8")
        ids = set(MOTIF_ID.findall(texte))

        for _, cible in MOTIF_RESSOURCE.findall(texte):
            if est_externe(cible):
                continue

            # 4. Ancres internes.
            if cible.startswith("#"):
                if cible[1:] and cible[1:] not in ids:
                    erreur(nom, "ancre morte {}".format(cible))
                continue

            chemin = cible.split("#")[0].split("?")[0]
            if not chemin:
                continue

            # 2 et 3. Ressources et pages internes.
            if not existe_sensible_casse(chemin):
                erreur(nom, "cible inexistante {}".format(chemin))

        # 5. Titre unique et non vide.
        trouve = MOTIF_TITRE.search(texte)
        if not trouve or not trouve.group(1).strip():
            erreur(nom, "titre absent ou vide")
        else:
            titres.setdefault(trouve.group(1).strip(), []).append(nom)

        if not MOTIF_DESC.search(texte):
            erreur(nom, "meta description absente")

        # Balises indispensables au partage (LinkedIn, Slack, mail) et a l'accessibilite.
        for motif, manque in (
            ('rel="canonical"', "lien canonical absent"),
            ('property="og:title"', "balise og:title absente"),
            ('property="og:description"', "balise og:description absente"),
            ('property="og:image"', "balise og:image absente"),
            ('property="og:url"', "balise og:url absente"),
            ('rel="icon"', "favicon absent"),
            ('class="saut"', "lien d'evitement absent"),
            ('<main id="contenu">', "ancre #contenu du lien d'evitement absente"),
        ):
            if motif not in texte:
                erreur(nom, manque)

        # Typographie francaise : apostrophe courbe partout ou le texte est lu par
        # un humain ou un moteur. On couvre le texte hors balises, plus les
        # attributs porteurs de texte. Les autres attributs (href, class, style)
        # sont ignores : une apostrophe y serait legitime.
        suspects = [m for m in re.split(r"(<[^>]*>)", texte)
                    if not m.startswith("<") and "'" in m]
        suspects += [v for _, v in MOTIF_ATTR_TEXTE.findall(texte) if "'" in v]
        if suspects:
            erreur(nom, "apostrophe droite dans le texte : "
                        + " ".join(suspects[0].split())[:40])

        # Un saut de niveau de titre (h1 -> h3 par exemple) casse la navigation
        # au lecteur d'ecran. On verifie la continuite de la hierarchie.
        niveaux = [int(n) for n in re.findall(r"<h([1-6])[^>]*>", texte.split("<main", 1)[-1])]
        precedent = None
        for n in niveaux:
            if precedent is not None and n > precedent + 1:
                erreur(nom, "saut de niveau de titre h{} -> h{}".format(precedent, n))
                break
            precedent = n

        if VERIFIER_MENU:
            menus[nom] = bloc_menu(texte)
            actifs = entree_active(texte)
            if actifs is not None and (len(actifs) != 1 or actifs[0] != nom):
                erreur(nom, "le menu marque la mauvaise entree active")

    for titre, fichiers in titres.items():
        if len(fichiers) > 1:
            erreur(", ".join(fichiers), "titre en double : {}".format(titre))

    # 6. Menu identique sur toutes les pages.
    if VERIFIER_MENU:
        manquants = [n for n, m in menus.items() if m is None]
        for nom in manquants:
            erreur(nom, "bloc MENU:DEBUT/MENU:FIN absent")
        valeurs = {n: m for n, m in menus.items() if m is not None}
        if len(set(valeurs.values())) > 1:
            reference = valeurs.get("index.html")
            for nom, menu in valeurs.items():
                if menu != reference:
                    erreur(nom, "menu different de celui de index.html")

    if erreurs:
        print("ECHEC - {} probleme(s) :".format(len(erreurs)))
        for e in erreurs:
            print("  - " + e)
        return 1

    print("OK - {} page(s) verifiee(s)".format(len(pages)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
