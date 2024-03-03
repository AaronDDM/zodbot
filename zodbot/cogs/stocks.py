import tempfile
from dataclasses import dataclass
from datetime import datetime

import discord
from discord.ext import commands
from zodbot import utils

from zodbot.cache import Cache
from zodbot.client import finhub
from zodbot.db import db

class Stocks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cache = Cache(tempfile.gettempdir() + "/cache", "stocks-v2.json", 60)

        if not db.check_if_db_exists():
            db.create_table()

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

    async def get_daily_price_info(self, symbol: str, cache: bool = False):
        # Check if the stock price information is in the cache
        if cache:
            cache_price_dict = self._cache.get(symbol + "-price")
            if cache_price_dict is not None:
                return finhub.StockQuote.from_dict(cache_price_dict)

        stock_price = await finhub.get(finhub.StockQuote, "https://finnhub.io/api/v1/quote?symbol={}".format(symbol))
        return stock_price
    
    @commands.command()
    async def add(self, ctx: commands.Context, symbol: str, shares: int, purchase_price: float):
        # Check if the stock information is in the cache
        stock_info = await self.get_stock_info(symbol)
        if stock_info is None:
            await ctx.send("No stock found")
            return

        # Check if the stock price information is in the cache
        stock_price_info = await self.get_daily_price_info(symbol, cache=True)
        if stock_price_info is None:
            await ctx.send("No stock price found")
            return

        # Check if the user already has stocks in the database
        if db.get_user_stock(ctx.author.id, symbol):
            await ctx.send("You already have this stock in your portfolio")
            return

        # Add the stock to the user's stocks
        db.add_transaction(ctx.author.id, symbol, 'BUY', shares, purchase_price)

        await ctx.send("Added stock to your portfolio")
    
    @commands.command()
    async def portfolio(self, ctx: commands.Context, *, member: discord.Member | None = None):
        user = member or ctx.author

        user_stocks = db.get_user_portfolio(user.id)
        if not user_stocks:
            await ctx.send("No stocks found for this user")
            return

        # Create the embed
        embed = discord.Embed(title="Stocks for {}".format(user.name),
                              description="",
                              colour=discord.Color.blue(),
                              timestamp=datetime.now())

        for stock in user_stocks:
            stock_info = await self.get_stock_info(stock.symbol)
            if stock_info is None:
                continue

            stock_price_info = await self.get_daily_price_info(stock.symbol, cache=True)
            if stock_price_info is None:
                continue

            # Add the stock to the embed
            embed.add_field(
                name="{} (${})".format(stock_info.name, stock_price_info.current_price),
                value="""
                    Purchased at: ${}\n
                    Shares: {}\n
                    Total value: ${}
                    """.format(
                        str(stock.weighted_average).format("0.2f"),
                        stock.shares, 
                        str(stock.value).format("0.2f")
                    ),
                inline=False
            )

        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.content.startswith('$'):
            # Get the stock symbol (e.g. "$APPL" or "$APPL message" both extract to $APPL)
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