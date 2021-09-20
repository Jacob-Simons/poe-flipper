"""
ninjaAPI is the driver which handles all poe.ninja API requests.
"""
import requests
import poeAPI


def get_overview(target):
    """
    Grabs the item type overview for the specified target type from poe.ninja API.  It then creates a list of Consumables
    to represent the item data returned by the API.

    :param target: item type ID for API url
    :return: list of Consumables of specified item type with avg price, id, name, and icon url
    """
    r = requests.get('https://poe.ninja/api/data/itemoverview?league=' + poeAPI.currLeague + '&type=' + target)
    avg_price_list = []

    for consumable in r.json()['lines']:
        price = consumable['chaosValue']
        consumable_id = consumable['detailsId']
        name = consumable['name']
        icon = consumable['icon']
        avg_price_list.append(poeAPI.Consumable(consumable_id, price, name, icon))

    return avg_price_list


def get_exa_price():
    """
    Sends a get request to poe.ninja API for the currency overview to get the current exa price in chaos

    :return: returns an int representing the current exa price in chaos
    """
    r = requests.get('https://poe.ninja/api/data/currencyoverview?league=' + poeAPI.currLeague + '&type=Currency')
    exa_price = 0
    for currency in r.json()['lines']:
        if currency['detailsId'] == 'exalted-orb':
            exa_price = currency['chaosEquivalent']
            break
    return exa_price
