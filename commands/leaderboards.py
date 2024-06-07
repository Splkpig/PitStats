import asyncio
import discord
import json
from discord.ext import commands
from discord import app_commands
from useful_things.api_functions import getInfo
from useful_things import pit_functions
from useful_things import formatting_functions
from useful_things.discord_functions import footerDateGen
from useful_things import pit_functions
from useful_things.pit_functions import calcBracketColor

globalLeaderboardsList = ['arrowHits', 'arrowShots', 'assists', 'blocksBroken', 'blocksPlaced', 'bountiesClaimed',
                          'chatMessages', 'contracts', 'gold', 'renown', 'damageDealt', 'damageReceived',
                          'darkPants', 'deaths', 'diamondItemsPurchased', 'enderchestOpened', 'fishedAnything',
                          'fishedFish', 'fishingRodCasts', 'gapples', 'gheads', 'hiddenJewelsTriggered',
                          'ingotsPickedUp', 'jumpsIntoPit', 'kills', 'kingsQuests', 'launcherLaunches',
                          'lavaBuckets', 'leftClicks', 'lifetimeGold', 'lifetimeRenown', 'tierThrees',
                          'nightQuests', 'obsidianBroken', 'playtime', 'ragePotatoesEaten', 'sewerTreasures',
                          'soups', 'xp', 'vampireHealedHp', 'wheatFarmed']
globalLeaderboardsFormatedList = ["<:Arrow:1248117169653284926> Arrow Hits",
                                  "<:Bow:1248118009369854002> Arrows Shot",
                                  "<:woodensword:1248118747697250376> Assists",
                                  "<:diamondpickaxe:1248119046172446792> Blocks Broken",
                                  "<:obsidian:1248119285075935396> Blocks Placed",
                                  "<:goldleggings:1248119482388316202> Bounties Claimed",
                                  ":regional_indicator_t: Chat Messages",
                                  "<:enchantedbook:1248119930155569222> Contracts Completed",
                                  "<:goldingot:1247391882968043652> Current Gold",
                                  "<:emerald:1248128261272244305> Current Renown",
                                  "<:damagedealt:1248127865103585391> Damage Dealt",
                                  "<:damagereceived:1248128029427892316> Damage Received",
                                  "<:darkpants:1248121831475642440> Dark Pants Created",
                                  "<:ironchestplate:1247719811857907762> Deaths",
                                  "<:diamondchestplate:1248121536985169960> Diamond Items Purchased",
                                  "<:enderchest:1248124015483158598> Enderchests Opened",
                                  "<:tripwirehook:1248127264755810407> Fished Anything",
                                  "<:rawcod:1248126906851790848> Fished Fish",
                                  "<:fishingrod:1248127083549556736> Fishing Rod Casts",
                                  "<:goldenapple:1248127429084577913> Golden Apples Eaten",
                                  "<:goldenhead:1248127570373775433> Golden Heads",
                                  "<:sewerpants:1248126745756958782> Hidden Jewels Triggered",
                                  "<:goldingot:1247391882968043652> Ingots Gathered",
                                  "<:thepit:1248129525825409054> Jumps into Mid",
                                  "<:ironsword:1247392632129323080> Kills",
                                  "<:goldenhelmet:1248126543553892443> Kings Quest Completions",
                                  "<:slimeblock:1248126317745143828> Launcher Launches",
                                  "<:lavabucket:1248126173074952222> Lava Buckets Emptied",
                                  ":regional_indicator_l: Left Clicks",
                                  "<:goldingot:1247391882968043652> Lifetime Gold",
                                  "<:beacon:1248121257690402869> Lifetime Renown",
                                  "<:enchantingtable:1248125952865734676> Mystics Enchanted",
                                  "<:coal:1248125818744602636> Night Quests",
                                  "<:goldenpickaxe:1248125042550636574> Obsidian Broken",
                                  "<a:minecraftclock:1247400003786510479> Playtime",
                                  "<:bakedpotato:1248125222486409226> Rage Potatoes Eaten",
                                  "<:chest:1248125595678937099> Sewer Treasures",
                                  "<:mushroomstew:1248125413109141567> Soups Drank",
                                  "<:xpbottle:1245974825865056276> Total XP",
                                  "<:fermentedspidereye:1248124676706926642> Vampire Healing",
                                  "<:wheat:1248124503255420928> Wheat Farmed"]

