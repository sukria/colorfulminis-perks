#!/usr/bin/env python3
"""Tests du moteur de simulation.

Le moteur doit deux choses a qui s'en sert : converger vers les bonnes valeurs,
et donner deux fois le meme resultat pour la meme graine. Un simulateur qui
n'est pas reproductible ne prouve rien.

    python3 evals/test_moteur.py

Aucune dependance : ni pytest, ni rien d'autre.
"""

import csv
import importlib.util
import random
import subprocess
import sys
import tempfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
MOTEUR = RACINE / "scripts" / "montecarlo.py"
EXEMPLE = RACINE / "exemple" / "regles.py"

echecs = []


def charger_moteur():
    spec = importlib.util.spec_from_file_location("montecarlo", MOTEUR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verifier(nom, condition, detail=""):
    if condition:
        print(f"  ok    {nom}")
    else:
        print(f"  ECHEC {nom}  {detail}")
        echecs.append(nom)


def presque(a, b, marge):
    return abs(a - b) <= marge


def ecrire_regles(dossier, corps):
    chemin = Path(dossier) / "regles.py"
    chemin.write_text(corps, encoding="utf-8")
    return chemin


def lancer(regles, dossier, tirages=20000, graine=1):
    subprocess.run(
        [sys.executable, str(MOTEUR), str(regles),
         "--tirages", str(tirages), "--graine", str(graine),
         "--sortie", str(dossier)],
        check=True, capture_output=True,
    )
    return Path(dossier) / "resume.md", Path(dossier) / "tirages.csv"


# ---------------------------------------------------------------------------
# Un jeu dont on connait la reponse exacte, a la main.
#
#   un seul de a six faces
#   valeur       moyenne exacte 3.5
#   succes 4+    exactement 50.0 %
# ---------------------------------------------------------------------------

REGLES_TEMOIN = '''
NOM = "Un de"
SCENARIOS = [{"cas": "unique"}]

def resoudre(scenario, rng):
    d = rng.randint(1, 6)
    return {"valeur": d, "issue": "succes" if d >= 4 else "echec"}
'''


def test_convergence():
    """Sur un cas a solution connue, la simulation doit tomber dessus."""
    moteur = charger_moteur()
    rng = random.Random(1)
    valeurs = [rng.randint(1, 6) for _ in range(200_000)]

    stats = moteur.agreger(valeurs)
    verifier("moyenne d'un d6 convergee vers 3.5",
             presque(stats["moyenne"], 3.5, 0.02),
             f"obtenu {stats['moyenne']:.4f}")

    issues = ["succes" if v >= 4 else "echec" for v in valeurs]
    taux = moteur.agreger(issues)["taux"]
    verifier("taux de succes sur 4+ convergee vers 50 %",
             presque(taux["succes"], 50.0, 0.5),
             f"obtenu {taux['succes']:.2f} %")


def test_agregation_types():
    """Une colonne numerique donne des stats, une colonne texte des taux."""
    moteur = charger_moteur()

    num = moteur.agreger([1, 2, 3, 4])
    verifier("colonne numerique reconnue", num["type"] == "nombre")
    verifier("mediane exacte", num["mediane"] == 2.5, f"obtenu {num['mediane']}")
    verifier("min et max exacts", num["min"] == 1 and num["max"] == 4)

    cat = moteur.agreger(["a", "a", "b", "b"])
    verifier("colonne texte reconnue", cat["type"] == "categorie")
    verifier("taux a 50/50", cat["taux"] == {"a": 50.0, "b": 50.0})

    # Un booleen n'est pas un nombre : sinon `touche` moyennerait au lieu de compter.
    bools = moteur.agreger([True, False])
    verifier("les booleens sont traites en categories",
             bools["type"] == "categorie")


def test_reproductibilite():
    """Deux lancers de meme graine donnent des fichiers identiques."""
    with tempfile.TemporaryDirectory() as tmp:
        regles = ecrire_regles(tmp, REGLES_TEMOIN)
        a = Path(tmp) / "a"
        b = Path(tmp) / "b"
        r1, _ = lancer(regles, a, tirages=5000, graine=42)
        r2, _ = lancer(regles, b, tirages=5000, graine=42)
        verifier("meme graine, meme resume",
                 r1.read_text() == r2.read_text())

        c = Path(tmp) / "c"
        r3, _ = lancer(regles, c, tirages=5000, graine=43)
        verifier("graine differente, resume different",
                 r1.read_text() != r3.read_text())


def test_csv():
    """Le CSV contient une ligne par tirage, avec scenario et sortie."""
    with tempfile.TemporaryDirectory() as tmp:
        regles = ecrire_regles(tmp, REGLES_TEMOIN)
        _, csv_path = lancer(regles, tmp, tirages=1000)

        with open(csv_path, encoding="utf-8") as f:
            lignes = list(csv.DictReader(f))

        verifier("une ligne par tirage", len(lignes) == 1000, f"obtenu {len(lignes)}")
        verifier("les colonnes du scenario sont presentes",
                 "cas" in lignes[0])
        verifier("les colonnes de sortie sont presentes",
                 "valeur" in lignes[0] and "issue" in lignes[0])


def test_borne_csv():
    """Le CSV ne depasse pas --csv-max, meme sur beaucoup de tirages."""
    with tempfile.TemporaryDirectory() as tmp:
        regles = ecrire_regles(tmp, REGLES_TEMOIN)
        subprocess.run(
            [sys.executable, str(MOTEUR), str(regles), "--tirages", "50000",
             "--csv-max", "1000", "--sortie", tmp],
            check=True, capture_output=True,
        )
        with open(Path(tmp) / "tirages.csv", encoding="utf-8") as f:
            n = sum(1 for _ in f) - 1
        verifier("CSV borne par --csv-max", n <= 1000, f"obtenu {n}")


def test_regles_invalides():
    """Un fichier de regles incomplet echoue proprement, sans trace Python."""
    cas = [
        ("SCENARIOS manquant", 'def resoudre(s, rng): return {"a": 1}'),
        ("resoudre manquante", 'SCENARIOS = [{"a": 1}]'),
        ("SCENARIOS vide", 'SCENARIOS = []\ndef resoudre(s, rng): return {"a": 1}'),
        ("resoudre ne retourne pas un dict",
         'SCENARIOS = [{"a": 1}]\ndef resoudre(s, rng): return 3'),
    ]
    for nom, corps in cas:
        with tempfile.TemporaryDirectory() as tmp:
            regles = ecrire_regles(tmp, corps)
            r = subprocess.run(
                [sys.executable, str(MOTEUR), str(regles),
                 "--tirages", "10", "--sortie", tmp],
                capture_output=True, text=True,
            )
            verifier(f"echec propre : {nom}",
                     r.returncode == 1 and "erreur :" in r.stderr
                     and "Traceback" not in r.stderr,
                     f"code {r.returncode}")


def lire_moyennes(texte, section_voulue):
    """Extrait {(colonne 1, colonne 2): moyenne} d'une section du resume."""
    moyennes = {}
    section = None
    for ligne in texte.splitlines():
        if ligne.startswith("## "):
            section = ligne[3:].strip()
            continue
        if section != section_voulue or not ligne.startswith("| ") or "---" in ligne:
            continue
        cellules = [c.strip() for c in ligne.strip("|").split("|")]
        try:
            moyennes[(cellules[0], cellules[1])] = float(cellules[2])
        except ValueError:
            continue  # la ligne d'entetes
    return moyennes


def test_exemple_fourni():
    """L'exemple livre tourne, et ses deux anomalies sont bien la.

    Le plafond de 6 des et le plancher de 1 de aplatissent les extremes : un
    Combat 6 met le meme temps a abattre n'importe qui, et un Combat 2 met le
    meme temps quel que soit l'adversaire au-dessus de lui. C'est le defaut
    que le tutoriel doit faire trouver.
    """
    with tempfile.TemporaryDirectory() as tmp:
        resume, _ = lancer(EXEMPLE, tmp, tirages=20000)
        texte = resume.read_text(encoding="utf-8")
        verifier("l'exemple produit un resume", "## tours pour abattre" in texte)

        tours = lire_moyennes(texte, "tours pour abattre")
        verifier("les 25 scenarios sont la", len(tours) == 25, f"obtenu {len(tours)}")

        haut = [tours[("6", str(c))] for c in range(2, 7)]
        verifier("un Combat 6 abat tout le monde a la meme vitesse",
                 max(haut) - min(haut) < 0.1,
                 f"de {min(haut):.2f} a {max(haut):.2f}")

        bas = [tours[("2", str(c))] for c in range(3, 7)]
        verifier("un Combat 2 met le meme temps face a 3, 4, 5 et 6",
                 max(bas) - min(bas) < 0.2,
                 f"de {min(bas):.2f} a {max(bas):.2f}")

        verifier("Combat 4 et Combat 6 sont identiques face a un Combat 2",
                 abs(tours[("4", "2")] - tours[("6", "2")]) < 0.1,
                 f"{tours[('4', '2')]:.2f} contre {tours[('6', '2')]:.2f}")

        verifier("le plancher double le temps d'abattage entre 2v2 et 2v3",
                 tours[("2", "3")] > 1.8 * tours[("2", "2")],
                 f"{tours[('2', '2')]:.2f} puis {tours[('2', '3')]:.2f}")


def main():
    tests = [
        ("convergence", test_convergence),
        ("agregation", test_agregation_types),
        ("reproductibilite", test_reproductibilite),
        ("csv", test_csv),
        ("borne csv", test_borne_csv),
        ("regles invalides", test_regles_invalides),
        ("exemple fourni", test_exemple_fourni),
    ]
    for nom, fn in tests:
        print(f"\n{nom}")
        fn()

    print()
    if echecs:
        print(f"{len(echecs)} echec(s) : " + ", ".join(echecs))
        return 1
    print("tout passe.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
