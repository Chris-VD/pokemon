#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Parser that takes the raw info from a json and adapts it to the game.
The created json will be the one used in game.
RAW:
    {"Number": , "N": "", "T": "", "ATK": "", "DEF": "", "SPD": "", "HP": "", "Moves": []} <- Pokemons
    {"N": "", "Unlock": "", "C": "", "T": "", "P": "", "ACC": "", "PP": ""} <- Ataques
GAME:
    {"N": "", "T": "", "LVL": "","DEF": "", "MHP": "", "CHP": "", "ATK": []} <- Pokemons
    {"N": "", "T": "", "P": "", "MAP": "", "CAP": ""} <- Ataques
'''

import json

Pokemons_raw = json.load(open(r"pokemons_raw.json"))
Pokemons = []
for pokemon in Pokemons_raw:
    try:
        new_attack_list = []
        attack_list = pokemon["Moves"]
        for attack in attack_list:
            new_attack = {"N": attack["N"], "T": attack["T"], "P": attack["P"], "MAP": (round(attack["PP"]) // 10), "CAP": ""}
            new_attack["CAP"] = new_attack["MAP"]
            new_attack_list.append(new_attack)
        new_pokemon = {"N": pokemon["N"], "T": pokemon["T"], "LVL": "", "DEF": pokemon["DEF"], "MHP": pokemon["HP"], "CHP": "", "ATK": new_attack_list}
        new_pokemon["CHP"] == new_pokemon["MHP"]
        Pokemons.append(new_pokemon)
    except:
        print(f"Error parsing {pokemon}, retrying...")
        try:
            new_pokemon = {"N": "ERROR", "T": "ERROR", "LVL": 00, "DEF": 00, "MHP": 00, "CHP": 00, "ATK": [{"N": "ERROR", "T": "ERROR", "P": 00, "MAP": 00, "CAP": 00}]}
            Pokemons.append(new_pokemon)
            print(f"{pokemon} will not be usable in battle but won't disturb the rest of pokemons.")        
            continue
        except:
            print(f"Fatal error. {pokemon} coud cause the program to fail.")

json.dump(Pokemons, open("pokemons_usable.json", "w"))
