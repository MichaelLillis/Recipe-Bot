import nextcord
import nextcord.ext.commands
import os
from datetime import date, datetime
import pyrebase
from dotenv import load_dotenv
from database import firebaseConfig
import string

# TODO Modal


class RecipeModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="Recipes",
            timeout=None,
            custom_id="persistent_modal:Recipes",
        )

        self.recipe_title = nextcord.ui.TextInput(
            label="Recipe Title",
            placeholder="e.g. Good Old Fashioned Pancakes!",
            required=True,
            style=nextcord.TextInputStyle.short,
            custom_id="persistent_modal:recipe_title",
        )
        self.add_item(self.recipe_title)

        self.ingredients = nextcord.ui.TextInput(
            label="List of recipe ingredients",
            placeholder="1½ cups all-purpose flour, 3½ teaspoons baking powder¼ teaspoon salt or more to taste...",
            required=True,
            custom_id="persistent_modal:ingredients",
        )
        self.add_item(self.ingredients)

        self.instructions = nextcord.ui.TextInput(
            label="How to make the recipe",
            placeholder="e.g. Step 1 In a large bowl, sift together the flour...",
            style=nextcord.TextInputStyle.paragraph,
            required=True,
            custom_id="persistent_modal:instructions",
        )
        self.add_item(self.instructions)

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.send(
            f"Recipe added!"
        )
        # TODO Call db function
        ingredient_list = self.ingredients.value.split(", ")
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        new_recipe(
            self.recipe_title.value,
            ingredient_list,
            self.instructions.value,
            date_time,
            interaction.user.name
        )


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
prefix = os.getenv("PREFIX")
token = os.getenv("TOKEN")
server = os.getenv("SERVER")
bot = Bot(prefix)


# async def recipes(interaction: nextcord.Interaction):
#     await interaction.response.send_modal(RecipeModal())


@bot.slash_command(
    description="Add a recipe to the recipes list!",
    guild_ids=[int(server)],
)
async def recipe(interaction: nextcord.Interaction):
    pass


@recipe.subcommand(description="Add a recipe to the recipe list")
async def add(interaction: nextcord.Interaction):
    await interaction.response.send_modal(RecipeModal())

# TODO: Get specific recipe from database:
# 'if name/recipe exists... do logic to parse ingredients, and embed a message'
# Message should have multiple pages (if necesary, page per recipe)


@recipe.subcommand(description="Find a specific recipe")
async def find(interaction: nextcord.Interaction):
    embed = nextcord.Embed(
        title="title", description="desc")
    embed.add_field(name="Name", value="field")
    await interaction.send(embed=embed)

# TODO: Get random recipe from database


def new_recipe(recipe_name: str, ingredient_list: list[str], instructions: str, date: str, user: str):
    try:
        for i in ingredient_list:
            i = i.capitalize()

        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()
        data = {
            "Recipe": recipe_name,
            "Ingredients": ingredient_list,
            "Instructions": instructions,
            "Date created": date,
            "Author": user
        }
        db.child(f"{recipe_name} by {user}").set(data)
    except Exception as e:
        print(f"Error - Data Entry Add Failed: {e}")


# TODO: Take input of users and pass it to database
try:
    bot.run(token)
except Exception as e:
    print(f"Error - Login Failed: {e}")
