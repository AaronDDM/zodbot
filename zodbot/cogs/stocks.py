import discord
import requests
import os
import tempfile
from zodbot.cache import Cache
from datetime import datetime
from discord.ext import commands 

class Stocks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_user = None
        self._cache = Cache(tempfile.gettempdir() + "/cache", "stocks.json", 60 * 60 * 24)

    async def get_stock_info(self, symbol: str):
        # Check if the stock information is in the cache
        stock_info = self._cache.get(symbol)
        if stock_info is not None:
            return stock_info
        
        # If the stock information is not in the cache, make a request to the API
        request = requests.get("https://finnhub.io/api/v1/stock/profile2?symbol={}".format(symbol), headers={"X-Finnhub-Token": os.getenv('FINNHUB_API_KEY')})

        # Check if the request was successful
        if request.status_code != 200:
            print(request.status_code, request.text)
            return None
        
        # Parse the response
        response = request.json()

        # If the response does not contain the stock information
        if "country" not in response:
            return None
        
        # Convert to dict
        stock_info = {
            "country": response["country"],
            "currency": response["currency"],
            "exchange": response["exchange"],
            "ipo": response["ipo"],
            "marketCapitalization": response["marketCapitalization"],
            "name": response["name"],
            "phone": response["phone"],
            "shareOutstanding": response["shareOutstanding"],
            "ticker": response["ticker"],
            "weburl": response["weburl"],
            "logo": response["logo"],
            "finnhubIndustry": response["finnhubIndustry"],
        }

        # Save the stock information in the cache
        self._cache.set(symbol, stock_info)

        return stock_info

    async def get_daily_price_info(self, symbol: str):
        request = requests.get("https://finnhub.io/api/v1/quote?symbol={}".format(symbol), headers={"X-Finnhub-Token": os.getenv('FINNHUB_API_KEY')})

        # Check if the request was successful
        if request.status_code != 200:
            print(request.status_code, request.text)
            return None
    
        # Parse the response
        response = request.json()

        # Check if the response contains the stock information
        if "d" not in response:
            return None
        
        # Convert to dict
        # "01. symbol": "NET",
        # "02. open": "100.0000",
        # "03. high": "101.6600",
        # "04. low": "97.1400",
        # "05. price": "98.4500",
        # "06. volume": "2945929",
        # "07. latest trading day": "2024-02-23",
        # "08. previous close": "99.4700",
        # "09. change": "-1.0200",
        # "10. change percent": "-1.0254%"
        
        return {
            "symbol": symbol,
            "price": float(response["c"]),
            "change": float(response["d"]),
            # Remove the % sign and convert to float
            "change_percent":  float(response["dp"]),
            "volume": int(response["t"]),
        }

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
            
            # Get the color based on the change
            color = discord.Color.red() if stock_price_info["change"] < 0 else discord.Color.green()

            # Create the embed
            embed = discord.Embed(title="{}% at ${}".format(stock_price_info["change_percent"], stock_price_info["price"]),
                      description="**Symbol**: {}\n**Volume**: {}".format(stock_price_info["symbol"], stock_price_info["volume"]),
                      colour=color,
                      timestamp=datetime.now())

            embed.set_author(name="{}".format(stock_info["name"]), icon_url="{}".format(stock_info["logo"]))

            # embed.set_footer(text="Latest trading day {}".format(stock_price_info["latest_trading_day"]))

            await message.channel.send(embed=embed)
            


    @commands.command()
    async def stock(self, ctx: commands.Context, *, member: discord.Member | None = None):
        """Says hello"""
        user = member or ctx.author
        if self._last_user is None or self._last_user.id != user.id:
            await ctx.send(f'Hello {user.name}~')
        else:
            await ctx.send(f'Hello {user.name}... This feels familiar.')
        self._last_user = user