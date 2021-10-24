"""
poeAPI is the driver which handles all official POE trade API requests.  The Consumable class is defined to represent
all flippable items with their important characteristics.  In order to get the price for an item from the POE trade API
first a post to the 'BASE_SEARCH' with an item payload must be sent.  The returned value of the BASE_SEARCH must be then
use to send a get request from the 'BASE_FETCH' which will contain the item pricing.
"""
import requests
import time
import constants


class Consumable:
    def __init__(self, item_id, avg_price, name, icon):
        self.item_id = item_id
        self.avgPrice = avg_price
        self.name = name
        self.icon = icon
        self.supply = 0
        self.bulk_quant = 0
        self.profit = 0
        self.profit_per = 0


# API URLs
BASE_SEARCH = 'http://www.pathofexile.com/api/trade/exchange/'
BASE_FETCH = 'https://www.pathofexile.com/api/trade/fetch/'
QUERY = '?exchange=true&query='

# OAuth2 identification
HEADERS = {"User-Agent": constants.POE_API_HEADER}

# grabbing current league
r = requests.get('https://www.pathofexile.com/api/trade/data/leagues', headers=HEADERS)
currLeague = r.json()['result'][0]['id']

# first url to post item data to
url_search1 = BASE_SEARCH + currLeague
DEFAULT_DELAY = 10


def get_bulk_quant(item_name):
    """
    Finds the total amount of the specified item for a 1ex bulk sell.

    :param item_name: name of the item to trade
    :return: returns an int with the total amount for a bulk sell.  If there is no listings for the item then it will
             return 0.
    """
    payload = {
      "exchange": {
        "want": [""],
        "have": ["exa"],
        "status": "online"
      }
    }

    payload["exchange"]["want"][0] = item_name

    response = process_post(url_search1, payload)

    time.sleep(DEFAULT_DELAY)
    url_id = response.json()['id']
    if len(response.json()['result']) == 0:
        return 0
    result_line = response.json()['result'][0]
    url_search2 = BASE_FETCH + result_line + QUERY + url_id
    response = process_get(url_search2)

    time.sleep(DEFAULT_DELAY)
    if response.json() is None:
        return 0

    exa = response.json()['result'][0]['listing']['price']['exchange']['amount']
    quant = response.json()['result'][0]['listing']['price']['item']['amount']
    bulk_quant = quant / exa
    return normalize(bulk_quant)


def process_get(target_url):
    """
    Handles get requests with the official POE trade API.  This is for sending requests to the first fetch url.

    The request will loop indefinitely until it succeeds and gets a 200 (OK) response code.  If the loop fails it will
    automatically check the response header and conform to the rate limit specifications.  There is a default delay
    between requests of 5 seconds to prevent hitting the rate limit.  It will also catch and ignore connection reset
    errors to prevent crashing.

    :param target_url: URL to send request to.
    :return: returns the response from the API.
    """
    invalid_response_code = True
    while invalid_response_code:
        try:
            response = requests.get(target_url, headers=HEADERS)
            print(response.status_code)
            wait_time = parse_rate_limit(response.headers['X-Rate-Limit-Ip'])
            print(wait_time)
            if response.status_code == 200:
                invalid_response_code = False
                time.sleep(wait_time)
            elif response.status_code == 429:
                state1 = response.headers['X-Rate-Limit-Ip-State']
                state1 = state1[state1.find(':') + 1:]
                state1 = state1[state1.find(':') + 1:state1.find(',')]
                state2 = response.headers['X-Rate-Limit-Ip-State']
                state2 = state2[state2.find(',') + 1:]
                state2 = state2[state2.find(':') + 1:]
                state2 = state2[state2.find(':') + 1:]
                if int(state1) > int(state2):
                    time.sleep(int(state1) + 1)
                else:
                    time.sleep(int(state2) + 1)

        except requests.exceptions.RequestException as e:
            print(e)
            time.sleep(DEFAULT_DELAY)
    return response


def process_post(target_url, payload):
    """
        Handles post requests with the official POE trade API.  This is for sending requests to the second fetch url.

        The request will loop indefinitely until it succeeds and gets a 200 (OK) response code.  If the loop fails it will
        automatically check the response header and conform to the rate limit specifications.  There is a default delay
        between requests of 5 seconds to prevent hitting the rate limit.  It will also catch and ignore connection reset
        errors to prevent crashing.

        :param target_url: URL to send request to.
        :return: returns the response from the API.
        """
    invalid_response_code = True
    while invalid_response_code:
        try:
            response = requests.post(target_url, json=payload, headers=HEADERS)
            print(response.status_code)

            wait_time = parse_rate_limit(response.headers['X-Rate-Limit-Ip'])
            print(wait_time)

            if response.status_code == 200:
                invalid_response_code = False
                time.sleep(wait_time)
            elif response.status_code == 429:
                state1 = response.headers['X-Rate-Limit-Ip-State']
                state1 = state1[state1.find(':') + 1:]
                state1 = state1[state1.find(':') + 1:state1.find(',')]
                state2 = response.headers['X-Rate-Limit-Ip-State']
                state2 = state2[state2.find(',') + 1:]
                state2 = state2[state2.find(':') + 1:]
                state2 = state2[state2.find(':') + 1:]
                if int(state1) > int(state2):
                    time.sleep(int(state1) + 1)
                else:
                    time.sleep(int(state2) + 1)
            else:
                time.sleep(DEFAULT_DELAY)

        except requests.exceptions.RequestException as e:
            print(e)
            time.sleep(DEFAULT_DELAY)
    return response


def normalize(num):
    """
    Normalize fixes the passed float and removes decimals past the 2nd point or if
    the number is an whole number it will convert it into an int.

    :param num: float that needs to be rounded to 2nd decimal place
    :return: returns the original num rounded and converted to an int if there are no decimals.
    """
    num = float(f'{round(num, 2):g}')
    if num.is_integer():
        num = int(num)
    return num

def parse_rate_limit(rate):
    max_wait = 0
    rate += ',.'
    while rate.find(",") != -1:
        first_colon = rate.find(":")
        second_colon = rate.find(":", first_colon + 1)
        max_requests = int(rate[0:first_colon])
        time_interval = int(rate[first_colon + 1:second_colon])
        wait = time_interval / max_requests
        max_wait = max(max_wait, wait)
        rate = rate[rate.find(",") + 1:]
    return max_wait + 1