embedPages = []
currentPage = -1


def leaderboardStuff():
    global globalLeaderboardsList
    global globalLeaderboardsFormatedList

    with open("../PitStats/tokens_and_keys/PP_API_KEY.json", 'r') as f:
        data = json.load(f)
        key = data['TOKEN']

    for i in range(0, len(globalLeaderboardsList) - 1):
        embedPage = discord.Embed(title=f"{globalLeaderboardsFormatedList[i]}", color=discord.Color.greyple())
        urlPP: str = f"https://pitpanda.rocks/api/leaderboard/{globalLeaderboardsList[i]}?page=0&pageSize=10&{key}"
        leaderboard = getInfo(urlPP)
        if not leaderboard["success"]:
            print(urlPP)
            try:
                print(leaderboard["error"])
            except KeyError:
                print("invalid url")
        else:
            leaderboard = leaderboard["leaderboard"]
            for j in range(0, 10):
                name = formatting_functions.extract_name(leaderboard[j]["name"])
                embedPage.add_field(name=f"#{j + 1}", value=f"{name}", inline=False)
        embedPages.append(embedPage)


class simpleView(discord.ui.View):
    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        global currentPage
        global embedPages

        if currentPage == -1:
            currentPage = 0

        if currentPage <= 0:
            embed = embedPages[currentPage]
            view = simpleView(timeout=None)

            await interaction.response.edit_message(embed=embed, view=view)  # noqa
        else:
            embed = embedPages[currentPage - 1]
            view = simpleView(timeout=None)
            currentPage -= 1

            await interaction.response.edit_message(embed=embed, view=view)  # noqa

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple)
    async def forward(self, interaction: discord.Interaction, button: discord.ui.Button):
        global currentPage
        global embedPages

        if currentPage <= 0:
            currentPage += 1

        if currentPage == len(embedPages) - 1:
            embed = embedPages[currentPage]
            view = simpleView(timeout=None)

            await interaction.response.edit_message(embed=embed, view=view)  # noqa
        else:
            embed = embedPages[currentPage]
            view = simpleView(timeout=None)
            currentPage += 1

            await interaction.response.edit_message(embed=embed, view=view)  # noqa


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

            global globalLeaderboardsList
            global globalLeaderboardsFormatedList

            leaderboardsList = globalLeaderboardsList
            leaderboardsFormatedList = globalLeaderboardsFormatedList

            playersRankings = []

            embed = discord.Embed(
                title=f"Leaderboard positions for [{formatting_functions.int_to_roman(currentPrestige)}{currentLevel}] {data['data']['name']}",
                color=calcBracketColor(0))

            await interaction.response.defer()  # noqa

            for i in range(0, len(leaderboardsList)):
                playersRankings.append(
                    {leaderboardsFormatedList[i]: pit_functions.getLeaderboardPosition(leaderboardsList[i], player)})
                print(f"finished {leaderboardsList[i]}")
                await asyncio.sleep(4)

            sorted_leaderboards = sorted(playersRankings, key=lambda x: list(x.values())[0], reverse=False)

            top25 = sorted_leaderboards[:25]

            for idx, leaderboard in enumerate(top25, start=1):
                leaderboard_name, ranking = leaderboard.popitem()
                if ranking == 999999:
                    embed.add_field(name=f"{leaderboard_name}:", value=f"#>2500", inline=False)
                else:
                    embed.add_field(name=f"{leaderboard_name}:", value=f"#{ranking}", inline=False)

            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{data['data']['uuid']}?format=webp")
            embed.set_footer(text=footerDateGen())

            await interaction.followup.send(embed=embed)  # noqa

    @app_commands.command(name="leaderboards", description="Shows top 10 leaderboard positions for all leaderboards")
    async def leaderboards(self, interaction: discord.Interaction):
        await interaction.response.defer() # noqa

        leaderboardStuff()
        embed = discord.Embed(title="Pit Leaderboards", color=discord.Color.greyple())
        embed.add_field(name="View the different top 10 players for the pit leaderboards", value="")

        view = simpleView(timeout=None)

        await interaction.followup.send(embed=embed, view=view)  # noqa


async def setup(client: commands.Bot) -> None:
    await client.add_cog(leaderboards(client))