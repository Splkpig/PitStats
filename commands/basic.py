import discord
from discord.ext import commands
from discord import app_commands

pitpandaSignatures = discord.Embed(title="PitPanda Signatures", color=discord.Color.greyple())
pitpandaSignatures.add_field(name="/prestige-level *player*", value="Displays a player's prestige and level PitPanda signature", inline=False)
pitpandaSignatures.add_field(name="/profile *player*", value="Displays a player's profile PitPanda signature", inline=False)

prestigeCalculations = discord.Embed(title="Prestige Calculations", color=discord.Color.greyple())
prestigeCalculations.add_field(name="/prestige-info *player*", value="Displays a player's prestige progress", inline=False)
prestigeCalculations.add_field(name="/kings-quest *player*", value="Displays the granted XP from completing a King's Quest", inline=False)
prestigeCalculations.add_field(name="/xp-until *player*", value="Calculates the needed XP until reaching a certain Prestige and Level", inline=False)

funCommands = discord.Embed(title="Fun Commands", color=discord.Color.greyple())
funCommands.add_field(name="/jenna *player*", value="Compares a player's yapping to Jenna's", inline=False)

helpPages = [pitpandaSignatures, prestigeCalculations, funCommands]
currentPage = -1


class simpleView(discord.ui.View):
    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        global currentPage
        global helpPages

        if currentPage == -1:
            currentPage = 0

        if currentPage <= 0:
            embed = helpPages[currentPage]
            view = simpleView(timeout=None)

            await interaction.response.edit_message(embed=embed, view=view) # noqa
        else:
            embed = helpPages[currentPage - 1]
            view = simpleView(timeout=None)
            currentPage -= 1

            await interaction.response.edit_message(embed=embed, view=view) # noqa

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple)
    async def forward(self, interaction: discord.Interaction, button: discord.ui.Button):
        global currentPage
        global helpPages

        print(currentPage)

        if currentPage <= 0:
            currentPage += 1

        if currentPage == len(helpPages) - 1:
            embed = helpPages[currentPage]
            view = simpleView(timeout=None)

            await interaction.response.edit_message(embed=embed, view=view) # noqa
        else:
            embed = helpPages[currentPage]
            view = simpleView(timeout=None)
            currentPage += 1

            await interaction.response.edit_message(embed=embed, view=view) # noqa


class helpCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    global currentPage

    @app_commands.command(name="help", description="Displays the bot's commands")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Page through the bot's different commands", color=discord.Color.greyple())

        view = simpleView(timeout=None)

        await interaction.response.send_message(embed=embed, view=view)  # noqa


async def setup(client: commands.Bot) -> None:
    await client.add_cog(helpCommand(client))
