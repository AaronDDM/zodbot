import tempfile
from dataclasses import dataclass
from datetime import datetime

import discord
from discord.ext import commands
from zodbot import utils

from zodbot.cache import Cache
from zodbot.client import finhub


class Stocks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_user = None
        self._cache = Cache(tempfile.gettempdir() + "/cache", "stocks.json", 60 * 60 * 24)

    async def get_stock_info(self, symbol: str):
        # Check if the stock information is in the cache
        cache_info_dict = self._cache.get(symbol)
        if cache_info_dict is not None:
            return finhub.StockInfo.from_dict(cache_info_dict)
        
        # If the stock information is not in the cache, make a request to the API
        stock_info = await finhub.get(finhub.StockInfo, "https://finnhub.io/api/v1/stock/profile2?symbol={}".format(symbol)) 
        if stock_info is None:
            return None

        # Save the stock information in the cache
        self._cache.set(symbol, stock_info)

        return stock_info

    async def get_daily_price_info(self, symbol: str):
        stock_price = await finhub.get(finhub.StockQuote, "https://finnhub.io/api/v1/quote?symbol={}".format(symbol))

        # Convert to dict
        return stock_price

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.content.startswith('$'):
            # Get the stock symbol (e.g. $APPL, or $APPL message both extract to $APPL)
            stock_symbol = message.content.split()[0][1:]

            stock_info = await self.get_stock_info(stock_symbol)
            if stock_info is None:
                await message.channel.send("No stock found")
                return

            stock_price_info = await self.get_daily_price_info(stock_symbol)
            if stock_price_info is None:
                await message.channel.send("No stock price found")
                return
            
            stock_basic_financials = await finhub.get(finhub.StockBasicFinancials, "https://finnhub.io/api/v1/stock/metric?symbol={}".format(stock_symbol))
            if stock_basic_financials is None:
                await message.channel.send("No stock basic financials found")
                return

            # Get the color based on the change
            color = discord.Color.red() if stock_price_info.change < 0 else discord.Color.green()

            # Create the embed
            embed = discord.Embed(title="${} {} {}%".format(stock_price_info.current_price, 'up' if stock_price_info.change_percent > 0 else 'down', round(stock_price_info.change_percent, 3)),
                      description="**Symbol**: {}\n**Market Cap**: {}".format(stock_symbol, utils.human_format(stock_info.market_capitalization)),
                      colour=color,
                      timestamp=datetime.now())

            embed.set_author(name="{}".format(stock_info.name))

            await message.channel.send(embed=embed)
            