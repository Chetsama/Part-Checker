import re
from typing import Any, Dict, List

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Initialize the FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="frontend/src/templates")
app.mount(
    "/static", StaticFiles(directory="/mnt/c/Projects/PartChecker"), name="static"
)


# Import functions from partChecker.py to use actual API logic instead of mock values
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Try importing the auth module properly
    from auth.auth import password, username
except ImportError:
    # Fallback to default credentials if needed for testing purposes (not secure in production)
    password = "4M~ZlJbnplJ~~3"
    username = "venomous_w4NVg"

import requests


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


def get_price(item: str) -> List[float]:
    """
    Get price information for a part by calling the actual API.
    This function replaces the mock implementation with real API calls.
    """
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

    if "json" in str(r.headers.get("Content-Type")):
        js = r.json()
        prices = get_prices_from_json(js)
        return prices

    else:
        print(r.status_code)
        return []


def calculate_part_price(prices: List[float]) -> float:
    """
    Calculate the price of a single part - using maximum price as per original logic.
    """
    if not prices:  # Handle empty list case to avoid errors
        return 0.0

    # Filter out zero or negative prices (not valid)
    filtered_prices = [p for p in prices if p > 0]

    if not filtered_prices:
        return 0.0

    # Simple approach - just take the maximum price as original code did
    max_price = max(filtered_prices) if filtered_prices else 0.0
    return round(max_price, 2)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/calculate", response_class=HTMLResponse)
async def calculate_prices(request: Request, parts: str = Form(...)):
    try:
        # Split the input into individual parts
        part_list = [p.strip() for p in parts.split("\n") if p.strip()]

        if not part_list:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "error": "Please enter at least one computer part.",
                },
            )

        results = []
        total_price = 0.0

        # Process each part
        for part in part_list:
            try:
                # Get prices (mock implementation)
                prices = get_price(part)

                # Calculate the price for this part
                calculated_price = calculate_part_price(prices)

                results.append({"part": part, "price": calculated_price})
                total_price += calculated_price

            except Exception as e:
                # If there's an error with one part, continue with others
                print(f"Error processing part '{part}': {str(e)}")
                results.append(
                    {"part": part, "price": 0.0}
                )  # Add zero price for failed parts

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "results": results,
                "total_price": round(total_price, 2),
                "error": None,
            },
        )

    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": f"An error occurred during processing: {str(e)}",
            },
        )


if __name__ == "__main__":
    # This will not be used directly since we run with uvicorn
    print("Backend server initialized")
