import requests
import time
import pprint
import constants


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

HEADERS = {"User-Agent": constants.POE_API_HEADER}

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

    invalid_response_code = True
    while invalid_response_code:
        try:
            r = requests.post(urlSearch1, json=payload, headers=HEADERS)
            invalid_response_code = False

            if r.status_code == 200:
                invalid_response_code = False
            else:
                print(r.headers['X-Rate-Limit-Ip-State'])
                state1 = r.headers['X-Rate-Limit-Ip-State']
                state1 = state1[state1.find(':') + 1:]
                state1 = state1[state1.find(':') + 1:state1.find(',')]
                state2 = r.headers['X-Rate-Limit-Ip-State']
                state2 = state2[state2.find(',') + 1:]
                state2 = state2[state2.find(':') + 1:]
                state2 = state2[state2.find(':') + 1:]
                if int(state1) > int(state2):
                    time.sleep(int(state1) + 5)
                else:
                    time.sleep(int(state2) + 5)
        except requests.exceptions.RequestException as e:
            print(e)
            time.sleep(10)

    time.sleep(5)
    urlID = r.json()['id']
    if len(r.json()['result']) == 0:
        return 0
    resultLine = r.json()['result'][0]
    urlSearch2 = BASE_FETCH + resultLine + QUERY + urlID
    invalid_response_code = True
    while invalid_response_code:
        try:
            r = requests.get(urlSearch2, headers=HEADERS)
            if r.status_code == 200:
                invalid_response_code = False
            else:
                print(r.headers['X-Rate-Limit-Ip-State'])
                state1 = r.headers['X-Rate-Limit-Ip-State']
                state1 = state1[state1.find(':') + 1:]
                state1 = state1[state1.find(':') + 1:state1.find(',')]
                state2 = r.headers['X-Rate-Limit-Ip-State']
                state2 = state2[state2.find(',') + 1:]
                state2 = state2[state2.find(':') + 1:]
                state2 = state2[state2.find(':') + 1:]
                if int(state1) > int(state2):
                    time.sleep(int(state1) + 5)
                else:
                    time.sleep(int(state2) + 5)

        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(e)
            time.sleep(10)

    if r.json() is None:
        return 0

    exa = r.json()['result'][0]['listing']['price']['exchange']['amount']
    quant = r.json()['result'][0]['listing']['price']['item']['amount']
    bulkQuant = quant / exa
    return normalize(bulkQuant)


def normalize(num):
    num = float(f'{round(num, 2):g}')
    if num.is_integer():
        int(num)
    return num
