from discord.ext import commands

class CommandsError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Comando no encontrado. Usa `=help` para ver los comandos disponibles.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Faltan argumentos para este comando. Por favor, revisa la sintaxis.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("❌ No tienes permiso para usar este comando.")
        else:
            await ctx.send("❌ Ha ocurrido un error al ejecutar el comando.")
            raise error  # Re-raise the error for logging purposes
        
async def setup(bot):
    await bot.add_cog(CommandsError(bot))