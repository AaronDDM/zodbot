import os
from typing import cast
from dotenv import load_dotenv

load_dotenv()

class Config():
    discord_token: str = ""
    finnhub_token: str = ""
    cache_folder: str = ""
    watch_file: str = ""

    def __init__(self):
        self._load()

    def _load(self):
        self.discord_token = cast(str, os.environ.get('DISCORD_TOKEN', ''))
        self.finnhub_token = cast(str, os.environ.get('FINNHUB_API_KEY', ''))
        self.cache_folder = cast(str, os.environ.get('CACHE_FOLDER', ''))
        self.db_file = cast(str, os.environ.get('DB_FILE', ''))
        