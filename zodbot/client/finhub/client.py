import os
from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict, Generic, Optional, Protocol, Self, Type, TypeVar, cast

import requests

from zodbot.config import config


class ResponseDataAbstract(Protocol):
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict) -> Self:
        pass

    def asdict(cls) -> Dict:
        pass

T = TypeVar('T', bound=ResponseDataAbstract)

class ResponseData(Generic[T]):
    pass
    
async def get(cls: type[T], url: str) -> Optional[T]:
    # Make the request
    request = requests.get(url, headers={"X-Finnhub-Token": config.finnhub_token})

    # Check if the request was successful
    if request.status_code != 200:
        print(request.status_code, request.text)
        return None
    
    # Parse the response
    response_dict = request.json()

    return cls.from_dict(data=response_dict)

async def post(cls: type[T], url: str, body: dict | None = None) -> Optional[T]:
    # Make the request
    request = requests.post(url, data=body, headers={"X-Finnhub-Token": os.getenv('FINNHUB_API_KEY')})

    # Check if the request was successful
    if request.status_code != 200:
        print(request.status_code, request.text)
        return None
    
    # Parse the response
    response_dict = request.json()

    return cls.from_dict(data=response_dict)
