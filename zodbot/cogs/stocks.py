import tempfile
from dataclasses import dataclass
from datetime import datetime

import discord
from discord.ext import commands

from zodbot import utils
from zodbot.cache import Cache
from zodbot.client import finhub
from zodbot.config import config
from zodbot.db import db


class Stocks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._cache = Cache(config.cache_folder, "stocks-v2.json", 60)

        if not db.check_if_db_exists():
            db.create_table()


    async def get_stock_info(self, symbol: str) -> finhub.StockInfo | None:
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

    async def get_daily_price_info(self, symbol: str, cache: bool = False) -> finhub.StockQuote | None:
        # Check if the stock price information is in the cache
        if cache:
            cache_price_dict = self._cache.get(symbol + "-price")
            if cache_price_dict is not None:
                return finhub.StockQuote.from_dict(cache_price_dict)

        stock_price = await finhub.get(finhub.StockQuote, "https://finnhub.io/api/v1/quote?symbol={}".format(symbol))
        return stock_price
    
    async def buy(self, user_id: int, symbol: str, shares: int, purchase_price: float | None) -> tuple[str, None] | tuple[None, str]:
        # Check if the stock information is in the cache
        stock_info = await self.get_stock_info(symbol)
        if stock_info is None:
            return None, "No stock found"

        # Check if the stock price information is in the cache
        stock_price_info = await self.get_daily_price_info(symbol, cache=True)
        if stock_price_info is None:
            return None, "No stock price found"
        
        # If the purchase price is not provided, use the current market price
        if purchase_price is None:
            purchase_price = stock_price_info.current_price

        # Add the stock to the user's stocks
        db.add_transaction(user_id, symbol, 'BUY', shares, purchase_price)

        return "Added stock to your portfolio", None

    async def portfolio(self, user: discord.Member | discord.User) -> tuple[list[discord.Embed], None] | tuple[None, str]:
        user_stocks = db.get_user_portfolio(user.id)
        if not user_stocks:
            return None, "No stocks found for this user"

        # Create the embed
        embeds = []
        for stock in user_stocks:
            stock_info = await self.get_stock_info(stock.symbol)
            if stock_info is None:
                continue

            stock_price_info = await self.get_daily_price_info(stock.symbol, cache=True)
            if stock_price_info is None:
                continue
            
            # Get the percentage change
            change = stock_price_info.current_price - stock.weighted_average
            
            # Get the color based on the change, red if negative, green if positive, grey if 0
            colour = discord.Color.red() if change < 0 else discord.Color.green() if change > 0 else discord.Color.light_grey()

            # Add the stock to the embed
            embed = discord.Embed(
                title="{} (${})".format(stock_info.name, stock_price_info.current_price),
                description="",
                colour=colour,
                timestamp=stock.last_transaction_date
            )

            embed.add_field(
                name="Purchased at",
                value="{:.2f}%".format(stock.weighted_average)
            )
            
            embed.add_field(
                name="Change",
                value="{:.2f}%".format(change)
            )
            
            embeds.append(embed)

        return embeds, None

    @commands.command(name="buy")
    async def buy_command(self, ctx: commands.Context, symbol: str, shares: int = 100, purchase_price: float | None = None):
        message, error = await self.buy(ctx.author.id, symbol, shares, purchase_price)
        if error:
            await ctx.send(error)
        else:
            await ctx.send(message)
    
    @commands.command(name="portfolio")
    async def portfolio_command(self, ctx: commands.Context, *, member: discord.Member | None = None):
        user = member or ctx.author
        embed, error = await self.portfolio(user)
        if error:
            await ctx.send(error)
        elif embed is not None:
            await ctx.send(embeds=embed)

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
            embed = discord.Embed(
                title="${} {} {}%".format(stock_price_info.current_price, 'up' if stock_price_info.change_percent > 0 else 'down', round(stock_price_info.change_percent, 3)),
                description="**Symbol**: {}\n**Market Cap**: {}".format(stock_symbol.capitalize(), utils.human_format(stock_info.market_capitalization)),
                colour=color,
                timestamp=datetime.now()
            )

            embed.set_author(name="{}".format(stock_info.name))

            await message.channel.send(embed=embed)