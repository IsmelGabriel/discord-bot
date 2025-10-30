from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Check bot latency")
    async def ping(self, ctx):
        await ctx.send(f"Pong! Latency: {round(self.bot.latency * 1000)}ms")

async def setup(bot):
    await bot.add_cog(General(bot))
