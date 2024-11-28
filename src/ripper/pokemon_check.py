#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Check if all the 1025 pokemons are ripped.
'''

__author__ = "Christian Varela Docampo"

import json

def check():
    """
    Checks if the list of pokemons is full or if there's any missing
    """
    # Opens the raw list of pokemon
    Pokemons = json.load(open(r"pokemons_raw.json"))
    x = 0
    succ = 0

    for i in Pokemons:
        # Goes one by one checking for the pokemon's number
        x += 1
        poke_num = int(i["Number"][1:5])
        if poke_num != x:
            # If any pokemon is missing, it displays it
            print(f"Error!, missing pokemon #{x}")
        else:
            succ += 1

    print(f"{succ} successes!")