# def leaderboardStuff():
#     global globalLeaderboardsList
#     global globalLeaderboardsFormatedList
#
#     with open("../PitStats/tokens_and_keys/PP_API_KEY.json", 'r') as f:
#         data = json.load(f)
#         key = data['TOKEN']
#
#     for i in range(0, len(globalLeaderboardsList) - 1):
#         embedPage = discord.Embed(title=f"{globalLeaderboardsFormatedList[i]}", color=discord.Color.greyple())
#         urlPP: str = f"https://pitpanda.rocks/api/leaderboard/{globalLeaderboardsList[i]}?page=0&pageSize=10&{key}"
#         leaderboard = getInfo(urlPP)
#         if not leaderboard["success"]:
#             print(urlPP)
#             try:
#                 print(leaderboard["error"])
#             except KeyError:
#                 print("invalid url")
#         else:
#             leaderboard = leaderboard["leaderboard"]
#             embedPage.add_field(name=f":first_place: #1", value=f"{formatting_functions.extract_name(leaderboard[0]['name'])}", inline=False)
#             embedPage.add_field(name=f":second_place: #2", value=f"{formatting_functions.extract_name(leaderboard[1]['name'])}", inline=False)
#             embedPage.add_field(name=f":third_place: #3", value=f"{formatting_functions.extract_name(leaderboard[2]['name'])}", inline=False)
#             for j in range(3, 10):
#                 name = formatting_functions.extract_name(leaderboard[j]["name"])
#                 embedPage.add_field(name=f"#{j + 1}", value=f"{name}", inline=False)
#         embedPages.append(embedPage)




# @app_commands.command(name="leaderboards-all", description="Shows top 10 leaderboard positions for all leaderboards")
# async def leaderboards(self, interaction: discord.Interaction):
#     await interaction.response.defer() # noqa
#
#     leaderboardStuff()
#     embed = discord.Embed(title="Pit Leaderboards", color=discord.Color.greyple())
#     embed.add_field(name="View the different top 10 players for the pit leaderboards", value="")
#
#     view = simpleView(timeout=None)
#
#     await interaction.followup.send(embed=embed, view=view)  # noqa