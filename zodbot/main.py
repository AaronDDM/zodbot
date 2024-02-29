import discord
from zodbot.cogs import stocks
from discord.ext import commands 
from zodbot.config import config

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

description = '''A personal zodbot.'''


bot = commands.Bot(command_prefix='!', description=description, intents=intents)

@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user}')
  await bot.add_cog(stocks.Stocks(bot))


if config.discord_token is None:
  print("Token is not set")
else:
  bot.run(config.discord_token)
