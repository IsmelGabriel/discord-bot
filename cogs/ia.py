from discord.ext import commands
from utils.ia import generate_response
from utils.memory_db import clear_history

class IA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ask", help="Talk to the AI.")
    async def ask(self, ctx, *, question: str):
        await ctx.typing()
        server_id = ctx.guild.id if ctx.guild else 0
        response = generate_response(server_id, ctx.author.id, question)
        await ctx.send(response)

    @commands.command(name="reset", help="Clear your conversation memory with the AI.")
    async def reset(self, ctx):
        server_id = ctx.guild.id if ctx.guild else 0
        clear_history(server_id, ctx.author.id)
        await ctx.send("🧠 Memory cleared successfully.")

async def setup(bot):
    await bot.add_cog(IA(bot))
