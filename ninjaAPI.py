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
        fossilAvgPriceList.append(poeAPI.fossil(id, price, name, icon))
        path = Path(os.path.dirname(os.path.abspath(__file__)))
        file_name = id + '.png'
        path = path / 'src' / 'static' / 'images' / file_name

        if not path.is_file():
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
    path = Path(os.path.dirname(os.path.abspath(__file__)))
    path = path / 'src' / 'static' / 'images'
    file_name = id + '.png'
    file_to_open = path / file_name
    print(file_name)
    with open(file_to_open, 'wb') as out_file:
        shutil.copyfileobj(r.raw, out_file)
    del r
