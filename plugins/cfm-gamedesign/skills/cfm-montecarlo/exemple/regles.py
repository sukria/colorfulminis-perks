"""Les Gardiens du Pont — l'action d'Attaque.

Traduction en code de `regles.md`, et de rien d'autre.
Toute divergence entre ce fichier et `regles.md` se corrige ici.

Lancer :

    python3 ../scripts/montecarlo.py regles.py --tirages 200000 --sortie ./resultats
"""

NOM = "Les Gardiens du Pont — l'action d'Attaque"

NOTE = (
    "Regles simulees : `regles.md`. Les blessures sont comptees **apres** "
    "l'armure de la cible."
)

# --------------------------------------------------------------------------
# Le bareme. Toute modification se fait ici, et nulle part ailleurs.
# --------------------------------------------------------------------------

SEUIL = 4          # un de de 4 ou plus est un succes
DEG_PAR_5 = 1      # chaque 5 inflige 1 blessure
DEG_PAR_6 = 2      # chaque 6 inflige 2 blessures
DEF_SEUIL = 5      # chaque 5+ en defense annule 1 blessure

# Une arme = une clause, decrite comme le texte de sa ligne de tableau.
#   plat   blessures ajoutees a toute attaque reussie
#   par_6  blessures ajoutees par 6 obtenu
#   subst  {valeur lue: valeur retenue}
ARMES = {
    "Baton":    dict(plat=0, par_6=0, subst={}),
    "Epee":     dict(plat=1, par_6=0, subst={}),
    "Hache":    dict(plat=0, par_6=1, subst={}),
    "Arc long": dict(plat=0, par_6=0, subst={3: 4}),
}

# --------------------------------------------------------------------------
# Les cas a mesurer
# --------------------------------------------------------------------------

SCENARIOS = [
    {"arme": arme, "vigueur": vigueur, "armure": armure}
    for arme in ARMES
    for vigueur in (1, 2, 3, 4, 5, 6)
    for armure in (0, 2)
]


# --------------------------------------------------------------------------
# Une resolution, une fois
# --------------------------------------------------------------------------

def resoudre(scenario, rng):
    arme = ARMES[scenario["arme"]]

    des = [rng.randint(1, 6) for _ in range(scenario["vigueur"])]
    des = [arme["subst"].get(d, d) for d in des]

    succes = sum(1 for d in des if d >= SEUIL)

    if succes == 0:
        maladroit = any(d == 1 for d in des)
        return {
            "issue": "maladresse" if maladroit else "echec",
            "touche": 0,
            "blessures": 0,
        }

    k5 = sum(1 for d in des if d == 5)
    k6 = sum(1 for d in des if d == 6)
    brut = DEG_PAR_5 * k5 + DEG_PAR_6 * k6 + arme["plat"] + arme["par_6"] * k6

    annule = sum(1 for _ in range(scenario["armure"])
                 if rng.randint(1, 6) >= DEF_SEUIL)

    return {
        "issue": "succes",
        "touche": 1,
        "blessures": max(0, brut - annule),
    }
