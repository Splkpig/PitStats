import discord
from discord import app_commands
from discord.ext import commands
from useful_things import pit_functions
from useful_things import formatting_functions
from useful_things import discord_functions
from useful_things.api_functions import getInfo
from collections import Counter

keys = ["xp_boost", "cash_boost", "melee_damage", "bow_damage", "damage_reduction", "build_battler", "el_gato", "golden_heads", "fishing_rod", "lava_bucket", "strength_chaining", "free_blocks", "endless_quiver", "safety_first", "barbarian", "trickle_down", "lucky_diamond", "spammer", "bounty_hunter", "streaker", "assistant_streaker", "coop_cat", "conglomerate", "gladiator", "vampire", "recon", "overheal", "rambo", "olympus", "dirty", "first_strike", "soup", "marathon", "thick", "kung_fu_knowledge", "second_gapple", "extra_xp", "res_and_regen", "arquebusier", "khanate", "leech", "tough_skin", "fight_or_flight", "pungent", "speed_two", "withercraft", "feast", "counter_strike", "gold_nanofactory", "tactical_retreat", "glass_sword", "assured_strike", "shield_aura", "ice_cube", "super_streaker", "gold_stack", "xp_stack", "monster", "sponge_steve", "apostle", "overdrive", "beastmode", "hermit", "highlander", "grand_finale", "to_the_moon", "uberstreak"]
names = ["XP Boost", "Gold Boost", "Melee Damage", "Bow Damage", "Damage Reduction", "Build Battler", "El Gato", "Golden Heads", "Fishing Rod", "Lava Bucket", "Strength-Chaining", "Mineman", "Bonk!", "Safety First", "Barbarian", "Trickle Down", "Lucky Diamond", "Spammer", "Bounty Hunter", "Streaker", "Assistant (to the) Streaker", "Co-op Cat", "Conglomerate", "Gladiator", "Vampire", "Recon", "Overheal", "Rambo", "Olympus", "Dirty", "First Strike", "Soup", "Marathon", "Thick", "Kung Fu Knowledge", "Second Gapple", "Explicious", "R&R", "Arquebusier", "Khanate", "Leech", "Tough Skin", "Fight or Flight", "Pungent", "Hero's Haste", "Rush", "Feast", "Counter-Strike", "Gold Nano-Factory", "Tactical Retreat", "Glass Pickaxe", "Assured Strike", "Aura of Protection", "Ice Cube", "Super Streaker", "Gold Stack", "XP Stack", "Monster", "Spongesteve", "Apostle to RNGesus", "Overdrive", "Beastmode", "Hermit", "Highlander", "Magnum Opus", "To the Moon", "Uberstreak"]
namesFormated = ["<:xpboost:1251035226008850473> XP Boost", "<:goldboost:1251035984293007440> Gold Boost", "<:damagedealt:1248127865103585391> Melee Damage", "<:bowdamage:1251036153864388659> Bow Damage", "<:damagereceived:1248128029427892316> Damage Reduction", "<:buildbattler:1251036278070186005> Build Battler", "<:elgato:1251036569582829632> El Gato", "<:goldenhead:1248127570373775433> Golden Heads", "<:fishingrod:1248127083549556736> Fishing Rod", "<:lavabucket:1248126173074952222> Lava Bucket", "<:strengthchaining:1251037721724588162> Strength-Chaining", "<:diamondpickaxe:1248119046172446792> Mineman", "<:bonk:1251037940835029083> Bonk!", "<:safetyfirst:1251038090185674833> Safety First", "<:barbarian:1251038226597281793> Barbarian", "<:trickledown:1251038830241517650> Trickle Down", "<:luckydiamond:1251038963079188530> Lucky Diamond", "<:spammer:1251039108390850630> Spammer", "<:goldleggings:1248119482388316202> Bounty Hunter", "<:wheat:1248124503255420928> Streaker", "<:atts:1251039331955769385> Assistant (to the) Streaker", "<:coopcat:1251040069205360671> Co-op Cat", "<:conglomerate:1251040606160027679> Conglomerate", "<:gladiator:1251040731062341653> Gladiator", "<:fermentedspidereye:1248124676706926642> Vampire", "<:recon:1251040865850232903> Recon", "<:overheal:1251040981046919271> Overheal", "<:rambo:1251041176983703583> Rambo", "<:olympus:1251042140763721788> Olympus", "<:dirty:1251042306677542943> Dirty", "<:firststrike:1251042483811389474> First Strike", "<:mushroomstew:1248125413109141567> Soup", "<:marathon:1251043772200914944> Marathon", "<:thick:1251043923204243528> Thick", "<:kungfu:1251044013440630896> Kung Fu Knowledge", "<:goldenapple:1248127429084577913> Second Gapple", "<:xpboost:1251035226008850473> Explicious", "<:rr:1251044876703891516> R&R", "<:Arrow:1248117169653284926> Arquebusier", "<:goldenhelmet:1248126543553892443> Khanate", "<:leech:1251045967000633436> Leech", "<:toughskin:1251046230507782216> Tough Skin", "<:fightorflight:1251046419477954570> Fight or Flight", "<:fermentedspidereye:1248124676706926642> Pungent", "<:enchantedbook:1248119930155569222> Hero's Haste", "<:rush:1251046981405638706> Rush", "<:feast:1251047151333675038> Feast", "<:counterstrike:1251054076087504957> Counter-Strike", "<:trickledown:1251038830241517650> Gold Nano-Factory", "<:tacticalretreat:1251047854781497344> Tactical Retreat", "<:diamondpickaxe:1248119046172446792> Glass Pickaxe", "<:assuredstrike:1251048244155387935> Assured Strike", "<:auraofprot:1251048358617813123> Aura of Protection", "<:icecube:1251048590080475260> Ice Cube", "<:overheal:1251040981046919271> Super Streaker", "<:goldstack:1251048724424167445> Gold Stack", "<:xpstack:1251048813603586048> XP Stack", "<:thick:1251043923204243528> Monster", "<:spongesteve:1251048966582177802> Spongesteve", "<:aspostle:1251049079866392616> Apostle to RNGesus", "<:overdrive:1251049188763111447> Overdrive", "<:beastmode:1251049421236342887> Beastmode", "<:hermit:1251049608268742657> Hermit", "<:highlander:1251056305247092806> Highlander", "<:opus:1251049779400671272> Magnum Opus", "<:tothemoon:1251049903057010728> To the Moon", "<:uberstreak:1251050047014174793> Uberstreak"]


