import re

import numpy as np
import pandas as pd
import requests
from scipy import stats

from auth.auth import password, username


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
        some_math(prices)
    else:
        print(r.status_code)


def some_math(prices):
    # remove values that deviate from a norm
    # find
    df = pd.DataFrame(data={"A": prices})
    print(df)
    df_nonzero = df[df["A"] > 0]

    Q1 = df_nonzero["A"].quantile(0.25)
    Q3 = df_nonzero["A"].quantile(0.75)
    IQR = Q3 - Q1

    df_clean = df_nonzero[
        (df_nonzero["A"] >= Q1 - 1.5 * IQR) & (df_nonzero["A"] <= Q3 + 1.5 * IQR)
    ]

    print(df_clean.sort_values(by="A", ascending=False))
    # print(remove_bogus_values)


def main():
    get_price("RTX 5080")


if __name__ == "__main__":
    main()
