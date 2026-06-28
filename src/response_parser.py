def raw_to_price_gap(response_data: list[dict], min_gap=0.3) -> dict[str, float]:
    return_dict = {}

    for item in response_data:
        if (
            item["sell_price_min"]
            >= item["buy_price_max"] + item["buy_price_max"] * min_gap
            and item["buy_price_max"] > 0
            and item["sell_price_min"] > 0
        ):
            return_dict[item["item_id"]] = float(
                item["sell_price_min"] / item["buy_price_max"]
            )

    return return_dict


def print_sorted_output(items: dict[str, float]) -> None:
    sorted_items = sorted(items.items(), key=lambda x: x[1], reverse=True)
    print("Biggest price gaps found:")
    for item in sorted_items:
        print(f"{item[0]}: selling for {item[1]}x the buy price")
