#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
1. O xogador terá como pokemon a Charmander e o rival a Bulbasur.
1. O xogador escollerá un ataque (comprobar que non esgotou o número de intentos dese ataque) e realizarao ao rival (restaráselle a vitalidade ao rival).
1. O xogador seguirá escollendo e realizando ataques ata que o pokemon rival esgote a vitalidade. Cando isto se produza indicaralle ao xogador que gañou e rematará o programa.
1. O pokemon rival non realizará ningún ataque.
'''

__author__ = "Christian Varela Docampo"

from xogo import dano_ataque as dano

'''
{"N": "", "T": "", "LVL": "","DEF": "", "MHP": "", "CHP": "", "ATK": []} <- Pokemons
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

def turno_user(opc, pokemon_usuario, pokemon_rival, opc_atk):
    """Depending on the user's choice, displays battle info, attacks or flees from the battle.

    Args:
        opc (str): user's choice

    Raises:
        ValueError: If any of the values goes vobe the limit or there's an error
    """
    while True:
        battle = True
        try:
            if opc == "b" or opc == "B":
                dmg, BS = dano(pokemon_usuario, int((int(opc_atk)-1)), pokemon_rival)
                if BS == "defeated":
                    battle = False
                    BS = ["defeated", dmg]
                    return battle, BS
                damage = dmg
                break
            elif opc == "c" or opc == "C":
                battle = False
                damage = 0
                break
        except:
            continue
    return battle, damage

def main_battle(data, opc, opc_atk):
    # data = [pokemon_user, pokemon_rival]
    pokemon_usuario = data[0]
    pokemon_rival = data[1]
    battle = True
    while battle:
        """
        battle = boolean value to check if the battle is finished
        opc = user's option on the menu
        opciones = list of possible options
        opc_atk = attack option chosen by the user
        dmg = damage dealt by the user's attack
        BS = Battle Status, "defeated" if the battle is over and "None" if it continues
        s = sleep() function
        """
        while True:
            battle, damage = turno_user(opc, pokemon_usuario, pokemon_rival, opc_atk)
            if not battle == None:
                break
        # if defeated -> damage = ["defeated", dmg]
        return damage