from collections import defaultdict
from assets.constants import MIN_GAP


def raw_to_price_gap(
    response_data: list[dict], min_gap=MIN_GAP
) -> dict[str, dict[str, float]]:
    return_dict = defaultdict(dict)

    for item in response_data:
        if (
            item["sell_price_min"]
            >= item["buy_price_max"] + item["buy_price_max"] * min_gap
            and item["buy_price_max"] > 0
            and item["sell_price_min"] > 0
        ):
            return_dict[item["city"]][item["item_id"]] = float(
                item["sell_price_min"] / item["buy_price_max"]
            )

    return return_dict


def print_sorted_output(items: dict[str, dict[str, float]]) -> None:
    for city in items:
        sorted_items = sorted(items[city].items(), key=lambda x: x[1], reverse=True)
        print(f"Biggest price gaps found in {city}:")
        for item in sorted_items:
            print(f"{item[0]}: selling for {item[1]}x the buy price")
        print("\n===========================================================\n")
