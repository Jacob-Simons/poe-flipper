import requests
import poeAPI
import pprint

def getSupply(item_id, item_list):
    r = requests.get('https://api.poe.watch/get?category=' + item_id + '&league=' + poeAPI.currLeague)
    total_supply = 0
    print(r.json())
    for item_list in item_list:
        for poe_watch_list in r.json():
            if item_list.name == poe_watch_list['name']:
                item_list.supply = poe_watch_list['daily']
                total_supply += poe_watch_list['daily']
                break