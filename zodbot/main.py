import discord
from zodbot.cogs.stocks import Stocks
from discord.ext import commands 
from zodbot.config import config

intents = discord.Intents.all() 

description = '''A personal zodbot.'''

bot = commands.Bot(command_prefix='!', description=description, intents=intents)
stocks_cog = Stocks(bot)

@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user}')
  await bot.add_cog(stocks_cog)
  await bot.tree.sync()

@bot.tree.command(name="buy", description="Buy a stock")
async def buy(group: discord.app_commands.commands.Group, interaction: discord.Interaction, *args, **kwargs):    
  symbol, shares, purchase_price = args
  user_id = interaction.user.id
  success, response = await stocks_cog.buy(user_id, symbol, shares, purchase_price)
  await interaction.response.send_message(response)

@bot.tree.command(name="portfolio", description="View your portfolio")
async def portfolio(group: discord.app_commands.commands.Group, interaction: discord.Interaction, *args, **kwargs):
    user = interaction.user
    success, response = await stocks_cog.portfolio(user)
    if success:
        await interaction.response.send_message(embed=response)
    else:
        await interaction.response.send_message(response)

if config.discord_token is None:
  print("Token is not set")
else:
  bot.run(config.discord_token)
