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
            print("your mom lol")

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
            embed.add_field(name="", value=f"Prestige & Level: [{formatting_functions.int_to_roman(prestige)}-{level}]", inline=False)
            embed.add_field(name="", value=f"<:8983xpbottle:1245974825865056276> XP Grinded: {formatting_functions.add_commas(xp)}", inline=False)
            embed.add_field(name="", value=f"Gold Grinded: {formatting_functions.add_commas(gold)}", inline=False)
            embed.add_field(name="", value=f"Kills: {formatting_functions.add_commas(kills)}", inline=False)
            embed.add_field(name="", value=f"Deaths: {formatting_functions.add_commas(deaths)}", inline=False)
            embed.add_field(name="", value=f"KDR: {kdr}", inline=False)
            embed.add_field(name="", value=f"Time Played: {timeplayed}", inline=False)
            embed.set_footer(text=footerDateGen())
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{data['data']['uuid']}?format=webp")

            await interaction.response.send_message(embed=embed) # noqa

    @app_commands.command(name='genesis', description='Shows a player\'s genesis progress')
    async def genesis(self, interaction: discord.Interaction, player: str):
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
            points = data["data"]["doc"]["genesisPoints"]
            allegiance = data["data"]["doc"]["allegiance"]
            tier = pit_functions.calculateFactionTier(points)

            demonRewards = ["Deal +0.5♥︎ damage to players in the Angel faction.", "Unlock the Demon spawn.", "The Mystic Well costs 1/3 of the price.", "Deal +0.5♥︎ damage to players wearing diamond armor.", "Accumulate +50% gold on your bounties. Earn +1 renown when earning renown from events.", "Earn Armageddon Boots.", "Permanently gain +0.2g from kills. Can be claimed up to 15 times."]
            angelRewards = ["Deal +0.5♥︎ damage to players in the Demon faction.", "Unlock the Angel spawn.", "Diamond items cost 1/3 of the price.", "	Deal +0.25♥︎ damage to players wearing leather armor.", "Accumulate +50% gold on your bounties. Earn +1 renown when earning renown from events.", "Earn Archangel Chestplate.", "Permanently gain +1% XP from kills. Can be claimed up to 15 times."]

            if allegiance == "DEMON":
                embed = discord.Embed(title=f"Genesis points for [{formatting_functions.int_to_roman(prestige)}-{level}] {data['data']['name']}", color=calcBracketColor(48))
                embed.add_field(name="", value=f"Allegiance: {allegiance}", inline=False)
                embed.add_field(name="", value=f"Points: {points}", inline=False)
                embed.add_field(name="", value=f"Tier: {tier}", inline=False)

                for i in range(0, tier):
                    embed.add_field(name="", value=f":white_check_mark: {demonRewards[i]}", inline=False)

                for i in range(tier, 7):
                    embed.add_field(name="", value=f":x: {demonRewards[i]}", inline=False)

            elif allegiance == "ANGEL":
                embed = discord.Embed(title=f"Genesis points for [{formatting_functions.int_to_roman(prestige)}-{level}] {data['data']['name']}", color=calcBracketColor(35))
                embed.add_field(name="", value=f"Allegiance: {allegiance}", inline=False)
                embed.add_field(name="", value=f"Points: {points}", inline=False)
                embed.add_field(name="", value=f"Tier: {tier}", inline=False)

                for i in range(0, tier):
                    embed.add_field(name="", value=f":white_check_mark: {angelRewards[i]}", inline=False)

                for i in range(tier, 7):
                    embed.add_field(name="", value=f":x: {angelRewards[i]}", inline=False)
            else:
                embed = discord.Embed(title="No Faction selected", color=discord.Color.red())

            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{data['data']['uuid']}?format=webp")

            await interaction.response.send_message(embed=embed) # noqa


async def setup(client: commands.Bot) -> None:
    await client.add_cog(compare(client))
