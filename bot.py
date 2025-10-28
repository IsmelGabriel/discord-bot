import discord
from discord.ext import commands
import asyncio
import os
import sys
import logging
from utils.logger import setup_logger

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import config, handle missing file
try:
    import config
except ImportError:
    logger.error("config.py file not found! Please create one with your DISCORD_TOKEN")
    sys.exit(1)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Enable member intents

bot = commands.Bot(command_prefix="=", intents=intents)

logger = setup_logger()

@bot.event
async def on_ready():
    logger.info(f"Bot conectado como {bot.user}")
    logger.info(f"Bot ID: {bot.user.id}")
    
@bot.event
async def on_command_error(ctx, error):
    logger.error(f"Error en el comando '{ctx.command}': {str(error)}")

@bot.event
async def on_message(message):
    logger.info(f"Mensaje recibido de {message.author}: {message.content}")
    
    if message.author == bot.user:
        return
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

async def main():
    try:
        async with bot:
            await load_cogs()
            if not config.DISCORD_TOKEN:
                logger.error("No Discord token found in config.py!")
                return
            await bot.start(config.DISCORD_TOKEN)
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
