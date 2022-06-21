from discord import Permissions
import nextcord
from nextcord.ext import commands
from src.setup_modal import SetupModal
from recipe import server


class Recipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        description="Add a recipe to the recipes list!",
        guild_ids=[int(server)],
        default_member_permissions=Permissions(administrator=True)
    )
    async def setup(self, interaction: nextcord.Interaction):
        await interaction.response.send_modal(SetupModal())


def setup(bot):
    bot.add_cog(Recipe(bot))
