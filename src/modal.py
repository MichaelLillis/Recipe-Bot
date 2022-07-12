from nextcord import ui, TextInputStyle, Interaction
from src.recipe_object import Recipe, Success, Failed
from datetime import datetime


class RecipeModal(ui.Modal):
    def __init__(self):
        super().__init__(
            title="Recipes",
            timeout=None,
            custom_id="persistent_modal:Recipes",
        )

        self.recipe_title = ui.TextInput(
            label="Recipe Title",
            placeholder="Good Old Fashioned Pancakes!",
            required=True,
            max_length=100,
            style=TextInputStyle.short,
            custom_id="persistent_modal:recipe_title",
        )
        self.add_item(self.recipe_title)

        self.ingredients = ui.TextInput(
            label="List of recipe ingredients",
            placeholder="1½ cups all-purpose flour, 3½ teaspoons baking powder¼ teaspoon salt or more to taste...",
            max_length=1000,
            style=TextInputStyle.paragraph,
            required=True,
            custom_id="persistent_modal:ingredients",
        )
        self.add_item(self.ingredients)

        self.instructions = ui.TextInput(
            label="How to make the recipe",
            placeholder="Step 1: Add flour into a large bowl. Step 2: Add the eggs...",
            max_length=2000,
            style=TextInputStyle.paragraph,
            required=True,
            custom_id="persistent_modal:instructions",
        )
        self.add_item(self.instructions)

    async def callback(self, interaction: Interaction):
        recipe = Recipe()
        recipe.ingredient_list = self.ingredients.value.split(", ")
        recipe.date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        recipe.recipe_name = self.recipe_title.value
        recipe.instructions = self.instructions.value
        recipe.user = interaction.user.display_name
        recipe.user_id = interaction.user.id
        Add = recipe.new_recipe(recipe)
        if Add:
            await interaction.send(
                f"{Success}"
            )
        else:
            await interaction.send(
                f"{Failed}"
            )
