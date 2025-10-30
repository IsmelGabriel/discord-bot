from discord.ext import commands
from utils.ia import generate_response
from utils.memory import clear_history

class IA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ask", help="Ask a question to the AI.")
    async def ask(self, ctx, *, question: str):
        response = generate_response(ctx.author.id, question)
        await ctx.send(response)

    @commands.command(name="reset", help="Reset your conversation history.")
    async def reset(self, ctx):
        clear_history(ctx.author.id)
        await ctx.send("Your conversation history has been reset.")

def setup(bot):
    bot.add_cog(IA(bot))
    