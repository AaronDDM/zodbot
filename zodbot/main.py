import discord
import os
import datetime
import requests

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$'): 
    # Get the stock symbol (e.g. $APPL, or $APPL message both extract to $APPL)
    stockSymbol = message.content.split()[0][1:]
    
    r = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={}&apikey={}".format(stockSymbol, os.getenv('ALPHA_VANTAGE_API_KEY')))

    res = r.json()
    global_quote = res["Global Quote"]
    if "05. price" in global_quote:
      re_symbol = global_quote["01. symbol"]
      price = global_quote["05. price"]
      change = global_quote["09. change"]
      change_per = global_quote["10. change percent"]

      msg = "Name: **{}**".format(re_symbol) + "\n"
      msg += "Price: **{}**".format(price) + "\n"
      msg += "Change: **{} ({})**".format(change,change_per) + "\n"

      await message.channel.send(msg)
    else:
      await message.channel.send("No stock found")

  elif message.content.startswith('!hi'):
    present = datetime.datetime.now()
    future = datetime.datetime(2021, 6, 9, 0, 0, 0)
    difference = future - present
    await message.channel.send('Hi {}'.format(message.author.mention))

  elif message.content.startswith('!loki'):
    present = datetime.datetime.now()
    future = datetime.datetime(2021, 6, 9, 0, 0, 0)
    difference = future - present
    await message.channel.send('In {} days'.format(str(difference.days)))

token = os.getenv('TOKEN')

if token is None:
  print("Token is not set")
else:
  client.run(token)
