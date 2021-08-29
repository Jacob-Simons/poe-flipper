import requests
import poeAPI
import pprint
import shutil
import os.path

def getOverview():
    r = requests.get('https://poe.ninja/api/data/itemoverview?league=' + poeAPI.currLeague + '&type=Fossil')
    fossilAvgPriceList = []

    for fossil in r.json()['lines']:
        price = fossil['chaosValue']
        id = fossil['detailsId']
        name = fossil['name']
        icon = fossil['icon']
        fossilAvgPriceList.append(poeAPI.fossil(id, price, name, icon))
        icon_exists = os.path.isfile(id + '.png')
        if not icon_exists:
            download_icon(icon, id)
    return fossilAvgPriceList

def getExaPrice():
    r = requests.get('https://poe.ninja/api/data/currencyoverview?league=' + poeAPI.currLeague + '&type=Currency')
    exaPrice = 0
    for currency in r.json()['lines']:
        if(currency['detailsId'] == 'exalted-orb'):
            exaPrice = currency['chaosEquivalent']
            break
    return exaPrice

def download_icon(url, id):
    r = requests.get(url, stream=True)
    with open(id + '.png', 'wb') as out_file:
        shutil.copyfileobj(r.raw, out_file)
    del r