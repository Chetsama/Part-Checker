import re

import requests

from auth.auth import password, username


def between(a, b, string):
    try:
        temp1 = re.split(a, string)
        out = re.split(b, temp1[1])
        return out[0]
    except:
        return "no value"


def clean_price(price_value):
    """
    Cleans a price value by removing '£' and apostrophes, and converting to a numeric type.
    """
    if isinstance(price_value, (int, float)):
        return price_value
    if isinstance(price_value, str):
        cleaned = price_value.replace("£", "").replace("'", "").strip()
        try:
            # Try to convert to float first to handle decimals
            return float(cleaned)
        except ValueError:
            # If not a float, return the cleaned string
            return cleaned
    return price_value

def get_prices_from_json(data):
    """
    Recursively extracts all 'price' values from a nested dictionary or list.
    """
    prices = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "price":
                prices.append(clean_price(value))
            prices.extend(get_prices_from_json(value))
    elif isinstance(data, list):
        for item in data:
            prices.extend(get_prices_from_json(item))
    return prices


def get_price(item):
    # Structure payload.
    payload = {
        "source": "google_search",
        "query": "{}".format(item),
        "geo_location": "GB",
        "parse": True,
    }

    # Get response.
    response = requests.request(
        "POST",
        "https://realtime.oxylabs.io/v1/queries",
        auth=(str(username), str(password)),
        json=payload,
    )

    print(get_prices_from_json(response.json()))


def main():
    get_price("RTX 5080")


if __name__ == "__main__":
    main()
