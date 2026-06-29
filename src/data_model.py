from dataclasses import dataclass


@dataclass
class ItemListingData:
    city: str
    item_id: str
    profit: float
    volume: int = 0
