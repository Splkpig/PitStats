import discord
from discord import app_commands
from discord.ext import commands

from useful_things import formatting_functions
from useful_things import pit_functions
from useful_things.api_functions import getInfo
from useful_things.discord_functions import footerDateGen
from useful_things.pit_functions import calcBracketColor

globalLeaderboardsList = ["kills", "assists", "damageDealt", "damageReceived", "deaths", "xp", "gold", "lifetimeGold", "playtime", "contracts", "gapples", "gheads", "lavaBuckets", "soups", "tierThrees", "darkPants", "leftClicks", "chatMessages", "wheatFarmed", "fishedAnything", "blocksBroken", "blocksPlaced", "kingsQuests", "sewerTreasures", "nightQuests", "renown", "lifetimeRenown", "arrowShots", "arrowHits", "jumpsIntoPit", "launcherLaunches", "enderchestOpened", "diamondItemsPurchased", "fishedFish", "hiddenJewelsTriggered", "fishingRodCasts", "bountiesClaimed", "ragePotatoesEaten", "obsidianBroken", "ingotsPickedUp", "vampireHealedHp"]
globalLeaderboardsFormatedList = ["<:ironsword:1247392632129323080> Kills", "<:woodensword:1248118747697250376> Assists", "<:damagedealt:1248127865103585391> Damage Dealt", "<:damagereceived:1248128029427892316> Damage Received", "<:ironchestplate:1247719811857907762> Deaths", "<:xpbottle:1245974825865056276> Total XP", "<:goldingot:1247391882968043652> Current Gold", "<:goldingot:1247391882968043652> Lifetime Gold", "<a:minecraftclock:1247400003786510479> Playtime", "<:enchantedbook:1248119930155569222> Contracts Completed", "<:goldenapple:1248127429084577913> Golden Apples Eaten", "<:goldenhead:1248127570373775433> Golden Heads", "<:lavabucket:1248126173074952222> Lava Buckets Emptied", "<:mushroomstew:1248125413109141567> Soups Drank", "<:enchantingtable:1248125952865734676> Mystics Enchanted", "<:darkpants:1248121831475642440> Dark Pants Created", ":regional_indicator_l: Left Clicks", ":regional_indicator_t: Chat Messages", "<:wheat:1248124503255420928> Wheat Farmed", "<:tripwirehook:1248127264755810407> Fished Anything", "<:diamondpickaxe:1248119046172446792> Blocks Broken", "<:obsidian:1248119285075935396> Blocks Placed", "<:goldenhelmet:1248126543553892443> Kings Quest Completions", "<:chest:1248125595678937099> Sewer Treasures", "<:coal:1248125818744602636> Night Quests", "<:emerald:1248128261272244305> Current Renown", "<:beacon:1248121257690402869> Lifetime Renown", "<:Bow:1248118009369854002> Arrows Shot", "<:Arrow:1248117169653284926> Arrow Hits", "<:thepit:1248129525825409054> Jumps into Mid", "<:slimeblock:1248126317745143828> Launcher Launches", "<:enderchest:1248124015483158598> Enderchests Opened", "<:diamondchestplate:1248121536985169960> Diamond Items Purchased", "<:rawcod:1248126906851790848> Fished Fish", "<:sewerpants:1248126745756958782> Hidden Jewels Triggered", "<:fishingrod:1248127083549556736> Fishing Rod Casts", "<:goldleggings:1248119482388316202> Bounties Claimed", "<:bakedpotato:1248125222486409226> Rage Potatoes Eaten", "<:goldenpickaxe:1248125042550636574> Obsidian Broken", "<:goldingot:1247391882968043652> Ingots Gathered", "<:fermentedspidereye:1248124676706926642> Vampire Healing"]
globalLeaderboardsNameList = ["Kills", "Assists", "Damage Dealt", "Damage Received", "Deaths", "Total XP", "Current Gold", "Lifetime Gold", "Playtime", "Contracts Completed", "Golden Apples Eaten", "Golden Heads", "Lava Buckets Emptied", "Soups Drank", "Mystics Enchanted", "Dark Pants Created", "Left Clicks", "Chat Messages", "Wheat Farmed", "Fished Anything", "Blocks Broken", "Blocks Placed", "Kings Quest Completions", "Sewer Treasures", "Night Quests", "Current Renown", "Lifetime Renown", "Arrows Shot", "Arrow Hits", "Jumps into Mid", "Launcher Launches", "Enderchests Opened", "Diamond Items Purchased", "Fished Fish", "Hidden Jewels Triggered", "Fishing Rod Casts", "Bounties Claimed", "Rage Potatoes Eaten", "Obsidian Broken", "Ingots Gathered", "Vampire Healing"]

