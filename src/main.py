import api_request
import response_parser
import json
from data_model import ItemListingData


def main():
    # Make API requests for latest data and write do data directory
    api_request.make_request()
    api_request.request_history()

    # Parse data from the directory
    with open("data/raw_prices.json") as f:
        raw_prices = json.load(f)

    filtered_prices = response_parser.filter_by_profit(raw_prices)

    with open("data/raw_history.json") as f:
        raw_history = json.load(f)

    filtered_history = response_parser.get_volumes_dict(raw_history)

    filtered_listings = response_parser.filter_by_volume(
        filtered_prices, filtered_history
    )
    response_parser.print_sorted_output(filtered_listings)


if __name__ == "__main__":
    main()
