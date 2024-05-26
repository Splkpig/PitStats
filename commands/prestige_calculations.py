import discord
from discord.ext import commands
from discord import app_commands
from useful_things.api_functions import getInfo
from useful_things.discord_functions import footerDateGen
from useful_things import formatting_functions
from useful_things.file_functions import read_specific_line
from useful_things import pit_functions

globalPrestige = 0
globalLevel = 0
globalPlayer = ""


class simpleView(discord.ui.View):

    @discord.ui.button(label="View data breakdown", style=discord.ButtonStyle.blurple)
    async def showDataBreakdown(self, interaction: discord.Interaction, button: discord.ui.Button):
        global globalPrestige
        global globalLevel
        global globalPlayer

        urlPP: str = f"https://pitpanda.rocks/api/players/{globalPlayer}"
        dataPP = getInfo(urlPP)
        docData = dataPP["data"]["doc"]

        currentXP = docData["xp"]
        goalXP = int(read_specific_line("../PitStats/useful_things/pitdata/xp_sums.txt", globalPrestige - 1))
        goalXPFromFinalPrestige = pit_functions.calculateXPForLevel(globalPrestige, globalLevel)
        goalXP += goalXPFromFinalPrestige
        currentPrestige = len(dataPP["data"]["prestiges"]) - 1
        currentLevel = formatting_functions.extract_substring(dataPP['data']['formattedLevel'])

        neededXP = goalXP - currentXP

        embed = discord.Embed(title=f"XP until for {dataPP['data']['name']}", color=pit_functions.calcBracketColor(globalPrestige))
        embed.set_footer(text=footerDateGen())
        embed.add_field(name=f"[{formatting_functions.int_to_roman(globalPrestige)}-{globalLevel}]:",
                        value=f"{formatting_functions.add_commas(goalXP)} XP required", inline=False)
        embed.add_field(name=f"[{formatting_functions.int_to_roman(currentPrestige)}-{currentLevel}] {dataPP['data']['name']} currently has:",
                        value=f"{formatting_functions.add_commas(currentXP)} XP", inline=False)
        embed.add_field(name=f"To reach [{formatting_functions.int_to_roman(globalPrestige)}-{globalLevel}]: ",
                        value=f"{formatting_functions.add_commas(neededXP)} XP required", inline=False)
        embed.add_field(name=f"At {formatting_functions.add_commas(int(dataPP['data']['doc']['xpHourly']))} XP per hour:", value=f"{formatting_functions.add_commas(neededXP)} XP will take {formatting_functions.add_commas(int(neededXP / dataPP['data']['doc']['xpHourly']))} hours", inline=False)

        await interaction.response.send_message(embed=embed)  # noqa
        self.stop()


