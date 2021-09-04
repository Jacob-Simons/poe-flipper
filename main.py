import ninjaAPI
import poeAPI
import poeWatchAPI
import time
import csv
from tempfile import NamedTemporaryFile
import shutil


#  div card overview
# r = requests.get('https://poe.ninja/api/data/itemoverview?league=Heist&type=

FOSSIL_DATA_FILE_NAME = "fossil-data.csv"

def selectionSort(list):
    length = range(0, len(list) - 1)

    for i in length:
        min_value = i

        for k in range(i + 1, len(list)):
            if list[k].profitPerFossil > list[min_value].profitPerFossil:
                min_value = k

        if min_value != i:
            list[min_value], list[i] = list[i], list[min_value]
    return list


def update_fossils():
    while True:
        fossilAvgPriceList = ninjaAPI.getOverview()

        exa_price = ninjaAPI.getExaPrice()

        poeWatchAPI.getSupply('fossil', fossilAvgPriceList)

        with NamedTemporaryFile(mode='w', delete=False, newline='') as temp_log:
            log_writer = csv.writer(temp_log, delimiter=',')
            log_writer.writerow(['name', 'id', 'avgPrice', 'bulkQuant', 'profit', 'profitPerFossil', 'supply', 'icon_url'])

            for fossil in fossilAvgPriceList:
                fossil.bulkQuant = poeAPI.getBulkQuant(fossil.id)
                if fossil.bulkQuant == 0:
                    fossil.profit = 0
                    fossil.profitPerFossil = 0
                else:
                    fossil.profit = poeAPI.normalize(exa_price - (fossil.bulkQuant * fossil.avgPrice))
                    fossil.profitPerFossil = poeAPI.normalize(fossil.profit / fossil.bulkQuant)

                log_writer.writerow([fossil.name, fossil.id, fossil.avgPrice, fossil.bulkQuant, fossil.profit, fossil.profitPerFossil, fossil.supply, fossil.icon])
                time.sleep(5)

        shutil.move(temp_log.name, FOSSIL_DATA_FILE_NAME)


update_fossils()