currentPage = 0
globalLeaderboard = ''


class simpleView(discord.ui.View):
    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        global currentPage
        global globalLeaderboard

        if currentPage == 0:
            embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[globalLeaderboardsList.index(globalLeaderboard)]} Page: {currentPage + 1}", color=discord.Color.greyple())
            embed = formatting_functions.leaderboardEmbed(pit_functions.getLeaderboardData(globalLeaderboard, 10, currentPage), embed, currentPage)
            view = simpleView(timeout=None)
            embed.set_footer(text=footerDateGen())

            await interaction.response.edit_message(embed=embed, view=view) # noqa
        else:
            embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[globalLeaderboardsList.index(globalLeaderboard)]} Page: {currentPage}", color=discord.Color.greyple())
            embed = formatting_functions.leaderboardEmbed(pit_functions.getLeaderboardData(globalLeaderboard, 10, currentPage - 1), embed, currentPage - 1)
            currentPage -= 1
            view = simpleView(timeout=None)
            embed.set_footer(text=footerDateGen())

            await interaction.response.edit_message(embed=embed, view=view) # noqa

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple)
    async def forward(self, interaction: discord.Interaction, button: discord.ui.Button):
        global currentPage

        embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[globalLeaderboardsList.index(globalLeaderboard)]} Page: {currentPage + 2}", color=discord.Color.greyple())
        embed = formatting_functions.leaderboardEmbed(pit_functions.getLeaderboardData(globalLeaderboard, 10, currentPage + 1), embed, currentPage + 1)
        currentPage += 1
        view = simpleView(timeout=None)
        embed.set_footer(text=footerDateGen())

        await interaction.response.edit_message(embed=embed, view=view) # noqa


currentPageAll = 0


