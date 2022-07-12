import pyrebase
from src.helper import cap
try:
    from database import firebaseConfig
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
except Exception as e:
    print(f"Setup the config: {e}")
Success = "Recipe added!"
Failed = "Error - Recipe Add Failed. Make sure you don't already have a recipe with this name."


class Recipe():
    def __init__(
        self,
        recipe_name: str,
        ingredient_list: list[str],
        instructions: str,
        date: str,
        user: str,
        user_id: int
        ) -> None:

        self.recipe_name = recipe_name
        self.ingredient_list = ingredient_list
        self.instructions = instructions
        self.date = date
        self.user = user 
        self.user_id = user_id
    def new_recipe(self) -> bool:
        ingredient_list = cap(self.ingredient_list)
        recipe_name = self.recipe_name.lower()
        data = {
            "Recipe": recipe_name,
            "Ingredients": ingredient_list,
            "Instructions": self.instructions,
            "Date created": self.date,
            "Author": self.user_id,
            "Name": self.user,
        }
        try:
            db.child("Recipes").child(f"{recipe_name} by {self.user}").set(data)
            print(Success)
            return True
        except Exception as e:
            print(f"{Failed} {e}")
            return False