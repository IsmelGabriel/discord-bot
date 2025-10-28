from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Responde con Pong y la latencia del bot")
    async def ping(self, ctx):
        await ctx.send(f"Pong! Latencia: {round(self.bot.latency * 1000)}ms")

async def setup(bot):
    await bot.add_cog(General(bot))
