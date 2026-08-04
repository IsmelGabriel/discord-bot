import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # 1. Intentar usar el canal de mensajes de sistema de Discord
        channel = member.guild.system_channel

        # 2. Si está desactivado, buscar un canal por nombre
        if channel is None:
            for c in member.guild.text_channels:
                if "bienvenid" in c.name.lower() or "general" in c.name.lower():
                    channel = c
                    break

        # Si encontramos un canal válido, enviamos la tarjeta de bienvenida
        if channel is not None:
            embed = discord.Embed(
                title=f"¡Bienvenido/a a {member.guild.name}! 🎉",
                description=f"Hola {member.mention}, nos alegra mucho tenerte por aquí. \n\n¡Siéntete libre de presentarte y participar en los canales!",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"Ahora somos {member.guild.member_count} miembros.")

            await channel.send(content=f"¡Un nuevo miembro ha llegado, {member.mention}!", embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel = member.guild.system_channel

        if channel is None:
            for c in member.guild.text_channels:
                if "bienvenid" in c.name.lower() or "general" in c.name.lower():
                    channel = c
                    break

        if channel is not None:
            embed = discord.Embed(
                title=f"¡Hasta luego, {member.name}! 👋",
                description=f"Esperamos que hayas disfrutado tu tiempo en el servidor.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"Ahora somos {member.guild.member_count} miembros.")

            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
