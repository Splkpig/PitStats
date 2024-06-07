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
            leaderboardsFormatedList = ["<:Arrow:1248117169653284926> Arrow Hits", "<:Bow:1248118009369854002> Arrows Shot", "<:woodensword:1248118747697250376> Assists", "<:diamondpickaxe:1248119046172446792> Blocks Broken", "<:obsidian:1248119285075935396> Blocks Placed", "<:goldleggings:1248119482388316202> Bounties Claimed", ":regional_indicator_t: Chat Messages", "<:enchantedbook:1248119930155569222> Contracts Completed", "<:goldingot:1247391882968043652> Current Gold", "<:emerald:1248128261272244305> Current Renown", "<:damagedealt:1248127865103585391> Damage Dealt", "<:damagereceived:1248128029427892316> Damage Received", "<:darkpants:1248121831475642440> Dark Pants Created", "<:ironchestplate:1247719811857907762> Deaths", "<:diamondchestplate:1248121536985169960> Diamond Items Purchased", "<:enderchest:1248124015483158598> Enderchests Opened", "<:tripwirehook:1248127264755810407> Fished Anything", "<:rawcod:1248126906851790848> Fished Fish", "<:fishingrod:1248127083549556736> Fishing Rod Casts", "<:goldenapple:1248127429084577913> Golden Apples Eaten", "<:goldenhead:1248127570373775433> Golden Heads", "<:sewerpants:1248126745756958782> Hidden Jewels Triggered", "<:goldingot:1247391882968043652> Ingots Gathered", "<:thepit:1248129525825409054> Jumps into Mid", "<:ironsword:1247392632129323080> Kills", "<:goldenhelmet:1248126543553892443> Kings Quest Completions", "<:slimeblock:1248126317745143828> Launcher Launches", "<:lavabucket:1248126173074952222> Lava Buckets Emptied", ":regional_indicator_l: Left Clicks", "<:goldingot:1247391882968043652> Lifetime Gold", "<:beacon:1248121257690402869> Lifetime Renown", "<:enchantingtable:1248125952865734676> Mystics Enchanted", "<:coal:1248125818744602636> Night Quests", "<:goldenpickaxe:1248125042550636574> Obsidian Broken", "<a:minecraftclock:1247400003786510479> Playtime", "<:bakedpotato:1248125222486409226> Rage Potatoes Eaten", "<:chest:1248125595678937099> Sewer Treasures", "<:mushroomstew:1248125413109141567> Soups Drank", "<:xpbottle:1245974825865056276> Total XP", "<:fermentedspidereye:1248124676706926642> Vampire Healing", "<:wheat:1248124503255420928> Wheat Farmed"]

            playersRankings = []

            embed = discord.Embed(title=f"Leaderboard positions for [{formatting_functions.int_to_roman(currentPrestige)}{currentLevel}] {data['data']['name']}", color=calcBracketColor(0))

            await interaction.response.defer() # noqa

            for i in range(0, 24):
                playersRankings.append({leaderboardsFormatedList[i]: pit_functions.getLeaderboardPosition(leaderboardsList[i], player)})
                # print(f"finished {leaderboardsList[i]}")
                await asyncio.sleep(4)

            sorted_leaderboards = sorted(playersRankings, key=lambda x: list(x.values())[0], reverse=False)

            # for idx, leaderboard in enumerate(sorted_leaderboards, start=1):
            #     leaderboard_name, ranking = leaderboard.popitem()
            #     print(f"{leaderboard_name}: #{ranking}")

            top25 = sorted_leaderboards[:25]

            for idx, leaderboard in enumerate(top25, start=1):
                leaderboard_name, ranking = leaderboard.popitem()
                if ranking == 999999:
                    embed.add_field(name=f"{leaderboard_name}:", value=f"#>2500", inline=False)
                else:
                    embed.add_field(name=f"{leaderboard_name}:", value=f"#{ranking}", inline=False)

            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{data['data']['uuid']}?format=webp")
            embed.add_field(text=footerDateGen())

            await interaction.followup.send(embed=embed) # noqa


async def setup(client: commands.Bot) -> None:
    await client.add_cog(leaderboards(client))