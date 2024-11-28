#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
1. O xogador terá como pokemon a Charmander e o rival a Bulbasur.
1. O xogador escollerá un ataque (comprobar que non esgotou o número de intentos dese ataque) e realizarao ao rival (restaráselle a vitalidade ao rival).
1. O xogador seguirá escollendo e realizando ataques ata que o pokemon rival esgote a vitalidade. Cando isto se produza indicaralle ao xogador que gañou e rematará o programa.
1. O pokemon rival non realizará ningún ataque.
'''

__author__ = "Christian Varela Docampo"

from random import randint as r
import pokemons as p
import editor_pok as edit
from xogo import dano_ataque as dano
import interfaz as show
from time import sleep as s

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

def cancel(value):
    """function to go back at any moment mid battle

    Args:
        value (any): user's input

    Returns:
        bool: True or False depending on if the input is "q" or not
    """
    if value == "q":
        return True
    return False

def assign_pokemons():
    """Displays a list of gens so the user can select which gen to play in and what pokemon to select

    Raises:
        ValueError: If any of the values goes vobe the limit or there's an error
    """
    while True:
        try:
            show.display_gens()
            selec = input("En que xeración queres xogar?\n\t*Nota: Non podes enfrentar a pokemons de distintas xeracións!"
                          "\n\t*Outra nota: A xeración X é unha con pokemons experimentales non oficiales!\n")
            if cancel(selec):
                return 0, 0
            if int(selec) not in range(1, len(p.gens)+1):
                raise ValueError
            keys = list(p.gens.keys())
            selec = keys[int(selec)-1]
            pokemons = p.gens[selec]
            show.display_pokemons(pokemons)
            selec = input("Seleccione o pokemon que queres empregar (1, 2, 3...):\n")
            if (int(selec) not in range(1, len(pokemons)+1)) or cancel(selec):
                raise ValueError
            break
        except:
            print("Opción inválida.")
    pokemon_usuario = pokemons[int(selec)-1]
    while True:
        selec_IA = r(1, len(pokemons))
        if selec_IA != int(selec) or len(pokemons) <= 1:
            break
    pokemon_rival = pokemons[selec_IA-1]

    print(f"Teu pokemon é {pokemon_usuario["N"]} e vas pelar contra {pokemon_rival["N"]}!\n")
    s(2)
    return pokemon_usuario, pokemon_rival

def main_menu():
    """
    Main menu of the game where the user can select what to do
    """
    while True:
        while True:
            opc = input("Benvido a pokemon!\nQue desexa facer?\na)XOGAR\nb)EDITOR DE POKEMONS\nc)SAIR\n")
            lista_opc = ["a", "A", "b", "B", "c", "C"]
            if opc in lista_opc:
                break
            else:
                print("Opción inválida, tente de novo.")
        
        if opc == "a" or opc =="A":
            return False
        elif opc == "b" or opc == "B":
            edit.selec_opc()
            return True
        elif opc == "c" or opc == "C":
            print("Saindo...")
            exit()

def battle_opc():
    """Displays a list of options mid battle for the user to select

    Raises:
        ValueError: If any of the values goes vobe the limit or there's an error
    """
    while True:
        try:
            s(0.5)
            opc = input("Selecione a acción a tomar:\na)Mostrar detalles da batalla\nb)Atacar\nc)Fuxir\n")
            opciones = ["A", "a", "B", "b", "C", "c"]
            if opc not in opciones:
                raise ValueError
            print("\n\n")
            break
        except:
            print("Opción inválida.")
    return opc

def turno_user(opc):
    """Depending on the user's choice, displays battle info, attacks or flees from the battle.

    Args:
        opc (str): user's choice

    Raises:
        ValueError: If any of the values goes vobe the limit or there's an error
    """
    while True:
        turno_rival = True
        battle = True
        try:
            if opc == "a" or opc == "A":
                s(0.2)
                show.mostrar_stats(pokemons)
                turno_rival = False
                battle = True
                break
            elif opc == "b" or opc == "B":
                s(0.2)
                show.mostrar_ataques(pokemon_usuario)
                opc_atk = input("Seleccione o ataque(1, 2, 3...):")
                if cancel(opc_atk):
                    return None, None
                if int(opc_atk) not in range(1,len(pokemon_usuario["ATK"])+1):
                    print("O ataque seleccionado non existe ou non ten suficientes puntos de acción.")
                    raise ValueError
                dmg, BS = dano(pokemon_usuario, int((int(opc_atk)-1)), pokemon_rival)
                s(0.5)
                print(f"O ataque produciu {dmg} puntos de dano!")
                if BS == "defeated":
                    s(0.5)
                    print(f"Gañaches! {pokemon_rival["N"]} foi derrotado!")
                    turno_rival = False
                    battle = False
                    s(1)
                break
            elif opc == "c" or opc == "C":
                s(0.2)
                print("Fuxiches!")
                battle = False
                turno_rival = False
                break
        except:
            continue
    return turno_rival, battle


def rival():
    """
    When it's the rival's turn, this function attacks for it.
    """
    battle = True
    while turno_rival:
        while True:
            ataque = r(0, len(pokemon_rival["ATK"])-1)
            if pokemon_rival["ATK"][ataque]["CAP"] != 0:
                break
        dmg, BS = dano(pokemon_rival, ataque, pokemon_usuario)
        s(0.5)
        print(f"{pokemon_rival["N"]} empregou {pokemon_rival["ATK"][ataque]["N"]}!\nO ataque produciu {dmg} puntos de dano!")
        if BS == "defeated":
            s(0.5)
            print(f"Perdeches! {pokemon_rival["N"]} derrotouche!")
            battle = False
        else:
            s(1)
            print("\n\n")
        break
    return battle

# Calls for the new() function on pokemons.py that gets every pokemon ready
p.new()

pokemons = p.pokemons

m_m = True
while m_m:
    m_m = main_menu()
    if not m_m:
        pokemon_usuario, pokemon_rival = assign_pokemons()
        if pokemon_usuario != 0:
            pokemons = [pokemon_usuario, pokemon_rival]
            break
        else:
            m_m = True

show.mostrar_stats(pokemons)
s(1)

battle = True
opc = None
turno = 1

while battle:
    """
    battle = boolean value to check if the battle is finished
    opc = user's option on the menu
    opciones = list of possible options
    opc_atk = attack option chosen by the user
    dmg = damage dealt by the user's attack
    BS = Battle Status, "defeated" if the battle is over and "None" if it continues
    turno_rival = boolean vlaue to check if it's the rival's turn
    ataque = selected attack for the AI (riva)
    s = sleep() function
    """
    print(f"Turno {turno}!")
    while True:
        opc = battle_opc()
        turno_rival, battle = turno_user(opc)
        if not turno_rival == None and not battle == None:
            break
    if turno_rival:
        print(f"{pokemon_rival["N"]} está atacando!")
        battle = rival()
    turno += 1
    if not battle:
        print("Finalizando programa...")
        exit()