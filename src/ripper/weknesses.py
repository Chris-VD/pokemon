#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Small ripper to take the weaknesses chart.
'''

import json
from bs4 import BeautifulSoup
import requests

ChartPage_Raw = requests.get("https://pokemondb.net/type")
ChartPage = BeautifulSoup(ChartPage_Raw.content, "html.parser")
WeaknessList = {}

TableRaw = ChartPage.find("table", class_ = "type-table").find("tbody")
TableRows = TableRaw.findAll("tr")
for row in TableRows:
    Main_type = row.find("a").string
    WeaknessList[Main_type] = []
    CheckerList = row.findAll("td")
    for check in CheckerList:
        if check.string is not None and check.string == "2":
            strong = str(check["title"])
            strong = strong.replace(str(Main_type), "").replace(" = super-effective", "")[3:]
            WeaknessList[Main_type].append(strong)
json.dump(WeaknessList, open("Weaknesses.json", "w"))
