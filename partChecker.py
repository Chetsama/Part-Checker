import argparse
import re

import requests

from auth.auth import password, username

# defined command line options
# this also generates --help and error handling
CLI = argparse.ArgumentParser()
CLI.add_argument(
    "--list",  # name on the CLI - drop the `--` for positional/required parameters
    nargs="*",  # 0 or more values expected => creates a list
    type=str,
    default=["RTX5070", "64GB-DDR5-RAM"],  # default if nothing is provided
)
args = CLI.parse_args()


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
        "source": "amazon_search",
        "query": "{}".format(item),
        "geo_location": "GB",
        "parse": True,
    }

    # Get response.
    r = requests.request(
        "POST",
        "https://realtime.oxylabs.io/v1/queries",
        auth=(str(username), str(password)),
        json=payload,
    )

    print(r.headers.get("Content-Type"))
    if "json" in str(r.headers.get("Content-Type")):
        js = r.json()
        # print(str(js))
        prices = get_prices_from_json(js)
        print(prices)
        return prices

    else:
        print(r.status_code)


def some_math(prices):
    # remove values that deviate from a norm
    # find
    if not prices:  # Handle empty list case to avoid errors
        return 0

    # Filter out zero or negative prices (not valid)
    filtered_prices = [p for p in prices if p > 0]

    if not filtered_prices:
        return 0

    # Simple approach - just take the maximum price as original code did
    max_price = max(filtered_prices) if filtered_prices else 0
    print(max_price)
    return max_price


def main():
    total = 0
    items = len(args.list)
    for i in range(items):
        prices = get_price(args.list[i])

        total = total + some_math(prices)

    print("Your entire computer should set you back no more than... £" + str(total))


if __name__ == "__main__":
    main()
