#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
1. Nome do pokemon.
1. Tipo: Para Charmander será lume e para Bulbasur planta.
1. Nivel: entre 1 e 99.
1. Vitalidade Máxima: escolle calquera valor que consideres.
1. Vitalidade actual: nun primeiro momento debe ser igual a vitalidade máxima.
1. Ataques: lista de ataques. Cada ataque será un dicionario cos seguintes campos:
1. Nome: nome do ataque.
1. Tipo: poderá ser de calquera tipo definido (lume, planta, normal, etc.)
1. Poder: escolle calquera valor que consideres.
1. Número de ataques máximos: refírese as veces que se pode utilizar un ataque.
1. Número de ataques restantes: nun primeiro momento debe ser igual a ao número de ataques máximos.
'''

__author__ = "Christian Varela Docampo"

'''
{"N": "", "T": "", "LVL": "", "DEF": "", "MHP": "", "CHP": "", "ATK": []} <- Pokemons
{"N": "", "T": "", "P": "", "MAP": "", "CAP": ""} <- Ataques
N: Nome
T: Tipo, a lista de ó lado son os tipos contra o que este é forte
LVL: Nivel (LeVeL)
MHP: Vida máxima (Max Hit Points)
CHP: Vida actual (Current Hit Points)
ATK: Ataques (AtTacK)
P: Poder (Power)
MAP: Número de ataques máximos (Max Attack Points)
CAP: Número de ataques restantes (Current Attack Points)
'''

import json
from random import randint as r

pokemons = json.load(open(r"./ripper/pokemons_usable.json"))

genI, genII, genIII, genIV, genV, genVI, genVII, genVIII, genIX, genX = [], [], [], [], [], [], [], [], [], []
gens = {"I": genI,"II": genII, "III": genIII, "IV": genIV, "V": genV, "VI": genVI, "VII": genVII, "VIII": genVII, "IX": genIX, "X": genX}
def new():
    """
    Function that gets the selected pokemon ready for battle, assigning them similar levels,
    preparing the stats, attacks, etc.
    """
    x = 0
    # The level is set randomly but it's the same for all
    LVL = int(r(11,89) + r(-10,10))
    for pokemon in pokemons:
        x += 1
        pokemon["LVL"] = LVL
        # The HP has a small random factor to it but it's similar for both.
        while True:
            pokemon["MHP"] = pokemon["LVL"] * 10 + r(-50,50)
            if pokemon["MHP"] <= 1000 and pokemon["MHP"] >= 10:
                break
        pokemon["CHP"] = pokemon["MHP"]
        # This whole part just gets the attacks ready and deletes those that do not have
        # any Power, since passive attacks and buffs have not been implemented inthe game yet.
        continue_ = True
        while continue_:
            continue_ = False
            for atk in pokemon["ATK"]:
                atk["CAP"] = atk["MAP"]
                if int(atk["P"]) == 0 or float(atk["MAP"]) == 0:
                    pokemon["ATK"].pop(pokemon["ATK"].index(atk))
                    continue_ = True
                    break
        # Organises the pokemons in generations for easier management.
        if x in range(1,152):
            genI.append(pokemon)
        elif x in range(152,252):
            genII.append(pokemon)
        elif x in range(252,387):
            genIII.append(pokemon)
        elif x in range(387,494):
            genIV.append(pokemon)
        elif x in range(494,650):
            genV.append(pokemon)
        elif x in range(650,722):
            genVI.append(pokemon)
        elif x in range(722,810):
            genVII.append(pokemon)
        elif x in range(810,906):
            genVIII.append(pokemon)
        elif x in range(906,1026):
            genIX.append(pokemon)
        elif x >= 1026:
            genX.append(pokemon)
