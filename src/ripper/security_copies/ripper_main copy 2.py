#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Ripper to extract info about pokemons from a pokedex html page.
Page: https://bulbapedia.bulbagarden.net
The script could be optimised if the page were a bit more organised but oh well.
BeautifulSoup only works sometimes, the .nextSibling and .children actions work like once every 5 tries and some paths I took are probably
not optimal and could be fone easier but again, oh well, the thing does it's only job.

POKEMONS NOT ADDED DUE TO TECHNICAL ISSUES (not mines):
- Starmie (/wiki/Starmie_(Pok%C3%A9mon))
'''

__author__ = "Christian Varela Docampo"

import json
from timeit import default_timer as timer
import requests
from bs4 import BeautifulSoup
from time import sleep

def import_poke(pokemon_link: str) -> dict:
    print(pokemon_link)
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
    # Firstly you gotta locate the text "By leveling up", which is isnide a <span> inside an <h3>, we .parent to get to the <h3> and the next table is the one we're looking for.
    # Within that table, the attacks are located inside another table with class = "sortable", and within that table in the <tbody>.
    # We just save every <tr> in a list now
    PokemonAttackList_Raw = Pokemon.find("span", id = "By_leveling_up").parent.findNextSibling("table", class_ = "roundy").find("table", class_ = "sortable").find("tbody").findAll("tr")
    # Now that we have the table, we check every <td>. If we assume the table is organised the same way for every pokemon, we follow the same order to extract the stats.
    AttackList = []
    for tr in PokemonAttackList_Raw:
        # Every <tr> is an attack, so we make a list of every stat of that attack (the <td>s)
        td_list = tr.findAll("td")
        # x is a counter to organise evrything, since the first td is always the level, the second the name...
        x = 0
        for td in td_list:
            x += 1
            # Some of the attack stats are inside a <span> tag and other aren't, to avoid tris nuisance we jsut do this try.
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
                # Te accuracy has weird values when it's 0%, so we just chekc if it's a number and if it isn't we set it to 0.      
                try:
                    AttackAccuracy = int(content)
                except:
                    AttackAccuracy = 0
            elif x == 7:
                AttackPowerPoints = int(content)
        # This is inside a try since the very first <tr> isn't actually an attack, and idk how to ignore it :3
        try:
            AttackStats = {"N": AttackName, "Unlock": AttackLevelUnlock, "C": AttackCategory, "T": AttackType, "P": AttackPower, "MAP": 7 - round(AttackPowerPoints/10), "CAP": "", "ACC": AttackAccuracy}
            AttackList.append(AttackStats)
        except:
            continue

    # Once absolutely everything is done, we just create the pokemon...
    PokemonFull = {"Number": PokemonNumber,"N": PokemonName, "T": PokemonType, "DEF": PokemonDEF, "LVL": 99, "MHP": PokemonHP, "CHP": PokemonHP, "ATK": AttackList}
    # And append it to a list full of pokemons.
    PokemonFullList.append(PokemonFull)
    print(PokemonFull["Number"], PokemonFull["N"])

PokemonFullList = []
# Get whole page
MainPokemonPage_Raw = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number")
MainPokemonPage = BeautifulSoup(MainPokemonPage_Raw.content, "html.parser")
link_list = []
# Get every single table, they contain the pokemons of each gen
table_list_raw = MainPokemonPage.findAll("table")

# Check every table one by one
for table in table_list_raw:
    # Get every <tr> tag inside evry table (every pokemon)
    poke_list_raw = table.findAll("tr")
    # Check every single <tr> tag
    for tr in poke_list_raw:
        # Get the "href" value for the first <a> tag inside the <tr>
        a = tr.find("a", href = True)
        # Some <a> tags don't have "href", thus we do this to not deal with that.
        try:
            href = a["href"]
        except:
            continue
        # If the "href" contains the string "(Pok%C3%A9mon)", it means it's a Pokemon link, so we save it in the link_list
        if "(Pok%C3%A9mon)" in str(href):
            link_list.append(href)

# Delete the liks that repeat inside of the list
sorted = False
print(f"{len(link_list)} possible links found...")
while not sorted:
    sorted = True
    for i in link_list:
        try:
            if i == link_list[link_list.index(i)+1]:
                link_list.pop(link_list.index(i)+1)
                sorted = False
        except:
            print("Sorting...")
            continue

print(f"{len(link_list)} pokemons to import...")
sleep(2)

# start_time and end_time are used to calculate time_elapsed, this is just the time it took the program to rip every pokemon.
start_time = timer()

x, y = 0, 0
# Check the pokemon list and rip each one by one
for pokemon in link_list:
    # This is inside a try because there's a table that rases an error and I don't wanna deal with it, so we just do this
    try:
        # tries:
        x += 1
        import_poke(pokemon)
        # successes:
        y += 1
    except:
        print(f"There was an error ripping {pokemon}, continuing...")
        PokemonFullList.append({"Number": ("#0" + str(x))})
        sleep(1)
        continue

end_time = timer()
time_elapsed = float(end_time) - float(start_time)

# Once evrything's stored in a list and ready, we dump it inside a json.
json.dump(PokemonFullList, open("single_pokemon.json", "w"))
print(f"{x} tries, {y} succesful.\n{len(PokemonFullList)} pokemons ripped, out of {len(link_list)} total posibles.\nProgram completed in {round(time_elapsed)} seconds.\nClosing ripper...")
exit()