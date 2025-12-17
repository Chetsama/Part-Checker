import requests
from pprint import pprint
import re

def between(a,b, string):
    try:
        temp1 = re.split(a,string)
        out = re.split(b,temp1[1])
        return out[0]
    except:
        return "no value"


def get_prices_from_json(data):
    """
    Recursively extracts all 'price' values from a nested dictionary or list.
    """
    prices = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'price':
                prices.append(value)
            prices.extend(get_prices_from_json(value))
    elif isinstance(data, list):
        for item in data:
            prices.extend(get_prices_from_json(item))
    return prices

def get_price(item):

    # Structure payload.
    payload = {
        'source': 'google_search',
        'query': 'RTX 5070',
        'geo_location': 'GB',
        'parse': True
    }

    # Get response.
    response = requests.request(
        'POST',
        'https://realtime.oxylabs.io/v1/queries',
        auth=('username', 'pwd'),
        json=payload,
    )


    print(get_prices_from_json(response.json()))

def main():
    get_price("B07FZ8S74R")

if __name__=="__main__":
    main()