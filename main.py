import discord
import asyncio
import logging
import os
from asyncio import Lock
from discord import app_commands
from discord.ext import commands

# import config
import json

intents = discord.Intents.all()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix="=", heartbeat_timeout=60, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Error syncing commands: {e}')
 
@bot.event
async def on_disconnect():
    print('Bot disconnected! Attempting to reconnect...')
    
@bot.event
async def on_resumed():
    print('Bot has resumed connection!')
        
@bot.event
async def on_guild_join(guild):
    print(f'Joined guild: {guild.name} (ID: {guild.id})')
    
@bot.event
async def on_guild_remove(guild):
    print(f'Removed from guild: {guild.name} (ID: {guild.id})')
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Please use a valid command.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")
        
async def load_config():
    try:
        with open('config/config.json') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Configuration file not found.")
        return {}
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return {}
    
config = asyncio.run(load_config())
discord_token = config.get("DISCORD_TOKEN", "")
    