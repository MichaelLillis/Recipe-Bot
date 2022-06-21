import nextcord
import nextcord.ext
import nextcord.ext.commands
import os
from dotenv import load_dotenv
from database import patch


class Bot(nextcord.ext.commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_modals_added = False
        self.synced = False

    async def on_ready(self):
        if not self.persistent_modals_added:
            self.persistent_modals_added = True
        print(f"Logged in as {self.user} (ID: {self.user.id})")


load_dotenv()
patch()
token = os.getenv("TOKEN")
prefix = os.getenv("PREFIX")
server = os.getenv("SERVER")
bot = Bot(prefix)
cog_list = []
for fn in os.listdir("./cogs"):
    if fn.endswith(".py"):
        cog_list.append(f"cogs.{fn[:-3]}")
bot.load_extension("cogs.setup")


@bot.slash_command(
    description="Setup the database config",
    guild_ids=[int(server)],
)
async def load(interaction: nextcord.Interaction):
    bot.unload_extension("cogs.setup")
    for cogs in cog_list:
        bot.load_extension(cogs)
    await interaction.send("Loaded cogs")
try:
    bot.run(token)
except Exception as e:
    print(f"Error - Login Failed: {e}")
