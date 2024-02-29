import os
from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict, Generic, Optional, Protocol, Self, Type, TypeVar, cast

import requests


class ResponseDataAbstract(Protocol):
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict) -> Self:
        pass

T = TypeVar('T', bound=ResponseDataAbstract)

class ResponseData(Generic[T]):
    pass
    
async def get(cls: Type[T], url: str) -> Optional[T]:
    # Make the request
    request = requests.get(url, headers={"X-Finnhub-Token": os.getenv('FINNHUB_API_KEY')})

    # Check if the request was successful
    if request.status_code != 200:
        print(request.status_code, request.text)
        return None
    
    # Parse the response
    response_dict = request.json()

    return cls.from_dict(data=response_dict)

async def post(type_: type[T], url: str, body: dict | None = None) -> Optional[T]:
    # Make the request
    request = requests.post(url, data=body, headers={"X-Finnhub-Token": os.getenv('FINNHUB_API_KEY')})

    # Check if the request was successful
    if request.status_code != 200:
        print(request.status_code, request.text)
        return None
    
    # Parse the response
    response_dict = request.json()

    return cast(T, type_.from_dict(data=response_dict))
