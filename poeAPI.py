import requests
import time
import pprint


class consumable:
    def __init__(self, id, avgPrice, name, icon):
        self.id = id
        self.avgPrice = avgPrice
        self.name = name
        self.icon = icon
        self.supply = 0
        self.bulkQuant = 0
        self.profit = 0
        self.profitPer = 0


BASE_SEARCH = 'http://www.pathofexile.com/api/trade/exchange/'
BASE_FETCH = 'https://www.pathofexile.com/api/trade/fetch/'
QUERY = '?exchange=true&query='

HEADERS = {"User-Agent": "Bulk Flipper/1.0 (+poponoodles@gmail.com)"}

# grabbing current league
r = requests.get('https://www.pathofexile.com/api/trade/data/leagues', headers=HEADERS)
currLeague = r.json()['result'][0]['id']
urlSearch1 = BASE_SEARCH + currLeague



def getBulkQuant(itemName):

    payload = {
      "exchange": {
        "want": [ ""
        ],
        "have": [ "exa"
        ],
        "status": "online"
      }
    }

    payload["exchange"]["want"][0] = itemName

    HEADERS = {"User-Agent": "OAuth Bulk Flipper/1.0 (+poponoodles@gmail.com)"}
    invalid_response_code = True
    while invalid_response_code:
        r = requests.post(urlSearch1, json=payload, headers=HEADERS)
        #pprint.pprint(r.headers)
        if r.status_code != 406:
            invalid_response_code = False
        else:
            time.sleep(300)

    time.sleep(5)
    urlID = r.json()['id']
    if len(r.json()['result']) == 0:
        return 0
    resultLine = r.json()['result'][0]
    urlSearch2 = BASE_FETCH + resultLine + QUERY + urlID
    r = requests.get(urlSearch2, headers=HEADERS)
    exa = r.json()['result'][0]['listing']['price']['exchange']['amount']
    quant = r.json()['result'][0]['listing']['price']['item']['amount']
    bulkQuant = quant / exa
    return normalize(bulkQuant)


def normalize(num):
    num = float(f'{round(num, 2):g}')
    if num.is_integer():
        int(num)
    return num
