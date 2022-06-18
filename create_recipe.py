import pyrebase
from database import firebaseConfig

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

def new_recipe(recipe_name: str, ingredient_list: list[str], instructions: str, date: str, user: str, user_id: int):
    try:
        ingredient_list = cap(ingredient_list)
        data = {
            "Recipe": recipe_name,
            "Ingredients": ingredient_list,
            "Instructions": instructions,
            "Date created": date,
            "Author": user_id,
            "Name": user
        }
        db.child("Recipes").child(f"{recipe_name} by {user}").set(data)
    except Exception as e:
        print(f"Error - Data Entry Add Failed: {e}")


def cap(words) -> list:
    return [s.capitalize() for s in words]
