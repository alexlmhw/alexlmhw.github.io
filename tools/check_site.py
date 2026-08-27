#!/usr/bin/env python3
"""Verifications structurelles du site alexlmhw.github.io.

Aucune dependance externe. Lancer depuis la racine du depot :
    python tools/check_site.py
Code de sortie 0 si tout passe, 1 sinon.
"""
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

# Complete au fil des taches du plan.
PAGES_ATTENDUES = ["index.html"]

# Active a la tache 10, quand les 5 pages portent le meme menu.
VERIFIER_MENU = False
MENU_DEBUT = "<!-- MENU:DEBUT -->"
MENU_FIN = "<!-- MENU:FIN -->"

MOTIF_RESSOURCE = re.compile(r'(?:src|href|poster)\s*=\s*"([^"]+)"')
MOTIF_TITRE = re.compile(r"<title>(.*?)</title>", re.S)
MOTIF_DESC = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"')
MOTIF_ID = re.compile(r'id\s*=\s*"([^"]+)"')

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
    # Neutralise le marquage de la page courante et les espaces.
    brut = brut.replace(' class="actif"', "").replace(" actif", "")
    return " ".join(brut.split())


def main():
    # 1. Les pages attendues existent.
    for nom in PAGES_ATTENDUES:
        if not (RACINE / nom).is_file():
            erreur(nom, "page attendue absente")

    pages = [p for p in PAGES_ATTENDUES if (RACINE / p).is_file()]
    titres = {}
    menus = {}

    for nom in pages:
        texte = (RACINE / nom).read_text(encoding="utf-8")
        ids = set(MOTIF_ID.findall(texte))

        for cible in MOTIF_RESSOURCE.findall(texte):
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
            if not (RACINE / chemin).is_file():
                erreur(nom, "cible inexistante {}".format(chemin))

        # 5. Titre unique et non vide.
        trouve = MOTIF_TITRE.search(texte)
        if not trouve or not trouve.group(1).strip():
            erreur(nom, "titre absent ou vide")
        else:
            titres.setdefault(trouve.group(1).strip(), []).append(nom)

        if not MOTIF_DESC.search(texte):
            erreur(nom, "meta description absente")

        if VERIFIER_MENU:
            menus[nom] = bloc_menu(texte)

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
