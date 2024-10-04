import discord
from discord.ext import commands
from cogs.data.database import init_db
from cogs.data.environment import API_TOKEN

intents = discord.Intents.default()
intents.message_content, intents.members = True, True
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready for use.")


cogs = [
    'audit',
    'fun'
]

def load_cogs(cogs: list):
    for extension in cogs:
        bot.load_extension(f'cogs.{extension}')

if __name__ == "__main__":
    init_db()
    load_cogs(cogs)
    bot.run(API_TOKEN)