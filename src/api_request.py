import requests
import json
from assets.constants import ALL_LOCATIONS
from datetime import datetime, timedelta


def make_request():
    # Get api info
    with open("assets/api_info.json") as f:
        api_info = json.load(f)

    # Get all item ids
    with open("assets/items.json") as f:
        items_info = json.load(f)

    # Variable to hold all raw data returned at the end of the loop
    raw_data = []

    # Counter to keep track of item count per request
    counter = 0

    # Make item id string for this loop
    raw_ids = ""

    # Requesting 135 items at a time until all items are requested
    for item in items_info:
        # Make this loop's id string
        counter += 1
        raw_ids += item["UniqueName"] + ","
        if counter == 135:
            ids = raw_ids.rstrip(",")
            counter = 0

            # Making API request
            current_prices_request_url = (
                api_info["base_url"] + api_info["endpoints"]["current_prices"]
            )
            formatted_current_prices_url = current_prices_request_url.format(
                item_ids=ids,
                locations=ALL_LOCATIONS,
            )
            current_prices_response = requests.get(formatted_current_prices_url)

            # Add new response to final data
            raw_data.extend(current_prices_response.json())

            # Reset id string
            raw_ids = ""

    with open("data/raw_prices.json", "w") as f:
        json.dump(raw_data, f)


def request_history() -> None:
    # Get api info
    with open("assets/api_info.json") as f:
        api_info = json.load(f)

    # Get all item ids
    with open("assets/items.json") as f:
        items_info = json.load(f)

    # Getting date of last week and today, plus formatting
    today = datetime.today()
    week_ago = today - timedelta(days=7)
    today_str = today.strftime("%-m-%-d-%Y")
    week_ago_str = week_ago.strftime("%-m-%-d-%Y")

    # Variable to hold all raw data returned at the end of the loop, alongside helper variables
    raw_history = []
    counter = 0
    raw_ids = ""

    for item in items_info:
        counter += 1
        raw_ids += item["UniqueName"] + ","
        if counter == 135:
            ids = raw_ids.rstrip(",")
            counter = 0

            # Making API request
            current_prices_request_url = (
                api_info["base_url"] + api_info["endpoints"]["history_in_range"]
            )
            formatted_current_prices_url = current_prices_request_url.format(
                item_ids=ids,
                locations=ALL_LOCATIONS,
                date=week_ago_str,
                end_date=today_str,
                time_scale=24,
            )
            current_prices_response = requests.get(formatted_current_prices_url)

            # Add new response to final data, stripping first and last day due to insufficient data
            raw_history.extend(current_prices_response.json())

            # Reset id string
            raw_ids = ""

    with open("data/raw_history.json", "w") as f:
        json.dump(raw_history, f)
