"""
    Central driver for script that collects data from PoE APIs and stores it into csvs .

    Main is based around the function update_consumables which runs in an infinite loop.  It gathers
    a list of data for all fossils, delirium orbs, and scarabs from ninjaAPI driver along with current
    exalt price.  Then each item's bulk trade quantity for 1 exa is collected from the poeAPI driver.
    Next the supply within the last 24 hours for each item is collected off of poeWatch driver.  Lastly, all of the data
    is dumped into separate respective csv files (Fossil.csv, DeliriumOrb.csv, Scarab.csv) and the loop restarts.
"""
import ninjaAPI
import poeAPI
import poeWatchAPI
import csv
from tempfile import NamedTemporaryFile
import shutil

# URL IDs for official PoE API
CONSUMABLE_LIST = ['Fossil', 'DeliriumOrb', 'Scarab']
# URL IDs for poe.watch API
POE_WATCH_LIST = ['fossil', 'deliriumOrb', 'scarab']


def sort_by_profit_per(consumable_list):
    """ Takes in a list of Consumable objects and sorts them by profit_per least to greatest """
    length = range(0, len(consumable_list) - 1)

    for i in length:
        min_value = i

        for k in range(i + 1, len(consumable_list)):
            if consumable_list[k].profit_per > consumable_list[min_value].profit_per:
                min_value = k

        if min_value != i:
            consumable_list[min_value], consumable_list[i] = consumable_list[i], consumable_list[min_value]
    return consumable_list


def update_consumables():
    """
        Main looping function that connects all other drivers.

        update_consumables is an infinite loop that collects data with the ninjaAPI, poeWatchAPI, and poeAPI drivers.
        The loop iterates through the 'CONSUMABLE_LIST' collecting data for each item type and storing it into csvs.
        It gets a list of consumable objects from ninjaAPI's get_overview that has all item names, ids, and avg price
        along with current exalt price for the item type passed from 'CONSUMABLE_LIST'. Then the list is passed to
        poeWatchAPI where the daily supply for each item is collected. Next the list is passed to poeAPI where the bulk
        trade quant is collected for each consumable in the list. Lastly, the list is exported into it's respective csv
        (overwriting any previous data) and iterates to the next type of consumable.
    """
    while True:
        for consumable, poe_watch_target in zip(CONSUMABLE_LIST, POE_WATCH_LIST):
            avg_price_list = ninjaAPI.get_overview(consumable)
            if consumable == "Scarab":
                for scarab in avg_price_list:
                    if scarab.item_id.find('lure') != -1:
                        avg_price_list.remove(scarab)

            exa_price = ninjaAPI.get_exa_price()

            poeWatchAPI.get_supply(poe_watch_target, avg_price_list)

            with NamedTemporaryFile(mode='w', delete=False, newline='') as temp_log:
                log_writer = csv.writer(temp_log, delimiter=',')
                log_writer.writerow(['name', 'id', 'avgPrice', 'bulkQuant', 'profit', 'profitPer', 'supply', 'icon_url'])

                for item in avg_price_list:
                    if consumable == 'Scarab' and item.item_id.find('blight') == -1 and item.item_id.find('abyss') == -1 and item.item_id.find('expedition') == -1:
                        item.item_id = item.item_id.replace('winged', 'jewelled')
                    print(item.item_id)
                    item.bulk_quant = poeAPI.get_bulk_quant(item.item_id)
                    if item.bulk_quant == 0:
                        item.profit = 0
                        item.profit_per = 0
                    else:
                        item.profit = poeAPI.normalize(exa_price - (item.bulk_quant * item.avgPrice))
                        item.profit_per = poeAPI.normalize(item.profit / item.bulk_quant)

                sort_by_profit_per(avg_price_list)
                for item in avg_price_list:
                    log_writer.writerow([item.name, item.item_id, item.avgPrice, item.bulk_quant, item.profit, item.profit_per, item.supply, item.icon])

            shutil.move(temp_log.name, consumable + '.csv')


update_consumables()
