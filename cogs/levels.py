import discord
from discord import app_commands
from discord.ext import commands
import random
from datetime import datetime
import math
from utils.db import execute_query, fetch_query

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Diccionario para almacenar la última vez que un usuario ganó XP
        # Formato: {user_id: datetime}
        self.cooldowns = {}
        self.COOLDOWN_SECONDS = 10  # 10 segundos entre ganancias de XP

    def get_user_data(self, server_id: int, user_id: int):
        query = "SELECT xp, level FROM user_levels WHERE server_id = %s AND user_id = %s"
        result = fetch_query(query, (server_id, user_id))
        if result:
            return result[0]
        return None

    def add_user_xp(self, server_id: int, user_id: int, xp_to_add: int) -> int:
        """Suma XP y devuelve el nuevo nivel (si subió de nivel), de lo contrario retorna 0."""
        user_data = self.get_user_data(server_id, user_id)

        if not user_data:
            # Si el usuario no existe en la base de datos, lo creamos
            new_xp = xp_to_add
            new_level = 1
            query = """
                INSERT INTO user_levels (server_id, user_id, xp, level, last_message_at)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            execute_query(query, (server_id, user_id, new_xp, new_level))
            return 0  # No avisamos que subió a nivel 1 porque es el inicial
        else:
            current_xp = user_data["xp"]
            current_level = user_data["level"]

            new_xp = current_xp + xp_to_add

            # Ecuación matemática: Nivel = 0.1 * raíz cuadrada de XP
            # Esto significa que los primeros niveles son rápidos, y luego requieren más XP
            calculated_level = math.floor(0.1 * math.sqrt(new_xp))
            if calculated_level < 1:
                calculated_level = 1

            leveled_up = False
            if calculated_level > current_level:
                current_level = calculated_level
                leveled_up = True

            query = """
                UPDATE user_levels
                SET xp = %s, level = %s, last_message_at = CURRENT_TIMESTAMP
                WHERE server_id = %s AND user_id = %s
            """
            execute_query(query, (new_xp, current_level, server_id, user_id))

            return current_level if leveled_up else 0

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignorar mensajes de otros bots o mensajes por MD
        if message.author.bot or not message.guild:
            return

        user_id = message.author.id
        server_id = message.guild.id

        # 1. Verificar si el usuario está en cooldown
        now = datetime.now()
        if user_id in self.cooldowns:
            last_time = self.cooldowns[user_id]
            if (now - last_time).total_seconds() < self.COOLDOWN_SECONDS:
                return  # Aún no han pasado los 10 segundos, no dar XP

        # 2. Registrar el nuevo tiempo y otorgar XP aleatoria
        self.cooldowns[user_id] = now
        xp_gained = random.randint(15, 25)

        new_level = self.add_user_xp(server_id, user_id, xp_gained)

        # 3. Anunciar si el usuario subió de nivel
        if new_level > 0:
            embed = discord.Embed(
                title="🎉 ¡Subida de Nivel!",
                description=f"¡Felicidades {message.author.mention}! Has alcanzado el **Nivel {new_level}**.",
                color=discord.Color.gold()
            )
            # Puedes configurar para que lo envíe a un canal específico si lo deseas
            await message.channel.send(embed=embed)

    @app_commands.command(name="rank", description="Muestra tu nivel actual y experiencia.")
    async def rank(self, interaction: discord.Interaction, member: discord.Member = None):
        target = member or interaction.user
        if target.bot:
            await interaction.response.send_message("🤖 Los bots no pueden tener nivel.", ephemeral=True)
            return

        server_id = interaction.guild_id if interaction.guild else 0
        user_data = self.get_user_data(server_id, target.id)

        if not user_data:
            await interaction.response.send_message(f"📉 {target.display_name} aún no tiene experiencia en este servidor.")
            return

        current_xp = user_data["xp"]
        current_level = user_data["level"]

        # XP requerida para el siguiente nivel
        next_level_xp = 100 * ((current_level + 1) ** 2)
        # XP base del nivel actual
        base_xp = 100 * (current_level ** 2) if current_level > 1 else 0

        # Cálculo de la barra de progreso
        xp_needed_for_level = next_level_xp - base_xp
        xp_gained_this_level = current_xp - base_xp
        progress_percentage = xp_gained_this_level / xp_needed_for_level if xp_needed_for_level > 0 else 0

        # Crear barra de progreso visual
        filled_blocks = int(progress_percentage * 10)
        empty_blocks = 10 - filled_blocks
        progress_bar = ("█" * filled_blocks) + ("░" * empty_blocks)

        embed = discord.Embed(title=f"Estadísticas de {target.display_name}", color=discord.Color.blue())
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="Nivel", value=f"**{current_level}**", inline=True)
        embed.add_field(name="XP Total", value=f"**{current_xp}** XP", inline=True)
        embed.add_field(name="Progreso al Siguiente Nivel", value=f"`[{progress_bar}]` ({xp_gained_this_level}/{xp_needed_for_level} XP)", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Levels(bot))
