"""Arene — les regles du duel.

Traduction en code de `regles.md`, et de rien d'autre.
Toute divergence entre ce fichier et `regles.md` se corrige ici.

Lancer :

    python3 ../scripts/montecarlo.py regles.py --tirages 200000 --sortie ./resultats
"""

NOM = "Arene — le duel"

NOTE = (
    "L'attaquant frappe une fois par tour et la cible ne riposte pas : "
    "`tours` mesure le temps d'abattage, pas l'issue d'un duel."
)

# --------------------------------------------------------------------------
# Le bareme. Toute modification se fait ici, et nulle part ailleurs.
# --------------------------------------------------------------------------

DEG_PAR_5 = 1        # chaque 5 inflige 1 blessure
DEG_PAR_6 = 2        # chaque 6 inflige 2 blessures

DES_MIN = 1          # jamais moins de 1 de
DES_MAX = 6          # jamais plus de 6 des

PV_STANDARD = 10     # points de vie d'une figurine
TOURS_MAX = 200      # garde-fou : un duel qui ne finit pas est un bug

COMBAT = (2, 3, 4, 5, 6)

# --------------------------------------------------------------------------
# Les cas a mesurer : chaque niveau de Combat contre chaque autre.
# --------------------------------------------------------------------------

SCENARIOS = [
    {"attaquant": a, "cible": c}
    for a in COMBAT
    for c in COMBAT
]


# --------------------------------------------------------------------------
# Une resolution, une fois
# --------------------------------------------------------------------------

def des_lances(combat_attaquant, combat_cible):
    """1 de par point de Combat, plus ou moins 1 de par point d'ecart."""
    n = combat_attaquant + (combat_attaquant - combat_cible)
    return max(DES_MIN, min(DES_MAX, n))


def une_attaque(n, rng):
    des = [rng.randint(1, 6) for _ in range(n)]
    k5 = sum(1 for d in des if d == 5)
    k6 = sum(1 for d in des if d == 6)
    return DEG_PAR_5 * k5 + DEG_PAR_6 * k6


def resoudre(scenario, rng):
    n = des_lances(scenario["attaquant"], scenario["cible"])

    premiere = une_attaque(n, rng)

    pv = PV_STANDARD - premiere
    tours = 1
    while pv > 0 and tours < TOURS_MAX:
        pv -= une_attaque(n, rng)
        tours += 1

    return {
        "des": n,
        "degats par tour": premiere,
        "issue": "aucun degat" if premiere == 0 else "touche",
        "tours pour abattre": tours,
    }
