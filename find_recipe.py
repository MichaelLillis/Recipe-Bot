from create_recipe import db


def recipe_find(input: str) -> list:
    author_id = int(''.join(filter(str.isdigit, input)))
    recipes = db.child("Recipes").order_by_child(
        "Author").equal_to(author_id).get()
    our_recipe = recipes.val()
    items = list(our_recipe.items())
    return items


def separate_ingredients(items: list) -> str:
    recipe_ingredients = items
    ingredients = ' '
    for x in recipe_ingredients:
        if x != recipe_ingredients[-1]:
            ingredients += x + ', '
        else:
            ingredients += x
    return ingredients
