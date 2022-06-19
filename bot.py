import nextcord
import nextcord.ext.commands
import nextcord.ext
import os
from dotenv import load_dotenv
from database import patch
from src.find_recipe import recipe_find
from src.modal import RecipeModal
from src.embed import create_embed


class Bot(nextcord.ext.commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_modals_added = False
        self.synced = False

    async def on_ready(self):
        if not self.persistent_modals_added:
            self.add_modal(RecipeModal())
            self.persistent_modals_added = True
        print(f"Logged in as {self.user} (ID: {self.user.id})")


load_dotenv()
patch()
token = os.getenv("TOKEN")
server = os.getenv("SERVER")
prefix = os.getenv("PREFIX")
bot = Bot(prefix)


@bot.slash_command(
    description="Add a recipe to the recipes list!",
    guild_ids=[int(server)],
)
async def recipe(interaction: nextcord.Interaction):
    pass


@recipe.subcommand(description="Add a recipe to the recipe list")
async def add(interaction: nextcord.Interaction):
    await interaction.response.send_modal(RecipeModal())


@recipe.subcommand(description="Find a specific recipe")
async def find(interaction: nextcord.Interaction, *, input: str):
    items = recipe_find(input)
    if items == 0:
        await interaction.send("A recipe with this user or recipe name does not exist.")
    else:
        await create_embed(bot, interaction, items)

# TODO: Get random recipe from database

try:
    bot.run(token)
except Exception as e:
    print(f"Error - Login Failed: {e}")
