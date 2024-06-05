import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from useful_things.api_functions import getInfo
from useful_things import pit_functions
from useful_things import formatting_functions
from useful_things.discord_functions import footerDateGen
from useful_things import pit_functions
from useful_things.pit_functions import calcBracketColor


class leaderboards(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="leaderboard-positions", description="Shows a player's leaderboard positions")
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
            currentPrestige = len(data["data"].get("prestiges", [0])) - 1

            xpProgress = data["data"].get("xpProgress", {})
            display_current_xp = int(xpProgress.get("displayCurrent", 0))
            currentLevel = pit_functions.xpToLevel(currentPrestige, display_current_xp)

            leaderboardsList = ['arrowHits', 'arrowShots', 'assists', 'blocksBroken', 'blocksPlaced', 'bountiesClaimed', 'chatMessages', 'contracts', 'gold', 'renown', 'damageDealt', 'damageReceived', 'darkPants', 'deaths', 'diamondItemsPurchased', 'enderchestOpened', 'fishedAnything', 'fishedFish', 'fishingRodCasts', 'gapples', 'gheads', 'hiddenJewelsTriggered', 'ingotsPickedUp', 'jumpsIntoPit', 'kills', 'kingsQuests', 'launcherLaunches', 'lavaBuckets', 'leftClicks', 'lifetimeGold', 'lifetimeRenown', 'tierThrees', 'nightQuests', 'obsidianBroken', 'playtime', 'ragePotatoesEaten', 'sewerTreasures', 'soups', 'xp', 'vampireHealedHp', 'wheatFarmed']

            playersRankings = []

            embed = discord.Embed(title=f"Leaderboard positions for {formatting_functions.int_to_roman(currentPrestige)}{currentLevel}] {data['data']['name']}", color=calcBracketColor(0))

            await interaction.response.defer() # noqa

            for leaderboard in leaderboardsList:
                playersRankings.append({leaderboard: pit_functions.getLeaderboardPosition(leaderboard, player)})
                await asyncio.sleep(3)

            sorted_leaderboards = sorted(playersRankings, key=lambda x: list(x.values())[0], reverse=False)
            top25 = sorted_leaderboards[:25]

            for idx, leaderboard in enumerate(top25, start=1):
                leaderboard_name, ranking = leaderboard.popitem()
                embed.add_field(name=f"{leaderboard_name}:", value=f"#{ranking}", inline=False)

            await interaction.followup.send(embed=embed) # noqa


async def setup(client: commands.Bot) -> None:
    await client.add_cog(leaderboards(client))