import os
import discord
from discord.ext import commands
import matplotlib.pyplot as plt
import robin_stocks.robinhood as r
from wsgi import get_coins, get_plots
from pathlib import Path
from dotenv import load_dotenv

master_dict = {}
dotenv_path = Path('ACB/acb.env')
load_dotenv(dotenv_path=dotenv_path)
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')


def discord_coins():
    intents = discord.Intents.default()
    intents.message_content = True
    #os.chdir('test_plots.png')
    coin_bot = commands.Bot(command_prefix="#", intents=intents)

    @coin_bot.command(name='frumptypeas')
    async def send_coins(ctx):
        await ctx.send("Have you heard the good news about our lord and saviour, BTC?")
        await ctx.close

    coin_bot.run(DISCORD_BOT_TOKEN)


discord_coins()
