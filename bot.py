import nextcord
import nextcord.ext.commands
import os
import pyrebase
from dotenv import load_dotenv
from database import firebaseConfig

client = nextcord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# TODO: Setup inital command with modal prompting users of recipe name/ingredients


# TODO: Setup databse (FireBase)
firebase = pyrebase.initialize_app(firebaseConfig)


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
