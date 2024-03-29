import discord
from zodbot.cogs.stocks import Stocks
from zodbot.cogs.vectors import Vectors
from discord.ext import commands 
from zodbot.config import config

intents = discord.Intents.all() 

description = '''A personal zodbot.'''

bot = commands.Bot(command_prefix='!', description=description, intents=intents)
stocks_cog = Stocks(bot)
vectors_cog = Vectors(bot)

@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user}')
  await bot.add_cog(stocks_cog)
  await bot.add_cog(vectors_cog)
  await bot.tree.sync()
  
@bot.tree.command(name="buy", description="Buy a stock")  # type: ignore
async def buy(interaction: discord.Interaction, symbol: str, shares: int = 100, purchase_price: float | None = None):    
  user_id = interaction.user.id
  message, error = await stocks_cog.buy(user_id, symbol, shares, purchase_price)
  if error:
    await interaction.response.send_message(error)
  else:
    await interaction.response.send_message(message)

@bot.tree.command(name="portfolio", description="View your portfolio") # type: ignore
async def portfolio(interaction: discord.Interaction):
  user = interaction.user
  embeds, error = await stocks_cog.portfolio(user)
  if error:
    await interaction.response.send_message(error)
  elif embeds is not None:
    await interaction.response.send_message(embeds=embeds)

if config.discord_token is None:
  print("Token is not set")
else:
  bot.run(config.discord_token)
