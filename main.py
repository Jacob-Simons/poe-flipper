import ninjaAPI
import poeAPI
import poeWatchAPI
import gui
import time
import threading


#  div card overview
# r = requests.get('https://poe.ninja/api/data/itemoverview?league=Heist&type=DivinationCard')

def selectionSort(list):
    length = range(0, len(list) - 1)

    for i in length:
        min_value = i

        for j in range(i + 1, len(list)):
            if list[j].profitPerFossil > list[min_value].profitPerFossil:
                min_value = j

        if min_value != i:
            list[min_value], list[i] = list[i], list[min_value]
    return list


def update_fossils():
    while True:
        global fossilAvgPriceList
        fossilAvgPriceList = ninjaAPI.getOverview()

        exa_price = ninjaAPI.getExaPrice()

        poeWatchAPI.getSupply('fossil', fossilAvgPriceList)

        for fossil in fossilAvgPriceList:
            fossil.bulkQuant = poeAPI.getBulkQuant(fossil.id)
            if fossil.bulkQuant == 0:
                fossil.profit = 0
                fossil.profitPerFossil = 0
            else:
                fossil.profit = exa_price - (fossil.bulkQuant * fossil.avgPrice)
                fossil.profitPerFossil = fossil.profit / fossil.bulkQuant
            time.sleep(5)

        fossilAvgPriceList = selectionSort(fossilAvgPriceList)
        global updated
        updated = True


def update_gui_loop():
    global updated
    global fossilAvgPriceList
    if updated:
        gui.updateGUI(fossilAvgPriceList)
        updated = False

    gui.root.after(20, update_gui_loop)


fossilAvgPriceList = []
updated = False

t1 = threading.Thread(target=update_fossils)
t1.start()
gui.root.after(20, update_gui_loop)

gui.root.mainloop()



