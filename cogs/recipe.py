import nextcord
from nextcord.ext import commands
from main import server
try:
    from setup import db
    from src.modal import RecipeModal
    from src.find_recipe import recipe_delete, recipe_find
    from src.embed import create_embed
except Exception as e:
    print(f"Error - Run the setup command: {e}")


class Recipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        description="Add a recipe to the recipes list!",
        guild_ids=[int(server)],
    )
    async def recipe(self, interaction: nextcord.Interaction):
        pass

    @recipe.subcommand(description="Add a recipe to the recipe list")
    async def add(self, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RecipeModal())

    @recipe.subcommand(description="Find a specific recipe")
    async def find(self, interaction: nextcord.Interaction, *, input: str):
        items = recipe_find(input)
        if items == 0:
            await interaction.send("A recipe with this user or recipe name does not exist.")
        else:
            await create_embed(self.bot, interaction, items)

    @recipe.subcommand(description="Find a specific recipe")
    async def delete(self, interaction: nextcord.Interaction, *, input: str):
        msg = recipe_delete(
            input.lower(), interaction.user.id, interaction.user.display_name)
        await interaction.send(msg)

    @recipe.subcommand(description="Return all recipes")
    async def all(self, interaction: nextcord.Interaction):
        try:
            recipes = db.child("Recipes").order_by_child(
                "Recipe").get()
            our_recipe = recipes.val()
            items = list(our_recipe.items())
            await create_embed(self.bot, interaction, items)
        except:
            await interaction.send("No recipes exist in the database.")


def setup(bot):
    bot.add_cog(Recipe(bot))
