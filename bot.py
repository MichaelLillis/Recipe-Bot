import nextcord
import nextcord.ext.commands
import os
from datetime import date
import pyrebase
from dotenv import load_dotenv
from database import firebaseConfig, SERVER
# client = nextcord.Client()

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
            f"Recipe name: {self.recipe_title.value}\n"
            f"Recipe from {interaction.user.mention}\n"
            f"Ingredients: {self.ingredients.value}\n"
            f"How to make the recipe: {self.instructions.value}\n"
        )
        # TODO Call db function
        # new_recipe(self.recipe_title.value, )


class Bot(nextcord.ext.commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_modals_added = False
        self.synced = False

    async def on_ready(self):
        if not self.persistent_modals_added:
            # Register the persistent modal for listening here.
            # Note that this does not display the modal to the user.
            # To do that, you need to respond to an interaction as shown below.
            self.add_modal(RecipeModal())
            self.persistent_modals_added = True

        print(f"Logged in as {self.user} (ID: {self.user.id})")


bot = Bot(command_prefix="!")


@bot.slash_command(
    description="Add a recipe to the recipes list!",
    guild_ids=[SERVER],
)
async def recipes(interaction: nextcord.Interaction):
    await interaction.response.send_modal(RecipeModal())
# @client.event
# async def on_ready():
#     print(f'We have logged in as {client.user}')

# TODO: Setup inital command with modal prompting users of recipe name/ingredients


@bot.slash_command(description="Recipe bot commands!", guild_ids=[SERVER])
# @nextcord.ext.commands.cooldown(1, 60, type=nextcord.ext.commands.BucketType.default)
async def recipe(interaction: nextcord.Interaction):
    pass


@recipe.subcommand(description="Add a recipe to the recipe list")
async def add(interaction: nextcord.Interaction):
    await interaction.response.send_message("Added recipe!")

# TODO: Get specific recipe from database

# TODO: Get random recipe from database

# TODO: Setup databse (FireBase)


def new_recipe(recipe_name: str, ingredient_list: list[str], instructions: str, date: date, user: str):
    try:
        for ingredients in range(len(ingredient_list)):
            ingredient = ingredient_list[ingredients]
            ingredient = ingredient.lower()
            for letters in range(len(ingredient) - 1):
                currentletter = ingredient_list[ingredients][letters]
                nextletter = ingredient_list[ingredients][letters + 1]
                if currentletter == ' ' and nextletter.isalpha():
                    nextletter = nextletter.upper()

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
    load_dotenv()
    token = os.getenv("TOKEN")
    bot.run(token)
except Exception as e:
    print(f"Error - Login Failed: {e}")
