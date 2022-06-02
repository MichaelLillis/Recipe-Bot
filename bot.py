import nextcord
import nextcord.ext.commands
import os
import pyrebase
from database import firebaseConfig
client = nextcord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# TODO: Setup inital command with modal prompting users of recipe name/ingredients


# TODO: Setup databse (SQL)
firebase = pyrebase.initialize_app(firebaseConfig)


# TODO: Take input of users and pass it to database
@client.slash_command
async def add_recipe(ctx):

    # TODO: Get specific recipe from database

    # TODO: Get random recipe from database

try:
    client.run(os.getenv('TOKEN'))
except Exception as e:
    print(f"Error - Login Failed: {e}")
