import discord
import json
from discord import app_commands
from discord.ext import commands

from useful_things.api_functions import getInfo
from useful_things.pit_functions import calcBracketColor
from useful_things.pit_functions import xpToLevel
from useful_things.formatting_functions import int_to_roman
from useful_things import discord_functions


class discordFeatures(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="verify", description="Verify your Hypixel account")
    async def verify(self, interaction: discord.Interaction, player: str):
        """
        Args:
            player (str): A Minecraft username
        """
        pass

        with open("../PitStats/tokens_and_keys/API_KEY.json", 'r') as f:
            data = json.load(f)
            TOKEN = data['API_KEY']

        url: str = f"https://api.hypixel.net/v2/player?key={TOKEN}&name={player}"
        data = getInfo(url)

        if data["success"] is False:
            embedFail = discord.Embed(title="API on cooldown", color=discord.Color.red())

            await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa

        else:

            if data["player"] is None:
                embedFail = discord.Embed(title="Player not found", color=discord.Color.red())

                await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa

            else:
                username = interaction.user.name
                user = interaction.user
                socialMedia = data["player"].get("socialMedia", None)

                if socialMedia is None:
                    embedFail = discord.Embed(title="Discord account not linked", color=discord.Color.red())
                    embedFail.add_field(name="How to link your account", value="https://www.youtube.com/watch?v=zGvvpaUdyqs")

                    await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa

                else:
                    hypixelName = socialMedia["links"].get("DISCORD", None)

                    if hypixelName is None:
                        embedFail = discord.Embed(title="Discord account not linked", color=discord.Color.red())
                        embedFail.add_field(name="How to link your account", value="https://www.youtube.com/watch?v=zGvvpaUdyqs")

                        await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa

                    else:
                        if username == hypixelName:
                            urlPP: str = f"https://pitpanda.rocks/api/players/{player}"
                            data = getInfo(urlPP)

                            currentPrestige = len(data["data"].get("prestiges", [0])) - 1

                            xpProgress = data["data"].get("xpProgress", {})
                            display_current_xp = int(xpProgress.get("displayCurrent", 0))
                            currentLevel = xpToLevel(currentPrestige, display_current_xp)

                            embed = discord.Embed(title=f"Successfully linked", color=calcBracketColor(currentPrestige))
                            embed.add_field(name=f"", value=f"Linked {user.mention} as [{int_to_roman(currentPrestige)}{currentLevel}] {data['data']['name']}")
                            embed.set_image(url=f"https://pitpanda.rocks/api/images/profile/{data['data']['uuid']}")

                            await user.add_roles(discord_functions.getPrestigeRole(currentPrestige, interaction))

                            await interaction.response.send_message(embed=embed) # noqa
                        elif '#' in hypixelName:
                            embedFail = discord.Embed(title="You have a legacy discord account, relink your account", color=discord.Color.red())
                            embedFail.add_field(name="How to link your account", value="https://www.youtube.com/watch?v=zGvvpaUdyqs")

                            await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa
                        else:
                            embedFail = discord.Embed(title="Incorrect account linked", color=discord.Color.red())
                            embedFail.add_field(name="How to link your account", value="https://www.youtube.com/watch?v=zGvvpaUdyqs")

                            await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa

    @app_commands.command(name="verify-manual", description="Manually verify a players minecraft and discord account")
    @app_commands.checks.has_permissions(administrator=True)
    async def verify_manual(self, interaction: discord.Interaction, player: str, user: discord.Member):
        """
        Args:
            player (str): A Minecraft username
            user (discord.User) A discord user
        """
        pass

        failed = False
        urlPP: str = f"https://pitpanda.rocks/api/players/{player}"
        data = getInfo(urlPP)

        if not data["success"]:
            embedFail = discord.Embed(title="Player not found", color=discord.Color.red())

            await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa

        else:
            currentPrestige = len(data["data"].get("prestiges", [0])) - 1

            xpProgress = data["data"].get("xpProgress", {})
            display_current_xp = int(xpProgress.get("displayCurrent", 0))
            currentLevel = xpToLevel(currentPrestige, display_current_xp)

            embed = discord.Embed(title=f"Successfully linked", color=calcBracketColor(currentPrestige))
            embed.add_field(name=f"", value=f"Linked {user.mention} as [{int_to_roman(currentPrestige)}{currentLevel}] {data['data']['name']}")
            embed.set_image(url=f"https://pitpanda.rocks/api/images/profile/{data['data']['uuid']}")

            role = discord_functions.getPrestigeRole(currentPrestige, interaction)
            if role == 0:
                embedFail = discord.Embed(title="The necessary role does not exist", color=discord.Color.red())

                await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa
            else:
                try:
                    await user.add_roles(role)
                except AttributeError:
                    failed = True
                    embedFail = discord.Embed(title="The necessary role does not exist", color=discord.Color.red())

                    await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa

            if not failed:
                await interaction.response.send_message(embed=embed) # noqa

    @verify_manual.error
    async def on_test_error(self, interaction: discord.Interaction, error: discord.app_commands.errors.MissingPermissions):
        if isinstance(error, discord.app_commands.errors.MissingPermissions):
            await interaction.response.send_message(error, ephemeral=True)  # noqa
        else:
            raise error


async def setup(client: commands.Bot) -> None:
    await client.add_cog(discordFeatures(client))
