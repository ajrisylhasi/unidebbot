import requests
import coc
import traceback

import discord
from discord.ext import commands

lines_to_read = [3]

f = open("discordbot.txt", "r")
auth = f.readlines()
auth = [x.strip() for x in auth]
f.close()

clan_tag = auth[4]
coc_client = coc.login(auth[0], auth[1], key_count=5, key_names="Bot key", client=coc.EventsClient, )

bot = commands.Bot(command_prefix='-')
INFO_CHANNEL_ID = int(auth[2])


@coc_client.event
@coc.ClanEvents.description_change()
async def player_donated_troops(old_player, new_player):
    print('{} has donated troops!'.format(new_player))


@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")


@bot.command()
async def commands(ctx):
    await ctx.send("!hello: Say hi to the bot\n!heroes: Gets gets player tags heroes\n!members: Gets clan members\n")


@bot.command()
async def heroes(ctx, player_tag):
    player = await coc_client.get_player(player_tag)

    to_send = ""
    for hero in player.heroes:
        to_send += "{}: Lv {}/{}\n".format(str(hero), hero.level, hero.max_level)
        await ctx.send(to_send)


@bot.command()
async def members(ctx):
    members1 = await coc_client.get_members(clan_tag)

    to_send = "members:\n"
    for player in members1:
        to_send += "{0} ({1})\n".format(player.name, player.tag)

    await ctx.send(to_send)


bot.run(auth[3])
bot.close()