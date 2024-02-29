from dataclasses import dataclass
from typing import Self

@dataclass
class StockMetric:
    ten_day_average_trading_volume: float
    fifty_two_week_high: float
    fifty_two_week_low: float
    fifty_two_week_low_date: str
    fifty_two_week_price_return_daily: float
    beta: float

    @classmethod
    def asdict(cls, data) -> dict:
        return {
            "10DayAverageTradingVolume": data.ten_day_average_trading_volume,
            "52WeekHigh": data.fifty_two_week_high,
            "52WeekLow": data.fifty_two_week_low,
            "52WeekLowDate": data.fifty_two_week_low_date,
            "52WeekPriceReturnDaily": data.fifty_two_week_price_return_daily,
            "beta": data.beta
        }

    @classmethod
    def from_dict(cls, data) -> Self:
        return cls(
            ten_day_average_trading_volume=data["10DayAverageTradingVolume"],
            fifty_two_week_high=data["52WeekHigh"],
            fifty_two_week_low=data["52WeekLow"],
            fifty_two_week_low_date=data["52WeekLowDate"],
            fifty_two_week_price_return_daily=data["52WeekPriceReturnDaily"],
            beta=data["beta"]
        )


@dataclass
class StockBasicFinancials:
    metric: StockMetric
    metric_type: str
    symbol: str

    @classmethod
    def asdict(cls, data) -> dict:
        return {
            "metric": StockMetric.asdict(data.metric),
            "metricType": data.metric_type,
            "symbol": data.symbol
        }

    @classmethod
    def from_dict(cls, data) -> Self:
        return cls(
            metric=StockMetric.from_dict(data["metric"]),
            metric_type=data["metricType"],
            symbol=data["symbol"]
        )