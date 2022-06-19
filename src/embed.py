from nextcord import Embed, Interaction
from nextcord.ext import commands
from src.find_recipe import separate_ingredients
import asyncio


async def create_embed(bot, interaction: Interaction, items: list) -> Embed:
    pages = []
    for item in range(len(items)):
        name_of_recipe = items[item][1]["Recipe"]
        recipe_author = items[item][1]["Name"]
        ingredients = items[item][1]["Ingredients"]
        sep = separate_ingredients(ingredients)
        embed = Embed(
            title=name_of_recipe.capitalize(), description=sep)
        embed.set_author(
            name=f"{name_of_recipe.capitalize()} by {recipe_author}"
        )
        embed.add_field(
            name='Instructions', value=items[item][1]["Instructions"], inline=False
        )
        embed.add_field(
            name='Author', value=items[item][1]["Name"], inline=False
        )
        pages.append(embed)

    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
    current = 0
    msg = await interaction.channel.send(embed=pages[current])

    for button in buttons:
        await msg.add_reaction(button)

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == interaction.user and reaction.emoji in buttons, timeout=60.0)

        except asyncio.TimeoutError:
            return print("Recipe has timed out.")

        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0

            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1

            elif reaction.emoji == u"\u27A1":
                if current < len(pages)-1:
                    current += 1

            elif reaction.emoji == u"\u23E9":
                current = len(pages)-1

            for button in buttons:
                await msg.remove_reaction(button, interaction.user)

            if current != previous_page:
                await msg.edit(embed=pages[current])
