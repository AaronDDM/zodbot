from dataclasses import dataclass
from typing import Self


@dataclass
class StockQuote:
    current_price: float
    change: float
    change_percent: float
    high: float
    low: float
    open: float
    previous_close: float

    @classmethod
    def from_dict(cls, data) -> Self:
        return cls(
            current_price=data.get("c"),
            change=data.get("d"),
            change_percent=data.get("dp"),
            high=data.get("h"),
            low=data.get("l"),
            open=data.get("o"),
            previous_close=data.get("pc"),
        )