import nextcord
import nextcord.ext.commands
import os

client = nextcord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# TODO
# Command to add recipe

# TODO
# Get specific recipe

# TODO
# Get random recipe

client.run(os.getenv('TOKEN'))
