from nextcord import ui, TextInputStyle, Interaction
from src.create_recipe import new_recipe, Success, Failed
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
            style=TextInputStyle.short,
            custom_id="persistent_modal:recipe_title",
        )
        self.add_item(self.recipe_title)

        self.ingredients = ui.TextInput(
            label="List of recipe ingredients",
            placeholder="1½ cups all-purpose flour, 3½ teaspoons baking powder¼ teaspoon salt or more to taste...",
            required=True,
            custom_id="persistent_modal:ingredients",
        )
        self.add_item(self.ingredients)

        self.instructions = ui.TextInput(
            label="How to make the recipe",
            placeholder="Step 1 In a large bowl, sift together the flour...",
            style=TextInputStyle.paragraph,
            required=True,
            custom_id="persistent_modal:instructions",
        )
        self.add_item(self.instructions)

    async def callback(self, interaction: Interaction):
        ingredient_list = self.ingredients.value.split(", ")
        date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        Add = new_recipe(
            self.recipe_title.value,
            ingredient_list,
            self.instructions.value,
            date_time,
            interaction.user.display_name,
            interaction.user.id
        )
        if Add:
            await interaction.send(
                f"{Success}"
            )
        else:
            await interaction.send(
                f"{Failed}"
            )
