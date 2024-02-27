import discord
import os
from zodbot.cogs import stocks
from discord.ext import commands 

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

description = '''A personal zodbot.'''


bot = commands.Bot(command_prefix='!', description=description, intents=intents)

@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user}')
  await bot.add_cog(stocks.Stocks(bot))


token = os.getenv('TOKEN')

if token is None:
  print("Token is not set")
else:
  bot.run(token)
