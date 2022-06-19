import asyncio
from asyncio.windows_events import NULL
from email import message
import nextcord
import nextcord.ext.commands
# from nextcord.ext import menus
import nextcord.ext
import os
from dotenv import load_dotenv
from database import patch
from src.find_recipe import recipe_find, separate_ingredients
from src.modal import RecipeModal


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

    items = recipe_find(input)
    if items == 0:
        await interaction.send("A recipe with this user or recipe name does not exist.")
    else:
        await create_embed(interaction, items)


def create_recipe(interation: nextcord.Interaction, items: list) -> nextcord.Embed:
    pages = []
    for item in range(len(items)):
        name_of_recipe = items[item][1]["Recipe"]
        recipe_author = items[item][1]["Name"]
        ingredients = items[item][1]["Ingredients"]
        sep = separate_ingredients(ingredients)
        embed = nextcord.Embed(
            title=name_of_recipe.capitalize(), description=sep)
        embed.set_author(
            name=f"{name_of_recipe.capitalize()} by {recipe_author}"
        )
        embed.add_field(
            name='Instructions', value=items[item][1]["Instructions"], inline=False
        )
        embed.add_field(
            name='Author', value=items[item][1]["Name"], inline=False
        )
        pages.append(embed)

    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
    current = 0
    msg = await interaction.channel.send(embed=pages[current])

    for button in buttons:
        await msg.add_reaction(button)

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == interaction.user and reaction.emoji in buttons, timeout=60.0)

        except asyncio.TimeoutError:
            return print("Recipe has timed out.")

        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0

            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1

            elif reaction.emoji == u"\u27A1":
                if current < len(pages)-1:
                    current += 1

            elif reaction.emoji == u"\u23E9":
                current = len(pages)-1

            for button in buttons:
                await msg.remove_reaction(button, interaction.user)

            if current != previous_page:
                await msg.edit(embed=pages[current])


# TODO: Get random recipe from database

try:
    bot.run(token)
except Exception as e:
    print(f"Error - Login Failed: {e}")
