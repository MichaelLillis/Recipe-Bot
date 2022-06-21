from cgi import print_arguments
from nextcord import Embed, Interaction
import nextcord
import string
from src.find_recipe import separate_ingredients
import asyncio


async def create_embed(bot, interaction: Interaction, items: list) -> Embed:
    pages = []
    for item in range(len(items)):
        name_of_recipe = string.capwords(items[item][1]["Recipe"])
        ingredients = items[item][1]["Ingredients"]
        sep = separate_ingredients(ingredients)
        embed = Embed(title=name_of_recipe, color=nextcord.Color.green())
        embed.add_field(
            name='Author', value=items[item][1]["Name"], inline=False
        )
        embed.add_field(
            name='Ingredients', value=sep, inline=False
        )
        if len(items[item][1]["Instructions"]) < 1024:
            embed.add_field(
                name='Instructions', value=items[item][1]["Instructions"], inline=False
            )
        elif len(items[item][1]["Instructions"]) > 1024 and len(items[item][1]["Instructions"]) < 2047:
            s1 = items[item][1]["Instructions"][:len(
                items[item][1]["Instructions"])//2]
            s2 = items[item][1]["Instructions"][len(
                items[item][1]["Instructions"])//2:]
            items[item][1]["Instructions"]
            embed.add_field(
                name='Instructions 1/2', value=s1, inline=False
            )
            embed.add_field(
                name='Instructions 2/2', value=s2, inline=False
            )
        elif len(items[item][1]["Instructions"]) > 2048:
            s1 = items[item][1]["Instructions"][:len(
                items[item][1]["Instructions"])//2]
            s2 = items[item][1]["Instructions"][len(
                items[item][1]["Instructions"])//2:]
            items[item][1]["Instructions"]
            s3 = s1[:len(
                s1)//2]
            s4 = s2[:len(
                s2)//2]
            s5 = s1[len(
                s1)//2:]
            s6 = s2[len(
                s2)//2:]
            embed.add_field(
                name='Instructions 1/4', value=s3, inline=False
            )
            embed.add_field(
                name='Instructions 2/4', value=s5, inline=False
            )
            embed.add_field(
                name='Instructions 3/4', value=s4, inline=False
            )
            embed.add_field(
                name='Instructions 4/4', value=s6, inline=False
            )
        pages.append(embed)

    if (len(pages) == 1):
        await interaction.send(embed=pages[0])
    else:
        buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
        current_page = 0
        msg = await interaction.channel.send(embed=pages[current_page])

        for button in buttons:
            await msg.add_reaction(button)

        while True:
            try:
                reaction, user = await bot.wait_for(
                    "reaction_add",
                    check=lambda reaction,
                    user: user == interaction.user and reaction.emoji in buttons,
                    timeout=300.0)

            except asyncio.TimeoutError:
                return print("Recipe has timed out.")

            else:
                previous_page = current_page
                if reaction.emoji == u"\u23EA":
                    current_page = 0

                elif reaction.emoji == u"\u2B05":
                    if current_page > 0:
                        current_page -= 1

                elif reaction.emoji == u"\u27A1":
                    if current_page < len(pages)-1:
                        current_page += 1

                elif reaction.emoji == u"\u23E9":
                    current_page = len(pages)-1

                for button in buttons:
                    await msg.remove_reaction(button, interaction.user)

                if current_page != previous_page:
                    await msg.edit(embed=pages[current_page])
