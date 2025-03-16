import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Function to read token from a file
def load_token(filename):
    with open(filename, "r") as file:
        return file.read().strip()  # Reads token and removes extra spaces/newlines
    

# Load bot token from 'token.txt'
TOKEN = load_token("hidden_token.txt")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='test')
async def hello(ctx):
    await ctx.send("received!")

bot.run(TOKEN)