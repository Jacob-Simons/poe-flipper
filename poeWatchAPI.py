import requests
import poeAPI


def get_supply(item_id, item_list):
    """
        Gathers the daily supply data for each item in the item_list.

        param:  item_list - list of Consumables
                item_id - category ID for the poe.watch API url
    """
    response = requests.get('https://api.poe.watch/get?category=' + item_id + '&league=' + poeAPI.currLeague)
    total_supply = 0
    for item_list in item_list:
        for poe_watch_list in response.json():
            if item_list.name == poe_watch_list['name']:
                item_list.supply = poe_watch_list['daily']
                total_supply += poe_watch_list['daily']
                break
