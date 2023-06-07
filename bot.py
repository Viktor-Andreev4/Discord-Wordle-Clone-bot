import os
from dotenv import load_dotenv

import nextcord
from nextcord.ext import commands

from utils import *

load_dotenv()

bot = commands.Bot(command_prefix=[])

GUILD_IDS = (   [int(guild_id) for guild_id in os.getenv("GUILD_IDS").split(",")]
                if os.getenv("GUILD_IDS", None)
                else nextcord.utils.MISSING
            )

@bot.slash_command(name="play", description="Play wordle", guild_ids=GUILD_IDS)
async def play(interaction: nextcord.Interaction):
    id = random_wordle_id()
    embed = generate_wordle_embed(interaction.user, id)
    await interaction.send(embed=embed)

@bot.slash_command(name="legend", description="Shows a legend of what the color codes are")
async def legend(interaction: nextcord.Interaction):
    embed =  nextcord.Embed(title="LEGEND")
    embed.description = ":black_circle: Character does not exist\n:yellow_circle: Character exists but in wrong position\n:green_circle: Character exists and in the right postion"
    await interaction.send(embed=embed)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message: nextcord.Message):
    ref = message.reference
    if not ref or not isinstance(ref.resolved, nextcord.Message):
        return
    
    parent = ref.resolved
    if parent.author.id != bot.user.id:
        return 
    
    if not parent.embeds:
        return

    embed = parent.embeds[0]

    if embed.author.name != message.author.name or embed.author.icon_url != message.author.display_avatar.url:
        await message.reply(f"This is not your game to play. This game is played by {embed.author.name}", delete_after=5)
        
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return

    if is_game_over(embed):
        await message.reply("The game is already over. Start a new game with /play", delete_after=5)
        
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return 

    if len(message.content.split()) > 1:
        await message.reply("Please only one word with five letters", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return

    if not is_valid_word(message.content):
        await message.reply("That is not a valid word", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return

    embed = update_embed(embed, message.content)
    await parent.edit(embed=embed)

    try:
        await message.delete()
    except Exception:
        pass


bot.run(os.getenv("TOKEN"))