import ninjaAPI
import poeAPI
import poeWatchAPI
import time
import csv
from tempfile import NamedTemporaryFile
import shutil

#  div card overview
# r = requests.get('https://poe.ninja/api/data/itemoverview?league=Heist&type=

CONSUMABLE_LIST = ['Fossil', 'DeliriumOrb', 'Scarab']
POE_WATCH_LIST = ['fossil', 'deliriumOrb', 'scarab']

def sort_by_profit_per(list):
    length = range(0, len(list) - 1)

    for i in length:
        min_value = i

        for k in range(i + 1, len(list)):
            if list[k].profitPer > list[min_value].profitPer:
                min_value = k

        if min_value != i:
            list[min_value], list[i] = list[i], list[min_value]
    return list


def update_consumables():
    while True:
        for consumable,poe_watch_target in zip(CONSUMABLE_LIST, POE_WATCH_LIST):
            avg_price_list = ninjaAPI.getOverview(consumable)
            if consumable == "Scarab":
                for scarab in avg_price_list:
                    if scarab.id.find('lure') != -1:
                        avg_price_list.remove(scarab)

            exa_price = ninjaAPI.getExaPrice()

            poeWatchAPI.getSupply(poe_watch_target, avg_price_list)

            with NamedTemporaryFile(mode='w', delete=False, newline='') as temp_log:
                log_writer = csv.writer(temp_log, delimiter=',')
                log_writer.writerow(['name', 'id', 'avgPrice', 'bulkQuant', 'profit', 'profitPer', 'supply', 'icon_url'])

                for item in avg_price_list:
                    if consumable == 'Scarab' and item.id.find('blight') == -1 and item.id.find('abyss') == -1:
                        item.id = item.id.replace('winged', 'jewelled')
                    print(item.id)
                    item.bulkQuant = poeAPI.getBulkQuant(item.id)
                    if item.bulkQuant == 0:
                        item.profit = 0
                        item.profitPer = 0
                    else:
                        item.profit = poeAPI.normalize(exa_price - (item.bulkQuant * item.avgPrice))
                        item.profitPer = poeAPI.normalize(item.profit / item.bulkQuant)
                    time.sleep(5)

                sort_by_profit_per(avg_price_list)
                for item in avg_price_list:
                    log_writer.writerow([item.name, item.id, item.avgPrice, item.bulkQuant, item.profit, item.profitPer, item.supply, item.icon])

            shutil.move(temp_log.name, consumable + '.csv')

update_consumables()
