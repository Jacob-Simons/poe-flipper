import requests
import poeAPI
import pprint
import shutil
import os.path
from pathlib import Path


def getOverview(target):
    r = requests.get('https://poe.ninja/api/data/itemoverview?league=' + poeAPI.currLeague + '&type=' + target)
    avg_price_list = []

    for consumable in r.json()['lines']:
        price = consumable['chaosValue']
        id = consumable['detailsId']
        name = consumable['name']
        icon = consumable['icon']
        avg_price_list.append(poeAPI.consumable(id, price, name, icon))

    return avg_price_list

def getExaPrice():
    r = requests.get('https://poe.ninja/api/data/currencyoverview?league=' + poeAPI.currLeague + '&type=Currency')
    exaPrice = 0
    for currency in r.json()['lines']:
        if(currency['detailsId'] == 'exalted-orb'):
            exaPrice = currency['chaosEquivalent']
            break
    return exaPrice


