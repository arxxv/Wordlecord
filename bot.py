from db import create_table
import psycopg2
import os
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands
from utils import game_over, generate_embed, generate_leaderboard_embed, is_valid_word, update_embed, get_wordle_id
load_dotenv()

bot = commands.Bot(command_prefix=[])

create_table()


GUILD_IDS = ([int(g_id) for g_id in os.getenv("GUILD_IDS").split(",")]
             if os.getenv("GUILD_ID", None)
             else nextcord.utils.MISSING
             )


@bot.slash_command(description="Play a wordle", guild_ids=GUILD_IDS)
async def play(interaction):
    ansid = get_wordle_id()
    embed = generate_embed(interaction.user, ansid)
    await interaction.send(embed=embed)


@bot.slash_command(description="Discord wordle leaderboad", guild_ids=GUILD_IDS)
async def leaderboards(interaction):
    embed = generate_leaderboard_embed()
    await interaction.send(embed=embed)


@bot.event
async def on_message(message):
    ref = message.reference
    if not ref or not isinstance(ref.resolved, nextcord.Message):
        return

    parent = ref.resolved
    if parent.author.id != bot.user.id:
        return

    if not parent.embeds:
        return

    embed = parent.embeds[0]

    if embed.author.name != message.author.name:
        await message.reply(f"This game wasstarted by {embed.author.name}\nUse /play to start a new game", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return

    if game_over(embed):
        await message.reply("The game is already over\nPlay Again?\n", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return

    if len(parent.embeds) > 1:
        print(parent.embeds[0], parent.embeds[1])

    if len(message.content.split()) > 1:
        await message.reply("Please respond with a single 5-letter word", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return

    if not is_valid_word(message.content):
        await message.reply("Not a valid word", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return

    embed = update_embed(message.content, embed)
    await parent.edit(embed=embed)

    try:
        await message.delete()
    except Exception:
        pass

bot.run(os.getenv("TOKEN"))
