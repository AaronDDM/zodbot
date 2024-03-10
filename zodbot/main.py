import discord
from zodbot.cogs.stocks import Stocks
from discord.ext import commands 
from zodbot.config import config

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

description = '''A personal zodbot.'''


bot = commands.Bot(command_prefix='!', description=description, intents=intents)

stocks_cog = Stocks(bot)

@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user}')
  await bot.add_cog(stocks_cog)
  await bot.tree.sync()

if config.discord_token is None:
  print("Token is not set")
else:
  bot.run(config.discord_token)
