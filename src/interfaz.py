#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep as s
from roman import fromRoman as fr
from pokemons import gens

'''
Programa só para mostrar a interfaz.

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

__author__ = "Christian Varela Docampo"

def display_gens():
    """
    Displays a list of all gens for the user to select
    """
    keys = list(gens.keys())
    for i in range(len(gens)):
        print(str(fr(keys[i]))+") Gen", keys[i])

def display_pokemons(pokemons):
    """Displays a list of pokemons from a specific gen for the user to select.

    Args:
        pokemons (dict): dictionary containing the pokemons of a specific generation
    """
    if len(pokemons) == 0:
        print(pokemons)
        print("That generation is empty!")
        return 0
    x = 0
    for i in pokemons:
        x += 1
        print(x,")",i["N"])

def mostrar_stats(pokemon_list: list):
    """Shows the stats of the selected pokemon with it's attacks

    Args:
        pokemon_list (list): List of pokemons selected (usually user and rival)
    """
    for x in pokemon_list:
        print(x["N"]+":\nType:",x["T"],"\nLevel:",float(x["LVL"]),"\nLife:",x["CHP"],
            "\nAttack list:")
        y = 0
        for i in x["ATK"]:
            s(0.2)
            print("\t-",x["ATK"][y]["N"],"--> Type:",x["ATK"][y]["T"],"Power:",float(x["ATK"][y]["P"]),"Action Points:",float(x["ATK"][y]["CAP"]),"\n")
            y = y + 1
        s(0.5)

def mostrar_ataques(pokemon: dict):
    """Displays a list of the user's pokemon attacks

    Args:
        pokemon (dict): user's pokemon
    """
    y = 0
    for i in pokemon["ATK"]:
        s(0.2)
        print("\t",y+1,")",pokemon["ATK"][y]["N"],"--> Type:",pokemon["ATK"][y]["T"],"Power:",float(pokemon["ATK"][y]["P"]),"Action Points:",float(pokemon["ATK"][y]["CAP"]),"\n")
        y = y + 1