#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
dano_ataque(pokemon_atacante: Dict, ataque: Dict, pokemon_atacado: Dict)
Recibe como parámetros o pokemon que realiza o ataque, o ataque que realiza e o pokemon receptor do ataque.
Esta función deberá calcular e devolver o dano que realizará dito ataque.
O dano realizado é igual a vitalidade que se restará ao pokemon receptor ataque en función de:

1. O tipo de ataque e o tipo do pokemon que realiza o ataque. Por exemplo un ataque de tipo lume é moi efectivo contra un pokemon de tipo planta pero pouco contra un de tipo auga.
1. Selecciona ditas debilidades.
1. O nivel do pokemon que realiza o ataque. O nivel do pokemon que recibe o ataque non influirá.

Deberá ter unha compoñente aleatoria. O dano non sempre será o mesmo repetíndose as mesmas condicións. Utiliza a librería random
'''

__author__ = "Christian Varela Docampo"

from random import randint as r
import json

'''
{"N": "", "T": "", "LVL": "", "DEF": "", "MHP": "", "CHP": "", "ATK": []} <- Pokemons
{"N": "", "T": "", "P": "", "MAP": "", "CAP": ""} <- Ataques
N: Nome
T: Tipo
LVL: Nivel (LeVeL)
MHP: Vida máxima (Max Hit Points)
CHP: Vida actual (Current Hit Points)
ATK: Ataques (AtTacK)
P: Poder (Power)
MAP: Número de ataques máximos (Max Attack Points)
CAP: Número de ataques restantes (Current Attack Points)
'''

debilidades = json.load(open("ripper/Weaknesses.json"))

def dano_ataque(pokemon_atacante: dict, ataque: dict, pokemon_atacado: dict) -> float:
    """calculates the damage of an attack inflicted to a pokemon

    Args:
        pokemon_atacante (dict): attacking pokemon
        ataque (dict): number of the attack inside the "ATK" list
        pokemon_atacado (dict): attacked pokemon

    Returns:
        float: damage of the attack
    """
    debil = False
    if pokemon_atacado["T"] in debilidades[pokemon_atacante["ATK"][ataque]["T"]]:
        debil = True
    crit = 1
    if debil:
        crit = 2
        if r(1,100) in range(47,52):
            crit = 3
    dano = -1
    while dano<=0:
        # Og dmg:
        dano = round(((((2*crit*(float(pokemon_atacante["LVL"])))/5)+2)*(float(pokemon_atacante["ATK"][ataque]["P"]))/(float(pokemon_atacado["DEF"])/(r(20,30)/10)))*1.5*(r(5,10)/10))
        # For quicker matches (Removed DEF):
        # dano = round((((2*crit*(float(pokemon_atacante["LVL"])))/5)+2)*(float(pokemon_atacante["ATK"][ataque]["P"]))*1.5*(r(5,10)/10))
    pokemon_atacante["ATK"][ataque]["CAP"] = float(pokemon_atacante["ATK"][ataque]["CAP"]) - 1
    pokemon_atacado["CHP"] = float(pokemon_atacado["CHP"]) - dano
    if float(pokemon_atacado["CHP"]) <= 0:
        return dano, "defeated"
    return dano, "None"
