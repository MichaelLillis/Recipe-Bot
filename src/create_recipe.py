import pyrebase
from database import firebaseConfig

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
Success = "Recipe added!"
Failed = "Error - Recipe Add Failed. Make sure you don't already have a recipe with this name."


def new_recipe(recipe_name: str, ingredient_list: list[str], instructions: str, date: str, user: str, user_id: int) -> bool:
    try:
        ingredient_list = cap(ingredient_list)
        recipe_name = recipe_name.lower()
        recipe_and_author = recipe_name+str(user_id)
        data = {
            "Recipe": recipe_name,
            "Ingredients": ingredient_list,
            "Instructions": instructions,
            "Date created": date,
            "Author": user_id,
            "Name": user,
            "RecipeAndAuthor": recipe_and_author
        }
        db.child("Recipes").child(f"{recipe_name} by {user}").set(data)
        print(Success)
        return True
    except Exception as e:
        print(f"{Failed} {e}")
        return False


def cap(words) -> list:
    return [s.capitalize() for s in words]
