import nextcord
import nextcord.ext.commands
import os
from datetime import date
import pyrebase
from dotenv import load_dotenv
from database import firebaseConfig

client = nextcord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# TODO: Setup inital command with modal prompting users of recipe name/ingredients


# TODO: Setup databse (FireBase)
def new_recipe(recipe_name: str, ingredient_list: list[str], date: date, user: str):
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    data = {
        "Recipe": recipe_name,
        "Ingredients": ingredient_list,
        "Date created": date, "Author": user
    }
    db.child("Recipes").set(data)

# TODO: Take input of users and pass it to database


@client.slash_command
async def add_recipe(ctx):
    pass
    # TODO: Get specific recipe from database

    # TODO: Get random recipe from database

try:
    load_dotenv()
    token = os.getenv("TOKEN")
    client.run(token)
except Exception as e:
    print(f"Error - Login Failed: {e}")
