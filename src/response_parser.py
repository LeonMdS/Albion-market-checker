from collections import defaultdict
from assets.constants import MIN_GAP, MIN_VOLUME
from data_model import ItemListingData


def filter_by_profit(
    response_data: list[dict], min_gap=MIN_GAP
) -> list[ItemListingData]:

    return_list: list[ItemListingData] = []
    for item in response_data:
        if (
            item["sell_price_min"]
            >= item["buy_price_max"] + item["buy_price_max"] * min_gap
            and item["buy_price_max"] > 0
            and item["sell_price_min"] > 0
        ):
            new_listing = ItemListingData(
                item["city"],
                item["item_id"],
                item["sell_price_min"] / item["buy_price_max"],
            )
            return_list.append(new_listing)

    return return_list


def get_volumes_dict(raw_history: list[dict]) -> dict[str, dict[str, int]]:
    return_dict = defaultdict(dict)
    for listing in raw_history:
        # Get average sales volume:
        total_volume = 0
        for day in listing["data"][1:-1]:
            total_volume += day["item_count"]

        # Get average volume for the item in that city and add to return dict
        if len(listing["data"][1:-1]) != 0:
            average_volume = total_volume // len(listing["data"][1:-1])
            return_dict[listing["location"]][listing["item_id"]] = average_volume
        else:
            return_dict[listing["location"]][listing["item_id"]] = 0

    return return_dict


def filter_by_volume(
    listings: list[ItemListingData], volumes: dict[str, dict[str, int]]
) -> list[ItemListingData]:
    resulting_list: list[ItemListingData] = []

    for listing in listings:
        # Check if that listing's volume is above the minimum threshold
        try:
            if volumes[listing.city][listing.item_id] >= MIN_VOLUME:
                listing.volume = volumes[listing.city][listing.item_id]
                resulting_list.append(listing)
        except KeyError:
            continue

    return resulting_list


def print_sorted_output(listings: list[ItemListingData]) -> None:
    sorted_listings = sorted(listings, key=lambda x: x.profit, reverse=True)

    for listing in sorted_listings:
        print(
            f"City: {listing.city}, Item ID: {listing.item_id}, Profit: {listing.profit:.2f}, Volume: {listing.volume}"
        )