class prestigeCalculations(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="prestige-info", description="Shows XP and Gold info for current prestige")
    async def prestige_info(self, interaction: discord.Interaction, player: str):
        """my command description
        Args:
            player (str): A Minecraft username
        """
        pass

        urlPP: str = f"https://pitpanda.rocks/api/players/{player}"
        dataPP = getInfo(urlPP)

        if not dataPP["success"]:
            embedFail = discord.Embed(title="Player not found", color=discord.Color.red())

            await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa
        else:
            xpProgress = dataPP["data"]["xpProgress"]
            goldProgress = dataPP["data"]["goldProgress"]
            currentXP = xpProgress["displayCurrent"]
            prestigeGoalXP = xpProgress["displayGoal"]
            currentGoldGrinded = goldProgress["displayCurrent"]
            prestigeGoalGold = goldProgress["displayGoal"]
            currentPrestige = len(dataPP["data"]["prestiges"]) - 1
            currentLevel = formatting_functions.extract_substring(dataPP['data']['formattedLevel'])

            embed = discord.Embed(title=f"Prestige Info for [{formatting_functions.int_to_roman(currentPrestige)}-{currentLevel}] {dataPP['data']['name']}", color=pit_functions.calcBracketColor(currentPrestige))
            embed.set_footer(text=footerDateGen())
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{dataPP['data']['uuid']}?format=webp")
            embed.add_field(name=f"XP Breakdown",
                            value=f"{formatting_functions.add_commas(currentXP)} XP / {formatting_functions.add_commas(prestigeGoalXP)} XP \n {int(100 * (currentXP/prestigeGoalXP))}% grinded",
                            inline=False)
            embed.add_field(name=f"Gold Breakdown",
                            value=f"{formatting_functions.add_commas(currentGoldGrinded)} G / {formatting_functions.add_commas(prestigeGoalGold)} G \n {int(100 * (currentGoldGrinded/prestigeGoalGold))}% grinded",
                            inline=False)
            await interaction.response.send_message(embed=embed)  # noqa

    @app_commands.command(name="xp-until", description="XP needed to reach a certain prestige and level")
    async def xp_until(self, interaction: discord.Interaction, player: str, prestige: int, level: int):
        """my command description
        Args:
            player (str): A Minecraft username
            prestige (int): A prestige
            level (int): A level
        """
        pass

        urlPP: str = f"https://pitpanda.rocks/api/players/{player}"
        dataPP = getInfo(urlPP)

        global globalPrestige
        global globalLevel
        global globalPlayer

        globalPrestige = prestige
        globalLevel = level
        globalPlayer = player

        if not dataPP["success"]:
            embedFail = discord.Embed(title="Player not found", color=discord.Color.red())

            await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa

        else:
            docData = dataPP["data"]["doc"]
            currentXP = docData["xp"]
            prestigeList = dataPP["data"]["prestiges"]

            goalXP = int(read_specific_line("../PitStats/useful_things/pitdata/xp_sums.txt", prestige - 1))
            goalXPFromFinalPrestige = pit_functions.calculateXPForLevel(prestige, level)
            goalXP += goalXPFromFinalPrestige

            neededXP = goalXP - currentXP
            currentPrestige = len(prestigeList) - 1

            embed = discord.Embed(title=f"XP until for {dataPP['data']['name']}", color=pit_functions.calcBracketColor(prestige))
            embed.set_footer(text=footerDateGen())

            embed.add_field(
                name=f"[{formatting_functions.int_to_roman(currentPrestige)}-{formatting_functions.extract_substring(dataPP['data']['formattedLevel'])}] ---> [{formatting_functions.int_to_roman(prestige)}-{level}]:",
                value=f"{formatting_functions.add_commas(neededXP)} XP required")
            embed.add_field(name=f"", value=f"This will take {formatting_functions.add_commas(int(neededXP / dataPP['data']['doc']['xpHourly']))} hours", inline=False)
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{dataPP['data']['uuid']}?format=webp")

            view = simpleView()

            await interaction.response.send_message(embed=embed, view=view)  # noqa
            await view.wait()

    @app_commands.command(name="kings_quest", description="Determines what level completing the King's Quest will grant")
    async def kingsQuest(self, interaction: discord.Interaction, player: str):
        """
        Args:
            player (str): A Minecraft username
        """
        pass

        urlPP: str = f"https://pitpanda.rocks/api/players/{player}"
        dataPP = getInfo(urlPP)

        if not dataPP["success"]:
            embed = discord.Embed(title="Player not found", color=discord.Color.red())

            await interaction.response.send_message(embed=embed, ephemeral=True)  # noqa

        else:
            currentPrestige = len(dataPP["data"]["prestiges"]) - 1
            currentPrestigeRomanNum = formatting_functions.int_to_roman(currentPrestige)
            playerName = dataPP['data']['name']

            if currentPrestige == 0:
                embed = discord.Embed(title=f"{playerName} can't do kings", color=discord.Color.red())

                await interaction.response.send_message(embed=embed) # noqa

            currentXP = dataPP["data"]["xpProgress"]["displayCurrent"]
            prestigeGoalXP = dataPP["data"]["xpProgress"]["displayGoal"]
            afterKingsXP = int(prestigeGoalXP / 3) + currentXP
            resultingLevel = pit_functions.xpToLevel(currentPrestige, afterKingsXP)

            if resultingLevel == 120:
                grantedXP = prestigeGoalXP - currentXP
            else:
                grantedXP = int(prestigeGoalXP / 3)

            embed = discord.Embed(title=f"Kings Quest for {playerName}", color=pit_functions.calcBracketColor(currentPrestige))
            embed.add_field(name=f"[{currentPrestigeRomanNum}-{formatting_functions.extract_substring(dataPP['data']['formattedLevel'])}] ---> [{currentPrestigeRomanNum}-{resultingLevel}]:", value=f"{formatting_functions.add_commas(grantedXP)} XP granted")
            embed.set_footer(text=footerDateGen())
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{dataPP['data']['uuid']}?format=webp")

            await interaction.response.send_message(embed=embed) # noqa


async def setup(client: commands.Bot) -> None:
    await client.add_cog(prestigeCalculations(client))