import requests
import poeAPI
import pprint
import shutil
import os.path
from pathlib import Path


def getOverview():
    r = requests.get('https://poe.ninja/api/data/itemoverview?league=' + poeAPI.currLeague + '&type=Fossil')
    fossilAvgPriceList = []

    for fossil in r.json()['lines']:
        price = fossil['chaosValue']
        id = fossil['detailsId']
        name = fossil['name']
        icon = fossil['icon']
        fossilAvgPriceList.append(poeAPI.consumable(id, price, name, icon))

    return fossilAvgPriceList

def getExaPrice():
    r = requests.get('https://poe.ninja/api/data/currencyoverview?league=' + poeAPI.currLeague + '&type=Currency')
    exaPrice = 0
    for currency in r.json()['lines']:
        if(currency['detailsId'] == 'exalted-orb'):
            exaPrice = currency['chaosEquivalent']
            break
    return exaPrice


