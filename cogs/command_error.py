from discord.ext import commands

class CommandsError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Command not found. Type =help command for more info on a command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Command missing required arguments.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("❌ You do not have permission to use this command.")
        else:
            await ctx.send("❌ An error occurred while processing the command.")
            raise error  # Re-raise the error for logging purposes
        
async def setup(bot):
    await bot.add_cog(CommandsError(bot))