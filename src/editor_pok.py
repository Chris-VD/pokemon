#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Archivo para editar os pokemons e engadir novos
'''

from time import sleep as s
import json
from xogo import debilidades
from random import randint as r
from interfaz import mostrar_stats as stats
from interfaz import mostrar_ataques as atk
import pokemons
from os import system as clear
import interfaz as show

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

def new_atk(pokemon: dict):
    """Generates a new attack, either for an existing pokemon or for a new one.

    Args:
        pokemon (dict): selected pokemon

    Raises:
        ValueError: if any value goes avobe the limit or there's any error
    """
    while True:
        try:
            new_atk_n = input("Introduza o nome do novo ataque:\n")
            if cancel(new_atk_n):
                return 0
            new_atk_t = input("Introduza o tipo do novo ataque:\n")
            if cancel(new_atk_t):
                return 0
            if new_atk_t not in debilidades:
                raise ValueError
            new_atk_p = input("Introduza o poder do novo ataque:\n")
            if cancel(new_atk_p):
                return 0
            if int(new_atk_p) not in range(1,200):
                raise ValueError
            new_atk_ap = input("Introduza os action points do novo ataque:\n")
            if cancel(new_atk_ap):
                return 0
            if int(new_atk_ap) not in range(1,11):
                raise ValueError
            new_atk_full = {"N": new_atk_n, "T": new_atk_t, "P": int(new_atk_p), "MAP": int(new_atk_ap), "CAP": int(new_atk_ap)}
            pokemon["ATK"].append(new_atk_full)
            print("Ataque engadido!")
            return 
        except:
            print("Erro, tente de novo.")

def new_pokemon():
    """Creates a new pokemon.

    Raises:
        ValueError: If any of the values goes vobe the limit or there's an error
    """
    while True:
        try:
            new_pkm_n = input("Introduza o nome do novo pokemon:\n")
            if cancel(new_pkm_n):
                return 0
            new_pkm_t = input("Introduza o tipo do novo pokemon:\n")
            if cancel(new_pkm_t):
                return 0
            if new_pkm_t not in debilidades:
                raise ValueError
            num_ataques = int(input("Cantos ataques vai ter este pokemon?\n"))
            if cancel(num_ataques):
                return 0
            if int(num_ataques) not in range(1,31):
                raise ValueError
            new_pkm = {"N": new_pkm_n, "T": new_pkm_t, "LVL": 00, "MHP": 00, "CHP": 00, "ATK": []}
            while num_ataques != 0:
                new_atk(new_pkm)
                num_ataques = num_ataques - 1
            print("Pokemon creado!")
            new_pkm = [new_pkm]
            stats(new_pkm)
            new_pkm = new_pkm[0]
            break
        except:
            print("Erro, tente de novo.")
    print(new_pkm)
    pokemons.pokemons.append(new_pkm)
    pokemons_final = pokemons.pokemons
    json.dump(pokemons_final, open("ripper\pokemons_usable.json", "w"))
    return 

def modify_atk(pokemon_: dict):
    """Modifies an already existing attack.

    Args:
        pokemon (dict): pokemon selected to modify

    Raises:
        ValueError: If any of the values goes vobe the limit or there's an error
    """
    while True:
        try:
            atk(pokemon_)
            ataque = input("Que ataque desexa modificar? (1, 2, 3...)\n")
            if cancel(ataque):
                return 0
            if int(ataque) not in range(1,len(pokemon_["ATK"])+1):
                raise ValueError
            ataque = int(ataque) - 1
            print("Que desexa modificar?\n")
            modif = input("\na)Nome\nb)Tipo\nc)Poder\nd)Action Points\n")
            if cancel(modif):
                return 0
            opc_list = ["a", "A", "b", "B", "c", "C", "d", "D"]
            if modif not in opc_list:
                raise ValueError
            if modif == "a" or modif == "A":
                new_txt = input("Introduza o novo nome:\n")
                if cancel(new_txt):
                    return 0
                pokemon_["ATK"][ataque]["N"] = new_txt
            elif modif == "b" or modif == "B":
                new_txt = input("Introduza o novo tipo:\n")
                if cancel(new_txt):
                    return 0
                if new_txt not in debilidades:
                    raise ValueError
                pokemon_["ATK"][ataque]["T"] = new_txt
            elif modif == "c" or modif == "C":
                new_num = input("Introduza o novo poder:\n")
                if cancel(new_num):
                    return 0
                if float(new_num) not in range(1,200):
                    raise ValueError
                pokemon_["ATK"][ataque]["P"] = float(new_num)
            elif modif == "d" or modif == "D":
                new_num = input("Introduza os novos action points:\n")
                if cancel(new_num):
                    return 0
                if int(new_num) not in range(1,11):
                    raise ValueError
                pokemon_["ATK"][ataque]["MAP"] = float(new_num)
                pokemon_["ATK"][ataque]["CAP"] = float(new_num)
            return
        except:
            print("Opción inválida.")

def modifiy(pokemon_modif: dict):
    """modifies an already existing pokemon.

    Args:
        pokemon (dict): selected pokemon 

    Raises:
        ValueError: If any of the values goes vobe the limit or there's an error
    """
    while True:
        try:
            pokemon_modif = [pokemon_modif]
            stats(pokemon_modif)
            pokemon_modif = pokemon_modif[0]
            print("Que desexa modificar?\n")
            modif = input("\na)Nome\nb)Tipo\nc)Ataques\n")
            if cancel(modif):
                return 0
            opc_list = ["a", "A", "b", "B", "c", "C"]
            if modif not in opc_list:
                raise ValueError     
            if modif == "a" or modif == "A":
                new_txt = input("Introduza o novo nome:\n")
                if cancel(new_txt):
                    return 0
                pokemon_modif["N"] = new_txt
            elif modif == "b" or modif == "B":
                new_txt = input("Introduza o novo tipo:\n")
                if cancel(new_txt):
                    return 0
                if new_txt not in debilidades:
                    raise ValueError
                pokemon_modif["T"] = new_txt
            elif modif == "c" or modif =="C":
                opc = input("Desexa engadir un novo ataque?(Y/N)\n")
                if cancel(opc):
                    return 0
                if opc == "Y" or opc == "y":
                    new_atk(pokemon_modif)
                elif opc == "n" or opc == "N":
                    modify_atk(pokemon_modif)
                else:
                    raise ValueError
            print("Cambios realizados!")
            pokemon_modif = [pokemon_modif]
            stats(pokemon_modif)
            pokemon_modif = pokemon_modif[0]
            break
        except:
            print("Opción inválida.")
    for pokemon in range(len(pokemons.pokemons)):
        if pokemons.pokemons[pokemon]["N"] == pokemon_modif["N"]:
            pokemons.pokemons[pokemon] == pokemon_modif
    pokemons_final = pokemons.pokemons
    json.dump(pokemons_final, open("ripper\pokemons_usable.json", "w"))
    return

def selec_opc():
    """Main menu of the editor, where the user selects what to do.

    Raises:
        ValueError: If any of the values goes vobe the limit or there's an error
    """
    while True:
        while True:
            opc = input("Que desexa facer?\na)Modificar pokemon\nb)Engadir novo pokemon\nc)Atrás\n")
            lista_opc = ["a", "A", "b", "B", "c", "C"]
            if opc in lista_opc:
                break
            else:
                print("Opción inválida, tente de novo.")
            
        if opc == "a" or opc == "A":
            while True:
                try:
                    show.display_gens()
                    selec = input("De que xeración é o pokemon?\n")
                    if cancel(selec):
                        return 0     
                    if int(selec) not in range(1, len(pokemons.gens)+1):
                        raise ValueError
                    keys = list(pokemons.gens.keys())
                    selec = keys[int(selec)-1]
                    pokemons_ = pokemons.gens[selec]
                    show.display_pokemons(pokemons_)
                    selec = input("Seleccione o pokemon que queres modificar (1, 2, 3...):\n")
                    if cancel(selec):
                        return 0
                    if int(selec) not in range(1, len(pokemons_)+1):
                        raise ValueError
                    pokemon_modif = pokemons_[int(selec)-1]
                    break
                except:
                    print("Opción inválida.")
            modifiy(pokemon_modif)
            break
        elif opc == "b" or opc == "B":
            new_pokemon()
            break
        elif opc == "c" or opc == "C":
            print("Saindo do editor...")
            break
    clear("cls")
    return 0