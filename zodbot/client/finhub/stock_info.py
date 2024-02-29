from dataclasses import dataclass
from typing import Self


@dataclass
class StockInfo:
    country: str
    currency: str
    exchange: str
    ipo: str
    market_capitalization: float
    name: str
    phone: str
    share_outstanding: float
    ticker: str
    weburl: str
    logo: str
    finnhub_industry: str
    
    @classmethod
    def asdict(cls, data) -> dict:
        return {
            "country": data.country,
            "currency": data.currency,
            "exchange": data.exchange,
            "ipo": data.ipo,
            "marketCapitalization": data.market_capitalization,
            "name": data.name,
            "phone": data.phone,
            "shareOutstanding": data.share_outstanding,
            "ticker": data.ticker,
            "weburl": data.weburl,
            "logo": data.logo,
            "finnhubIndustry": data.finnhub_industry,
        }

    @classmethod
    def from_dict(cls, data) -> Self:
        return cls(
            country=data.get("country"),
            currency=data.get("currency"),
            exchange=data.get("exchange"),
            ipo=data.get("ipo"),
            market_capitalization=data.get("marketCapitalization"),
            name=data.get("name"),
            phone=data.get("phone"),
            share_outstanding=data.get("shareOutstanding"),
            ticker=data.get("ticker"),
            weburl=data.get("weburl"),
            logo=data.get("logo"),
            finnhub_industry=data.get("finnhubIndustry"),
        )