class upgrades(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="upgrades", description="Shows a players most purchased upgrades")
    async def upgrades(self, interaction: discord.Interaction, player: str):
        """
        Args:
            player (str): A Minecraft username
        """
        pass

        urlPP: str = f"https://pitpanda.rocks/api/players/{player}"
        data = getInfo(urlPP)

        global keys
        global names
        global namesFormated

        if not data["success"]:
            embedFail = discord.Embed(title="Player not found", color=discord.Color.red())

            await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa

        else:
            prestiges = data["data"].get("prestiges", [0])
            prestigeUpgrades = []

            prestigeStat = len(data["data"].get("prestiges", [0])) - 1
            currentXP = data["data"]["xpProgress"]["displayCurrent"]
            currentLevel = pit_functions.xpToLevel(prestigeStat, currentXP)

            for prestige in prestiges:
                unlocks = prestige.get("unlocks", [0])
                upgradesList = []
                for unlock in unlocks:
                    if unlock["type"] != "Renown":
                        upgradesList.append(unlock["key"])
                prestigeUpgrades.append(upgradesList)

            combined = []
            for prestige in prestigeUpgrades:
                combined += prestige

            counts = Counter(combined)
            mostPurchased = counts.most_common(25)

            embed = discord.Embed(title=f"Most purchased upgrades for [{formatting_functions.int_to_roman(prestigeStat)}{currentLevel}] {data['data']['name']}", color=pit_functions.calcBracketColor(prestigeStat))

            for item in mostPurchased:
                embed.add_field(name=namesFormated[keys.index(item[0])], value=f"Purchased {item[1]} times", inline=False)

            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{data['data']['uuid']}?format=webp")
            embed.set_footer(text=discord_functions.footerDateGen())

            await interaction.response.send_message(embed=embed) # noqa


async def setup(client: commands.Bot) -> None:
    await client.add_cog(upgrades(client))
