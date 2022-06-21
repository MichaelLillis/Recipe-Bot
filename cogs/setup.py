from nextcord import Permissions
import nextcord
from nextcord.ext import commands
from src.setup_modal import SetupModal
from main import server


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        description="Setup the database config",
        guild_ids=[int(server)],
    )
    async def setup(self, interaction: nextcord.Interaction):
        await interaction.response.send_modal(SetupModal())


def setup(bot):
    bot.add_cog(Setup(bot))
