#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Ripper para coller información dsa páxinas html.
'''

__author__ = "Christian Varela Docampo"

import requests
from bs4 import BeautifulSoup

MainPokemonPage_Raw = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number")
MainPokemonPage = BeautifulSoup(MainPokemonPage_Raw.content, "html.parser")
link_list = []
table_list_raw = MainPokemonPage.findAll("table")
for table in table_list_raw:
    link_list_raw = table.findAll("a")
    for link in link_list_raw:
        href = link.get("href")
        if "(Pok%C3%A9mon)" in str(href):
            link_list.append(href)
    link_list = list(set(link_list))
    for i in link_list:
        print(i)
print(len(link_list))
