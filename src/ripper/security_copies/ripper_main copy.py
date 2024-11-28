#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Ripper para coller información dsa páxinas html.
'''

__author__ = "Christian Varela Docampo"

from time import sleep
import requests
from bs4 import BeautifulSoup
from random import randint

def import_poke(pokemon_link: str) -> dict:
    # Get the page of the Pokemon we're importing
    main_link = "https://bulbapedia.bulbagarden.net"+str(pokemon_link)
    Pokemon_Raw = requests.get(main_link)
    Pokemon = BeautifulSoup(Pokemon_Raw.content, "html.parser")
    # The name of the Pokemon is inside the <div> with class_ = "mw-parser-output", so we save it
    PokemonName = Pokemon.find("div", class_ = "mw-parser-output").find("b").string
    # The number of the Pokemon is inside an <a> tag with title = "||", but there's several of these so we save all
    PokemonNumber = Pokemon.findAll("a", title = "List of Pokémon by National Pokédex number")
    # Check every <a> tag with title = "||"
    for a in PokemonNumber:
        # Get the string of text inside every <a>
        content = a.find("span").string
        # If the string does not consist of only letters, it's the Pokemon number, so we save it
        if not str(content).isalpha():
            PokemonNumber = content
            break
    # The Pokemon type is, for whatever reason, hard as shit to find. The path is something like this:
    # Inside the same div as the Name and Number, inside the firt table with class_ = "roundy", get all <td> tags
    PokemonType = Pokemon.find("div", class_ = "mw-parser-output").find("table", class_ = "roundy").findAll("td")
    # Search for a specific <td> tag that checks the conditions:
    for td in PokemonType:
        # In the first of its <a> tags...
        a = td.find("a")
        if a == None:
            continue
        # Has a "href" atribute...
        href = a.get("href")
        # With a value of "/wiki/Type"
        if str(href) == "/wiki/Type":
            # If all of those check out, in the first <table> tag of the <td>...
            table = td.find("table")
            # The first <b> tag is the Type!
            PokemonType = table.find("b").string
            # It's convoluted as fuck and I'm sure there are better ways of doing it, but I couldn't find any so yah
    # The stat table has an <a> tag with href = "/wiki/Stat", so we find that and to get the full table we just .parent*3
    PokemonStats_Table = Pokemon.find("a",  href = "/wiki/Stat").parent.parent.parent
    # Every stat of the table can be located the same way:
    PokemonHP = PokemonStats_Table.find("a", href = "/wiki/HP").parent.nextSibling.string
    PokemonATK = PokemonStats_Table.find("a", href = "/wiki/Stat#Attack").parent.nextSibling.string
    PokemonDEF = PokemonStats_Table.find("a", href = "/wiki/Stat#Defense").parent.nextSibling.string
    PokemonSPD = PokemonStats_Table.find("a", href = "/wiki/Stat#Speed").parent.nextSibling.string
    PokemonStats = {"HP": PokemonHP, "ATK": PokemonATK, "DEF": PokemonDEF, "SPD": PokemonSPD}
    # Uhhh the attack list is also convoluted to find.
    # Firstly you gotta locate the text "By leveling up", which is isnide a <span> inside an <h3>, we .parent to get to the <h3> andthe next table is the one we're looking for.
    # Within that table, the attacks are located inside another table with class = "sortable", and within that table in the <tbody>.
    # Sidenote, for whatever reason BS completely ignores the structure of the web and adds a <tr> that should be inside <thead> to the <tbody>,
    # which makes everything a bit more annoying. Anyhow, this is the main attacks table with an added <tr> that we'll ignore later:
    PokemonAttackList_Raw = Pokemon.find("span", id = "By_leveling_up").parent.findNextSibling("table", class_ = "roundy").find("table", class_ = "sortable").find("tbody").findAll("tr")
    # Now that we have the table, we check every <td>. If we assume the table is organised the same way for every pokemon, we follow the same order to extract the stats.
    AttackList = []
    for tr in PokemonAttackList_Raw:
        td_list = tr.findAll("td")
        x = 0
        for td in td_list:
            x += 1
            try:
                content = td.find("span").string
            except:
                content = td.string
            if x == 1:
                AttackLevelUnlock = content
            elif x == 2:
                AttackName = str(content)
            elif x == 3:
                AttackType = str(content)
            elif x == 4:
                AttackCategory = content
            elif x == 5:
                AttackPower = int(content)
            elif x == 6:            
                try:
                    AttackAccuracy = int(content)
                except:
                    AttackAccuracy = 0
            elif x == 7:
                AttackPowerPoints = int(content)
        try:
            AttackStats = {"Name": AttackName, "Type": AttackType, "Power": AttackPower, "Accuracy": AttackAccuracy, "Power Points": AttackPowerPoints}
            AttackList.append(AttackStats)
        except:
            continue
    PokemonFull = {"N": PokemonName, "T": PokemonType, "LVL": 99, "MHP": PokemonHP, "CHP": PokemonHP, "ATK": AttackList}
    print(PokemonFull)

# Get whole page
MainPokemonPage_Raw = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number")
MainPokemonPage = BeautifulSoup(MainPokemonPage_Raw.content, "html.parser")
link_list = []
# List of every <a> tag inside the first <table> whete class_ = "roundy", this is the table for the first generation pokemon
link_list_raw = MainPokemonPage.find("table", class_ = "roundy").findAll("a")
# Check every single <a> tag
for link in link_list_raw:
    # Get the "href" value for each <a> tag
    href = link.get("href")
    # If the "href" contains the string "(Pok%C3%A9mon)", it means it's a Pokemon link, so we save it in the link_list
    if "(Pok%C3%A9mon)" in str(href):
        link_list.append(href)
# Delete the liks that repeat inside of the list
link_list = list(set(link_list))

import_poke(link_list[randint(1,100)])
