import requests
import json


def make_request() -> list[dict]:
    # Get api info
    with open("../api_info.json") as f:
        api_info = json.load(f)

    # Get all item ids
    with open("../items.json") as f:
        items_info = json.load(f)

    # Variable to hold all raw data returned at the end of the loop
    raw_data = []

    # Counter to keep track of item count per request
    counter = 0

    # Make item id string for this loop
    ids = ""

    # Requesting 135 items at a time until all items are requested
    for item in items_info:
        # Make this loop's id string
        counter += 1
        ids += item["UniqueName"] + ","
        if counter == 135:
            ids.rstrip(",")
            counter = 0

            # Making API request
            current_prices_request_url = (
                api_info["base_url"] + api_info["endpoints"]["current_prices"]
            )
            formatted_current_prices_url = current_prices_request_url.format(
                item_ids=ids,
                locations="Lymhurst",
                qualities="1",
            )
            current_prices_response = requests.get(formatted_current_prices_url)

            # Add new response to final data
            raw_data.extend(current_prices_response.json())

            # Reset id string
            ids = ""

    return raw_data
