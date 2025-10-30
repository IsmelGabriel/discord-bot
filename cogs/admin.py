import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="mute", help="Silencia a un miembro del servidor")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: commands.MemberConverter):
        muted_role = discord.utils.get(ctx.guild.roles, name="MemMuted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="MemMuted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        
        await member.add_roles(muted_role)
        await ctx.send(f"{member.mention} ha sido silenciado.")
        
    @commands.command(name="unmute", help="Quita el silencio a un miembro del servidor")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: commands.MemberConverter):
        muted_role = discord.utils.get(ctx.guild.roles, name="MemMuted")
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f"{member.mention} ha sido desilenciado.")
        else:
            await ctx.send(f"{member.mention} no está silenciado.")
        
async def setup(bot):
    await bot.add_cog(Admin(bot))
