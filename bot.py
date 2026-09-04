import os

import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN :
    raise RuntimeError(
        "DISCORD_TOKEN not found in file .env"
    )

intents = discord.Intents.default()

class KpopBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )

        async def setup_hook(self): 
            await self.load_extension(
                "commands.groupe"
            )

            await self.tree.sync()

            print('Discord Command synchronised')

bot =  KpopBot()

@bot.event
async def on_ready(): 

    print(
        "Connected as {bot.user}"
    )

    print( 
        "ID of bot : {bot.user.id}"
    )

bot.run(TOKEN)
