import os
from typing import cast
from dotenv import load_dotenv

load_dotenv()

class Config():
    discord_token: str = ""
    finnhub_token: str = ""
    firebase_service_account_key: str = ""

    def __init__(self):
        self._load()

    def _load(self):
        self.discord_token = cast(str, os.environ.get('DISCORD_TOKEN', ''))
        self.finnhub_token = cast(str, os.environ.get('FINNHUB_API_KEY', ''))
        self.firebase_service_account_key = cast(str, os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY', ''))
        