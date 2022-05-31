from nextcord.ext import commands

# TODO: config functionality w/ prefix
bot = commands.Bot(config["prefix"])
print("Loading bot...")

# TODO: Setup inital command with modal prompting users of recipe name/ingredients


# TODO: Setup databse (SQL)


# TODO: Take input of users and pass it to database


# TODO: Setup server w/ bot
# TODO: Setup token functionality w/ config
try:
    bot.run(config["token"])
except Exception as e:
    print(f"Error - Login Failed: {e}")