class simpleViewAll(discord.ui.View):
    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        global currentPageAll
        global globalLeaderboard

        if currentPageAll == 0:
            embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[currentPageAll]}", color=discord.Color.greyple())
            embed = formatting_functions.leaderboardEmbedAll(pit_functions.getLeaderboardDataAll(globalLeaderboardsList[currentPageAll], 10), embed)
            view = simpleViewAll(timeout=None)

        else:
            embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[currentPageAll - 1]}", color=discord.Color.greyple())
            embed = formatting_functions.leaderboardEmbedAll(pit_functions.getLeaderboardDataAll(globalLeaderboardsList[currentPageAll - 1], 10,), embed)
            currentPageAll -= 1
            view = simpleViewAll(timeout=None)

        embed.set_footer(text=f"Current Page: {currentPageAll + 1} / {len(globalLeaderboardsList)}")
        await interaction.response.edit_message(embed=embed, view=view) # noqa

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple)
    async def forward(self, interaction: discord.Interaction, button: discord.ui.Button):
        global currentPageAll

        if currentPageAll == len(globalLeaderboardsList) - 1:
            embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[currentPageAll]}", color=discord.Color.greyple())
            embed = formatting_functions.leaderboardEmbedAll(pit_functions.getLeaderboardDataAll(globalLeaderboardsList[currentPageAll], 10), embed)
            view = simpleViewAll(timeout=None)

        else:
            embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[currentPageAll + 1]}", color=discord.Color.greyple())
            embed = formatting_functions.leaderboardEmbedAll(pit_functions.getLeaderboardDataAll(globalLeaderboardsList[currentPageAll + 1], 10), embed)
            currentPageAll += 1
            view = simpleViewAll(timeout=None)

        embed.set_footer(text=f"Current Page: {currentPageAll + 1} / {len(globalLeaderboardsList)}")
        await interaction.response.edit_message(embed=embed, view=view) # noqa


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

            uuid = data["data"]["uuid"]
            leaderboardsData = getInfo(f"https://pitpanda.rocks/api/position/{uuid}")

            global globalLeaderboardsFormatedList
            leaderboardsFormatedList = globalLeaderboardsFormatedList
            playersRankings = []

            embed = discord.Embed(
                title=f"Leaderboard positions for [{formatting_functions.int_to_roman(currentPrestige)}{currentLevel}] {data['data']['name']}",
                color=calcBracketColor(currentPrestige))

            await interaction.response.defer()  # noqa

            rankingsFormatted = formatting_functions.formatRankingsData(leaderboardsData["rankings"])

            for i in range(0, len(rankingsFormatted)):
                playersRankings.append({leaderboardsFormatedList[i]: rankingsFormatted[i]})
                # print(f"finished {leaderboardsFormatedList[i][leaderboardsFormatedList[i].index(' ') + 1:]}")

            sorted_leaderboards = sorted(playersRankings, key=lambda x: list(x.values())[0], reverse=False)
            top25 = sorted_leaderboards[:25]

            for idx, leaderboard in enumerate(top25, start=1):
                leaderboard_name, ranking = leaderboard.popitem()
                if ranking == 999999:
                    embed.add_field(name=f"{leaderboard_name}:", value="N/A", inline=False)
                elif ranking == 1:
                    embed.add_field(name=f"{leaderboard_name}:", value=f":first_place: #{ranking}", inline=False)
                elif ranking <= 10:
                    embed.add_field(name=f"{leaderboard_name}:", value=f":second_place: #{ranking}", inline=False)
                elif ranking <= 100:
                    embed.add_field(name=f"{leaderboard_name}:", value=f":third_place: #{ranking}", inline=False)
                else:
                    embed.add_field(name=f"{leaderboard_name}:", value=f"#{ranking}", inline=False)

            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{data['data']['uuid']}?format=webp")
            embed.set_footer(text=footerDateGen())

            await interaction.followup.send(embed=embed)  # noqa

    @app_commands.command(name="leaderboard", description="Shows a leaderboard")
    @app_commands.choices(leaderboard=[app_commands.Choice(name='Total XP', value="xp"), app_commands.Choice(name='Current Gold', value="gold"), app_commands.Choice(name='Lifetime Gold', value="lifetimeGold"), app_commands.Choice(name='Playtime', value="playtime"), app_commands.Choice(name='Contracts Completed', value="contracts"), app_commands.Choice(name='Chat Messages', value="chatMessages"), app_commands.Choice(name='Wheat Farmed', value="wheatFarmed"), app_commands.Choice(name='Fished Anything', value="fishedAnything"), app_commands.Choice(name='Blocks Broken', value="blocksBroken"), app_commands.Choice(name='Blocks Placed', value="blocksPlaced"), app_commands.Choice(name='Kings Quest Completions', value="kingsQuests"), app_commands.Choice(name='Sewer Treasures', value="sewerTreasures"), app_commands.Choice(name='Night Quests', value="nightQuests"), app_commands.Choice(name='Current Renown', value="renown"), app_commands.Choice(name='Lifetime Renown', value="lifetimeRenown"), app_commands.Choice(name='Jumps into Mid', value="jumpsIntoPit"), app_commands.Choice(name='Launcher Launches', value="launcherLaunches"), app_commands.Choice(name='Enderchests Opened', value="enderchestOpened"), app_commands.Choice(name='Diamond Items Purchased', value="diamondItemsPurchased"), app_commands.Choice(name='Fished Fish', value="fishedFish"), app_commands.Choice(name='Hidden Jewels Triggered', value="hiddenJewelsTriggered"), app_commands.Choice(name='Fishing Rod Casts', value="fishingRodCasts"), app_commands.Choice(name='Dark Pants Created', value="darkPants"), app_commands.Choice(name='Obsidian Broken', value="obsidianBroken"), app_commands.Choice(name='Ingots Gathered', value="ingotsPickedUp")])
    async def leaderboard(self, interaction: discord.Interaction, leaderboard: str):
        global globalLeaderboard
        global currentPage
        currentPage = 0
        globalLeaderboard = leaderboard

        await interaction.response.defer() # noqa

        embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[globalLeaderboardsList.index(leaderboard)]} Page: {currentPage + 1}", color=discord.Color.greyple())
        i = 1

        for player in pit_functions.getLeaderboardData(leaderboard, 10, 0):
            embed.add_field(name=f"#{i}:", value=f"{player}", inline=False)
            i += 1

        embed.set_footer(text=footerDateGen())

        view = simpleView(timeout=None)
        await interaction.followup.send(embed=embed, view=view)

    @app_commands.command(name="leaderboard-combat", description="Shows a combat related leaderboard")
    @app_commands.choices(leaderboard=[app_commands.Choice(name='Kills', value="kills"), app_commands.Choice(name='Assists', value="assists"), app_commands.Choice(name='Damage Dealt', value="damageDealt"), app_commands.Choice(name='Damage Received', value="damageReceived"), app_commands.Choice(name='Deaths', value="deaths"), app_commands.Choice(name='Golden Apples Eaten', value="gapples"), app_commands.Choice(name='Golden Heads', value="gheads"), app_commands.Choice(name='Lava Buckets Emptied', value="lavaBuckets"), app_commands.Choice(name='Soups Drank', value="soups"), app_commands.Choice(name='Mystics Enchanted', value="tierThrees"), app_commands.Choice(name='Left Clicks', value="leftClicks"), app_commands.Choice(name='Arrows Shot', value="arrowShots"), app_commands.Choice(name='Arrow Hits', value="arrowHits"), app_commands.Choice(name='Bounties Claimed', value="bountiesClaimed"), app_commands.Choice(name='Rage Potatoes Eaten', value="ragePotatoesEaten"), app_commands.Choice(name='Vampire Healing', value="vampireHealedHp")])
    async def leaderboardCombat(self, interaction: discord.Interaction, leaderboard: str):
        global globalLeaderboard
        global currentPage
        currentPage = 0
        globalLeaderboard = leaderboard

        await interaction.response.defer() # noqa

        embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[globalLeaderboardsList.index(leaderboard)]} Page: {currentPage + 1}", color=discord.Color.greyple())
        i = 1

        for player in pit_functions.getLeaderboardData(leaderboard, 10, 0):
            embed.add_field(name=f"#{i}:", value=f"{player}", inline=False)
            i += 1

        embed.set_footer(text=footerDateGen())

        view = simpleView(timeout=None)
        await interaction.followup.send(embed=embed, view=view)

    @app_commands.command(name="leaderboards", description="Shows the top 10 of every leaderboard")
    async def leaderboardsAll(self, interaction: discord.Interaction):
        global currentPageAll
        currentPageAll = 0

        await interaction.response.defer() # noqa

        embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[currentPageAll]}", color=discord.Color.greyple())
        i = 1

        for player in pit_functions.getLeaderboardData(globalLeaderboardsList[currentPageAll], 10, 0):
            embed.add_field(name=f"#{i}:", value=f"{player}", inline=False)
            i += 1

        embed.set_footer(text=f"Current Page: {currentPageAll + 1} / {len(globalLeaderboardsList)}")

        view = simpleViewAll(timeout=None)
        await interaction.followup.send(embed=embed, view=view)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(leaderboards(client))
