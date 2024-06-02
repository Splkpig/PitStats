import discord
from discord.ext import commands
from discord import app_commands
from useful_things.api_functions import getInfo
from useful_things import pit_functions
from useful_things import formatting_functions
from useful_things.discord_functions import footerDateGen
from useful_things.pit_functions import calcBracketColor


class compare(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name='compare', description='Compares the stats of two players')
    async def compare(self, interaction: discord.Interaction, player1: str, player2: str):
        """my command description
        Args:
            player1 (str): A Minecraft username
            player2 (str): A Minecraft username
        """
        pass

        urlPP: str = f"https://pitpanda.rocks/api/players/{player1}"
        player1Data = getInfo(urlPP)
        urlPP: str = f"https://pitpanda.rocks/api/players/{player2}"
        player2Data = getInfo(urlPP)

        if not (player1Data["success"] and player2Data["success"]):
            embedFail = discord.Embed(title="Player not found", color=discord.Color.red())

            await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa

        else:
            prestige = len(player1Data["data"]["prestiges"]) - 1
            level = pit_functions.xpToLevel(prestige, int(player1Data["data"]["xpProgress"]["displayCurrent"]))
            xp = player1Data["data"]["doc"]["xp"]
            gold = player1Data["data"]["doc"]["lifetimeGold"]
            kills = player1Data["data"]["doc"]["kills"]
            deaths = player1Data["data"]["doc"]["deaths"]
            kdr = str(player1Data["data"]["doc"]["kdr"])
            kdr = kdr[:kdr.index(".") + 3]
            timeplayed = player1Data["data"]["doc"]["playtime"]

            player1DataList = [prestige, level, xp, gold, kills, deaths, kdr, timeplayed]

            prestige = len(player2Data["data"]["prestiges"]) - 1
            level = pit_functions.xpToLevel(prestige, int(player2Data["data"]["xpProgress"]["displayCurrent"]))
            xp = player2Data["data"]["doc"]["xp"]
            gold = player2Data["data"]["doc"]["lifetimeGold"]
            kills = player2Data["data"]["doc"]["kills"]
            deaths = player2Data["data"]["doc"]["deaths"]
            kdr = str(player2Data["data"]["doc"]["kdr"])
            kdr = kdr[:kdr.index(".") + 3]
            timeplayed = player2Data["data"]["doc"]["playtime"]

            player2DataList = [prestige, level, xp, gold, kills, deaths, kdr, timeplayed]

            embed = discord.Embed(title=f"[{formatting_functions.int_to_roman(player1DataList[0])}-{player1DataList[1]}] {player1Data['data']['name']} vs [{formatting_functions.int_to_roman(player2DataList[0])}-{player2DataList[1]}] {player2Data['data']['name']}", color=calcBracketColor(max(player1DataList[0], player2DataList[0])))

            signs = []

            for i in range(len(player1DataList)):
                if player1DataList[i] < player2DataList[i]:
                    signs.append('<')
                elif player1DataList[i] > player2DataList[i]:
                    signs.append('>')
                else:
                    signs.append('=')

            embed.add_field(name="Prestige & Level:", value=f"[{formatting_functions.int_to_roman(player1DataList[0])}-{player1DataList[1]}]    {signs[0]}    [{formatting_functions.int_to_roman(player2DataList[0])}-{player2DataList[1]}]", inline=False)
            embed.add_field(name=" XP Grinded:", value=f"{formatting_functions.add_commas(player1DataList[2])} XP {signs[2]} {formatting_functions.add_commas(player2DataList[2])} XP", inline=False)
            embed.add_field(name="Gold Grinded:", value=f"{formatting_functions.add_commas(player1DataList[3])} G {signs[3]} {formatting_functions.add_commas(player2DataList[3])} G", inline=False)
            embed.add_field(name="Kills:", value=f"{formatting_functions.add_commas(player1DataList[4])} {signs[4]} {formatting_functions.add_commas(player2DataList[4])}", inline=False)
            embed.add_field(name="Deaths:", value=f"{formatting_functions.add_commas(player1DataList[5])} {signs[5]} {formatting_functions.add_commas(player2DataList[5])}", inline=False)
            embed.add_field(name="KDR:", value=f"{player1DataList[6]} {signs[6]} {player2DataList[6]}", inline=False)
            embed.add_field(name="Time Played:", value=f"{formatting_functions.format_playtime(int(player1DataList[7]))} {signs[7]} {formatting_functions.format_playtime(int(player2DataList[7]))}", inline=False)

            if player1DataList[0] > player2DataList[0]:
                embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{player1Data['data']['uuid']}?format=webp")
            else:
                embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{player2Data['data']['uuid']}?format=webp")

            await interaction.response.send_message(embed=embed) # noqa

    @app_commands.command(name="overview", description='Shows an overview of a player\'s stats')
    async def overview(self, interaction: discord.Interaction, player: str):
        """
        Args:
            player (str): A Minecraft username
        """
        pass

        urlPP: str = f"https://pitpanda.rocks/api/players/{player}"
        data = getInfo(urlPP)

        if not data["success"]:
            embedFail = discord.Embed(title="Player not found", color=discord.Color.red())

            await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa

        else:
            prestige = len(data["data"]["prestiges"]) - 1
            level = pit_functions.xpToLevel(prestige, int(data["data"]["xpProgress"]["displayCurrent"]))
            xp = data["data"]["doc"]["xp"]
            gold = data["data"]["doc"]["lifetimeGold"]
            kills = data["data"]["doc"]["kills"]
            deaths = data["data"]["doc"]["deaths"]
            kdr = str(data["data"]["doc"]["kdr"])
            kdr = kdr[:kdr.index(".") + 3]
            timeplayed = data["data"]["doc"]["playtime"]
            timeplayed = formatting_functions.format_playtime(int(timeplayed))

            embed = discord.Embed(title=f"Player Stats for [{formatting_functions.int_to_roman(prestige)}-{level}] {data['data']['name']}", color=calcBracketColor(int(prestige)))
            embed.add_field(name="Prestige & Level:", value=f"[{formatting_functions.int_to_roman(prestige)}-{level}]", inline=False)
            embed.add_field(name="XP Grinded:", value=f"{formatting_functions.add_commas(xp)} XP", inline=False)
            embed.add_field(name="Gold Grinded:", value=f"{formatting_functions.add_commas(gold)} G", inline=False)
            embed.add_field(name="Kills:", value=f"{formatting_functions.add_commas(kills)}", inline=False)
            embed.add_field(name="Deaths:", value=f"{formatting_functions.add_commas(deaths)}", inline=False)
            embed.add_field(name="KDR:", value=f"{kdr}", inline=False)
            embed.add_field(name="Time Played", value=f"{timeplayed}", inline=False)
            embed.set_footer(text=footerDateGen())
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{data['data']['uuid']}?format=webp")

            await interaction.response.send_message(embed=embed) # noqa


async def setup(client: commands.Bot) -> None:
    await client.add_cog(compare(client))
