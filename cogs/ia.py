from discord.ext import commands
from utils.ia import generate_response

class IA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ask", help="Ask a question to the AI.")
    async def ask(self, ctx, *, question: str):
        response = generate_response(question)
        await ctx.send(response)

async def setup(bot):
    await bot.add_cog(IA(bot))
