#!/usr/bin/env python3
"""Moteur de simulation Monte-Carlo pour le game design.

Ce fichier ne connait aucune regle de jeu. Il sait seulement repeter une
resolution un grand nombre de fois, compter ce qui en sort, et l'ecrire.

Les regles vivent dans un second fichier, un module Python qui declare :

    NOM         str, le nom de ce qui est mesure
    SCENARIOS   list[dict], les cas a balayer (un dict = une ligne de resultat)
    resoudre(scenario, rng) -> dict, une resolution, une fois

Usage :

    python3 montecarlo.py regles.py
    python3 montecarlo.py regles.py --tirages 200000 --graine 42
    python3 montecarlo.py regles.py --sortie ./resultats

Sorties, dans le dossier --sortie :

    resume.md    les tableaux agreges, lisibles
    tirages.csv  le detail des lancers, une ligne par tirage

Aucune dependance : Python 3.9 ou plus, rien d'autre.
"""

import argparse
import csv
import importlib.util
import random
import statistics
import sys
from pathlib import Path

TIRAGES_DEFAUT = 20_000
GRAINE_DEFAUT = 1
CSV_MAX_DEFAUT = 200_000


# ---------------------------------------------------------------------------
# Chargement du fichier de regles
# ---------------------------------------------------------------------------

def charger_regles(chemin):
    """Importe le module de regles et verifie qu'il expose ce qu'il faut."""
    chemin = Path(chemin).resolve()
    if not chemin.is_file():
        sortir(f"fichier de regles introuvable : {chemin}")

    spec = importlib.util.spec_from_file_location("regles_du_jeu", chemin)
    module = importlib.util.module_from_spec(spec)
    sys.modules["regles_du_jeu"] = module
    try:
        spec.loader.exec_module(module)
    except Exception as err:  # noqa: BLE001 - on veut le message brut
        sortir(f"le fichier de regles a plante a l'import : {err}")

    for attendu in ("SCENARIOS", "resoudre"):
        if not hasattr(module, attendu):
            sortir(f"le fichier de regles doit declarer `{attendu}`")

    if not isinstance(module.SCENARIOS, (list, tuple)) or not module.SCENARIOS:
        sortir("`SCENARIOS` doit etre une liste non vide de dictionnaires")

    for i, scenario in enumerate(module.SCENARIOS):
        if not isinstance(scenario, dict):
            sortir(f"SCENARIOS[{i}] n'est pas un dictionnaire")

    return module


def sortir(message):
    print(f"erreur : {message}", file=sys.stderr)
    raise SystemExit(1)


# ---------------------------------------------------------------------------
# Agregation
# ---------------------------------------------------------------------------

def est_nombre(valeur):
    return isinstance(valeur, (int, float)) and not isinstance(valeur, bool)


def agreger(valeurs):
    """Resume une colonne : stats si elle est numerique, frequences sinon."""
    if all(est_nombre(v) for v in valeurs):
        return {
            "type": "nombre",
            "moyenne": statistics.fmean(valeurs),
            "mediane": statistics.median(valeurs),
            "ecart_type": statistics.pstdev(valeurs) if len(valeurs) > 1 else 0.0,
            "min": min(valeurs),
            "max": max(valeurs),
        }

    total = len(valeurs)
    comptes = {}
    for v in valeurs:
        cle = str(v)
        comptes[cle] = comptes.get(cle, 0) + 1
    return {
        "type": "categorie",
        "taux": {k: 100.0 * n / total for k, n in sorted(comptes.items())},
    }


# ---------------------------------------------------------------------------
# Ecriture
# ---------------------------------------------------------------------------

def libelle(scenario):
    return " · ".join(f"{k} {v}" for k, v in scenario.items())


def tableau(entetes, lignes):
    out = ["| " + " | ".join(entetes) + " |",
           "|" + "|".join(["---"] * len(entetes)) + "|"]
    for ligne in lignes:
        out.append("| " + " | ".join(ligne) + " |")
    return "\n".join(out)


def nombre(valeur):
    if isinstance(valeur, int):
        return str(valeur)
    return f"{valeur:.2f}"


