import nextcord
from nextcord.ext import commands
import src.setup_modal
from main import server
import pyrebase
try:
    import config
    firebase = pyrebase.initialize_app(config.firebaseConfig)
    db = firebase.database()
except Exception as e:
    print(f"Error - Run the setup command: {e}")


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        description="Setup the database config",
        guild_ids=[int(server)],
    )
    async def setup(self, interaction: nextcord.Interaction):
        await interaction.response.send_modal(src.setup_modal.SetupModal())


def setup(bot):
    bot.add_cog(Setup(bot))
