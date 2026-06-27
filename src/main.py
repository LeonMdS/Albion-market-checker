import requests
import json


def main():
    # Get api info
    with open("../api_info.json") as f:
        api_info = json.load(f)

    # Testing
    base_request_url = api_info["base_url"] + api_info["endpoints"]["current_prices"]
    formatted_request_url = base_request_url.format(
        item_ids="T5_BAG", locations="Lymhurst", qualities="1"
    )
    test_response = requests.get(formatted_request_url)
    print(test_response.json())


if __name__ == "__main__":
    main()
