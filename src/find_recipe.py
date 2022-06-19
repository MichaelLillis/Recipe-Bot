from src.create_recipe import db


def recipe_find(input: str) -> list:
    try:
        if input.startswith("<@!"):
            author_id = int(''.join(filter(str.isdigit, input)))
            recipes = db.child("Recipes").order_by_child(
                "Author").equal_to(author_id).get()
        else:
            recipe_name = input.capitalize()
            recipes = db.child("Recipes").order_by_child(
                "Recipe").equal_to(recipe_name).get()
        our_recipe = recipes.val()
        items = list(our_recipe.items())
        return items
    except:
        return 0


def separate_ingredients(items: list) -> str:
    recipe_ingredients = items
    ingredients = ' '
    for x in recipe_ingredients:
        if x != recipe_ingredients[-1]:
            ingredients += x + ', '
        else:
            ingredients += x
    return ingredients
