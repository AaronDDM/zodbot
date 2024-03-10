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
    
    def asdict(cls) -> dict:
        return {
            "country": cls.country,
            "currency": cls.currency,
            "exchange": cls.exchange,
            "ipo": cls.ipo,
            "marketCapitalization": cls.market_capitalization,
            "name": cls.name,
            "phone": cls.phone,
            "shareOutstanding": cls.share_outstanding,
            "ticker": cls.ticker,
            "weburl": cls.weburl,
            "logo": cls.logo,
            "finnhubIndustry": cls.finnhub_industry,
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