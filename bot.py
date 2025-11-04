import discord
from discord.ext import commands
import asyncio
import os
import sys
import logging
from utils.logger_db import guardar_log
from utils.ia import generate_response
import webserver

# Get token from os environment variable for security
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import config, handle missing file
"""try:
    import config
except ImportError:
    logger.error("config.py file not found! Please create one with your DISCORD_TOKEN")
    sys.exit(1)"""

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Enable member intents

bot = commands.Bot(command_prefix="=", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Bot is online: '{bot.user}'")
    logger.info(f"Bot ID: '{bot.user.id}'")
    
    server_count = len(bot.guilds)
    logger.info(f"Connected to {server_count} servers.")
    
    # List servers
    for guild in bot.guilds:
        logger.info(f" - {guild.name} (ID: {guild.id})")
    
    
@bot.event
async def on_command_error(ctx, error):
    logger.error(f"Command error: '{ctx.command}': {str(error)}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if not message.guild:
        return

    guardar_log(
        level="INFO",
        server_id=message.guild.id if message.guild else 0,
        author_id=message.author.id,
        author_name=str(message.author),
        mensaje=message.content
    )
    
    if bot.user in message.mentions and not message.mention_everyone:
        prompt = message.content.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "").strip()
        if not prompt:
            await message.channel.send("👋 Hello! How can I assist you today?")
        else:
            await message.channel.typing()
            server_id = message.guild.id if message.guild else 0
            response = generate_response(server_id, message.author.id, prompt)
            user = message.author.mention
            await message.channel.send(response + f"\n{user}")


    await bot.process_commands(message)


async def load_cogs():
    # Verify cogs directory exists
    cogs_dir = "./cogs"
    if not os.path.exists(cogs_dir):
        logger.error(f"Directory '{cogs_dir}' not found!")
        return

    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logger.info(f"Loaded extension: {filename}")
            except Exception as e:
                logger.error(f"Failed to load extension {filename}: {str(e)}")

webserver.keep_alive()
async def main():
    try:
        async with bot:
            await load_cogs()
            if not DISCORD_TOKEN:
                logger.error("No Discord token found!")
                return
            await bot.start(DISCORD_TOKEN)
    except discord.LoginFailure:
        logger.error("Invalid Discord token!")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot shutdown by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
