import discord
from discord.ext import commands
import hashlib
import random
import json

# ---- LOAD TOKEN FROM CONFIG ----
with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["TOKEN"]

# ---- SET SERVER SEED IN CODE ----
SERVER_SEED = "my_server_secret_seed"  # replace with your secret seed

# ---- DISCORD INTENTS ----
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- Utility Function ---
def coinflip_result(server_seed, client_seed, nonce):
    combined = f"{server_seed}:{client_seed}:{nonce}"
    hashed = hashlib.sha256(combined.encode()).hexdigest()
    number = int(hashed[:8], 16)

    if number % 2 == 0:
        return "Heads / Red"
    else:
        return "Tails / Black"

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def flip(ctx, betamount: int, client_seed: str):
    """
    Usage: !flip <betamount> <client_seed>
    Example: !flip 100 myseed
    """
    nonce = random.randint(1, 1_000_000)
    result = coinflip_result(SERVER_SEED, client_seed, nonce)

    await ctx.send(
        f"🎲 **Coin Flip Result** 🎲\n"
        f"💰 Bet: `{betamount}`\n"
        f"🔑 Server Seed: `{SERVER_SEED}`\n"
        f"🧩 Client Seed: `{client_seed}`\n"
        f"🔄 Nonce: `{nonce}`\n"
        f"👉 Result: **{result}**"
    )

bot.run(TOKEN)
