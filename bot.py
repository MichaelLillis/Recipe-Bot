from dataclasses import dataclass
import nextcord
import nextcord.ext.commands
from nextcord.ext import menus
import os
from datetime import datetime
from dotenv import load_dotenv
from requests_toolbelt import user_agent
from database import patch
from create_recipe import db, new_recipe, Success, Failed
from find_recipe import recipe_find, separate_ingredients
import string


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
        ingredient_list = self.ingredients.value.split(", ")
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        Add = new_recipe(
            self.recipe_title.value,
            ingredient_list,
            self.instructions.value,
            date_time,
            interaction.user.display_name,
            interaction.user.id
        )
        if Add == True:
            await interaction.send(
                f"{Success}"
            )
        else:
            await interaction.send(
                f"{Failed}"
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

# TODO: Get specific recipe from database:
# 'if name/recipe exists... do logic to parse ingredients, and embed a message'
# Message should have multiple pages (if necesary, page per recipe)


@recipe.subcommand(description="Find a specific recipe")
async def find(interaction: nextcord.Interaction, *, input: str):
    # TODO: Setup embeds with pages
    # TODO: setup functionality for querying the database - seperate getting recipes to diff function
    if input.startswith("<@!"):
        items = recipe_find(input)
        for x in range(len(items)):
            name_of_recipe = items[x][1]["Recipe"]
            recipe_author = items[x][1]["Name"]
            ingredients = items[x][1]["Ingredients"]
            sep = separate_ingredients(ingredients)
            embed = nextcord.Embed(
                title=name_of_recipe.capitalize(), description=sep)
            embed.set_author(
                name=f"{name_of_recipe.capitalize()} by {recipe_author}"
            )
            embed.add_field(
                name='Instructions', value=items[x][1]["Instructions"], inline=False
            )
            embed.add_field(
                name='Author', value=items[x][1]["Name"], inline=False
            )
            await interaction.send(embed=embed)

        # await interaction.send(f"TEST - recipe with author exists")
    # TODO: Setup grabbing recipe using recipe
    else:
        await interaction.send("TEST - recipe with author exists")

    # else:
    #     recipes = db.child("Recipes").order_by_child(
    #         "Author").equal_to(input).get()

    # if recipes > 0:
        # TODO: setup embed with pages based on number of results from DB
        # await interaction.send("working.")
    # else:
    #     await interaction.send("Recipe with that author/name does not exist.")


# TODO: Get random recipe from database

try:
    bot.run(token)
except Exception as e:
    print(f"Error - Login Failed: {e}")
