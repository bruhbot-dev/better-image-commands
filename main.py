import discord
import random
from googleapiclient.discovery import build
from discord.ext import commands

# Function to read token from a file
def load_token(filename):
    with open(filename, "r") as file:
        return file.read().strip()  # Reads token and removes extra spaces/newlines
    

# Load bot token from 'token.txt'
TOKEN = load_token("hidden_token.txt")
GOOGLE_API_KEY = load_token("GOOGLE_API_KEY.txt")
CSE_ID = load_token('CSE_ID.txt')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='test')
async def hello(ctx):
    await ctx.send("received!")

# Function to search Google Images

def google_image_search(query, num_results=10, start=1):
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    
    start_index = (start - 1) * num_results + 1  # Calculate start index for pagination
    res = service.cse().list(
        q=query, 
        cx=CSE_ID, 
        searchType="image", 
        num=num_results, 
        start=start_index
    ).execute()
    
    if "items" in res:
        return [item["link"] for item in res["items"]]  # Return a list of image URLs
    return []
# Create a View with Buttons
class ImagePaginationView(discord.ui.View):
    def __init__(self, images, query):
        super().__init__()
        self.images = images
        self.query = query  # Store the original query
        self.index = 0

    async def update_message(self, interaction: discord.Interaction):
        """Update the message with the new image."""
        await interaction.response.defer()  # Acknowledge first
        embed = discord.Embed(title="Google Image Result", color=discord.Color.blue())
        embed.set_image(url=self.images[self.index])
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label="⬅️ Prev", style=discord.ButtonStyle.primary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.index > 0:
            self.index -= 1
            await self.update_message(interaction)

    @discord.ui.button(label="➡️ Next", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.index < len(self.images) - 1:
            self.index += 1
            if self.index>=len(self.images) -1:
                print(1)
                print(self.images)

                self.images += google_image_search(self.query, 10, len(self.images)-1)
                print(2)

                print(self.images)
            await self.update_message(interaction)

# Command to fetch an image with pagination
@bot.command(name='im')
async def image(ctx, *, query: str):
    images = google_image_search(query, 10, 1)
    print(images)
    if images:
        embed = discord.Embed(title="Google Image Result", color=discord.Color.blue())
        embed.set_image(url=images[0])
        view = ImagePaginationView(images, query)
        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send("No images found!")

bot.run(TOKEN)