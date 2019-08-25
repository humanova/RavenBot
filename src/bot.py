# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import asyncio
import os

import discord
from discord.ext import commands
from discord.ext.commands import Bot

import drive
import env_set
import sheets
import zvz

env_set._set()

################################

Client = discord.Client()
client = commands.Bot(command_prefix="!")

zvz_command_whitelist = ['511938378447454219',
                         '252126151877722112',
                         '143869608154103808',
                         '166135493476483072',
                         '145305284070342656',
                         '241276711839203328',
                         '213262071050141696',
                         ]

ZVZChannelID = "613091570475860107"

def place_value(number):
    return ("{:,}".format(number))


async def GetZVZLinks():
    links = []
    async for m in client.logs_from(discord.Object(id=ZVZChannelID)):
        if 'killboard/kill/' in m.content:
            links.append(m.content)

    return links


@client.event
async def on_ready():
    print("Logged in as %s." % (client.user.name))


@client.event
async def on_message(message):

    if not message.author.bot == 1:

        if message.content.startswith("!zvz ") and message.author.id in zvz_command_whitelist:

            msgs = message.content.split(" ")
            if len(msgs) != 1:
                zvz_name = "".join(msgs[1:])
                print("preparing ZVZ : ", zvz_name)

                links = await GetZVZLinks()
                #print("links : ", links)

                player_data = zvz.GetVictimsInventory(links)
                items_data = zvz.GetTotalItems(player_data)
                done, dat = sheets.CreateZVZSheet(
                    zvz_name, items_data, player_data, links)

                if done:
                    print("uploading zvz worksheet")
                    drive.UploadFile(f"sheets/{zvz_name}.xlsx")
                    await client.send_message(discord.Object(id=ZVZChannelID), f"`ZVZ Spreadsheet Ravenloft Drive'a yüklendi.`")
                else:
                    print("couldn't create zvz worksheet")

                await client.send_message(discord.Object(id=ZVZChannelID), f"`[{zvz_name}] ZVZ Spreadsheet Dosyası:`")
                await client.send_file(discord.Object(id=ZVZChannelID), fp=f"sheets/{zvz_name}.xlsx")

                total_price = place_value(int(dat['total_price']))
                embed = discord.Embed(title=" ", color=0x75df00)
                embed.set_author(name="Ravenloft ZVZ Iade",
                                 icon_url=client.user.avatar_url)
                embed.add_field(name="ZVZ Adı", value=zvz_name, inline=False)
                embed.add_field(
                    name="Oyuncu Sayısı :", value=f"{len(player_data)}/{len(links)}", inline=False)
                embed.add_field(name="Iade Değeri :",
                                value=f"⁓{total_price}", inline=False)
                embed.set_footer(text=f"Tarih: {dat['date']}")
                await client.send_message(discord.Object(id=ZVZChannelID), embed=embed)

        if message.content == "!zvz-temizle" and message.author.id in zvz_command_whitelist:
            msgs = []
            async for m in client.logs_from(discord.Object(id=ZVZChannelID)):
                msgs.append(m)

            try:
                await client.delete_messages(msgs)
            except Exception as e:
                print(e)

token = os.environ['BOT_TOKEN']
client.run(token)