def ecrire_resume(chemin, module, args, cles_scenario, resultats):
    nom = getattr(module, "NOM", Path(args.regles).stem)
    note = getattr(module, "NOTE", "")

    lignes = [
        f"# {nom} — resultats de simulation",
        "",
        "*Genere par `montecarlo.py`. Ne pas editer a la main : "
        "corriger les regles, puis relancer.*",
        "",
        f"**{format(args.tirages, ',d').replace(',', ' ')} tirages par scenario**, "
        f"graine {args.graine}, {len(resultats)} scenarios.",
        "",
    ]
    if note:
        lignes += [note, ""]

    # Une colonne de sortie = un tableau.
    colonnes = list(resultats[0]["stats"].keys())

    for colonne in colonnes:
        exemple = resultats[0]["stats"][colonne]
        lignes.append(f"## {colonne}")
        lignes.append("")

        if exemple["type"] == "nombre":
            entetes = list(cles_scenario) + ["moyenne", "mediane", "ecart-type", "min", "max"]
            corps = []
            for r in resultats:
                s = r["stats"][colonne]
                corps.append(
                    [str(r["scenario"][k]) for k in cles_scenario]
                    + [nombre(s["moyenne"]), nombre(s["mediane"]),
                       nombre(s["ecart_type"]), nombre(s["min"]), nombre(s["max"])]
                )
        else:
            modalites = sorted({m for r in resultats for m in r["stats"][colonne]["taux"]})
            entetes = list(cles_scenario) + modalites
            corps = []
            for r in resultats:
                taux = r["stats"][colonne]["taux"]
                corps.append(
                    [str(r["scenario"][k]) for k in cles_scenario]
                    + [f"{taux.get(m, 0.0):.1f} %" for m in modalites]
                )

        lignes.append(tableau(entetes, corps))
        lignes.append("")

    Path(chemin).write_text("\n".join(lignes), encoding="utf-8")


def ecrire_csv(chemin, entetes, lignes):
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=entetes)
        writer.writeheader()
        writer.writerows(lignes)


# ---------------------------------------------------------------------------
# Boucle principale
# ---------------------------------------------------------------------------

def simuler(module, args):
    rng = random.Random(args.graine)
    resultats = []
    lignes_csv = []
    entetes_csv = None
    cles_scenario = list(module.SCENARIOS[0].keys())

    # Combien de tirages detailles on garde par scenario, pour borner le CSV.
    quota = max(1, args.csv_max // len(module.SCENARIOS))

    for index, scenario in enumerate(module.SCENARIOS):
        colonnes = {}
        for tirage in range(args.tirages):
            sortie = module.resoudre(scenario, rng)
            if not isinstance(sortie, dict):
                sortir("`resoudre` doit retourner un dictionnaire")
            for cle, valeur in sortie.items():
                colonnes.setdefault(cle, []).append(valeur)

            if tirage < quota:
                ligne = {"scenario": index, "tirage": tirage}
                ligne.update(scenario)
                ligne.update(sortie)
                if entetes_csv is None:
                    entetes_csv = list(ligne.keys())
                lignes_csv.append(ligne)

        resultats.append({
            "scenario": scenario,
            "stats": {cle: agreger(vals) for cle, vals in colonnes.items()},
        })

        print(f"  {index + 1}/{len(module.SCENARIOS)}  {libelle(scenario)}",
              file=sys.stderr)

    return cles_scenario, resultats, entetes_csv, lignes_csv


def main():
    p = argparse.ArgumentParser(
        description="Simule un jeu par tirages Monte-Carlo.")
    p.add_argument("regles", help="fichier Python decrivant les regles")
    p.add_argument("--tirages", type=int, default=TIRAGES_DEFAUT,
                   help=f"tirages par scenario (defaut : {TIRAGES_DEFAUT})")
    p.add_argument("--graine", type=int, default=GRAINE_DEFAUT,
                   help=f"graine aleatoire, pour reproduire (defaut : {GRAINE_DEFAUT})")
    p.add_argument("--sortie", default=".",
                   help="dossier de sortie (defaut : le dossier courant)")
    p.add_argument("--csv-max", type=int, default=CSV_MAX_DEFAUT,
                   help=f"lignes maximum dans le CSV (defaut : {CSV_MAX_DEFAUT})")
    args = p.parse_args()

    if args.tirages < 1:
        sortir("--tirages doit valoir au moins 1")

    module = charger_regles(args.regles)
    dossier = Path(args.sortie)
    dossier.mkdir(parents=True, exist_ok=True)

    print(f"simulation : {args.tirages} tirages x {len(module.SCENARIOS)} scenarios",
          file=sys.stderr)
    cles, resultats, entetes_csv, lignes_csv = simuler(module, args)

    resume = dossier / "resume.md"
    tirages = dossier / "tirages.csv"
    ecrire_resume(resume, module, args, cles, resultats)
    ecrire_csv(tirages, entetes_csv, lignes_csv)

    print(f"\n{resume}\n{tirages}  ({len(lignes_csv)} lignes)", file=sys.stderr)


if __name__ == "__main__":
    main()
