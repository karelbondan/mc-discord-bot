"""
Copyright 2024 Karel Bondan
This bot was speficially made for one discord server.
No decision is currently made to expand this to be able to
handle multiple discord servers.
"""

import utils.constants as consts
import utils.methods as methods
import utils.strings as strings
import minecraft.worker as worker
import minecraft.rcon as rcon
import asyncio
from discord import Intents, Message, Game
from discord.ext import commands
from classes.chat import Chat
from typing import List
from pygtail import Pygtail
from traceback import format_exc

players_loaded = False
# previous message properties
prev_log: str = ""
prev_chat: Chat = Chat("", "", "")
prev_sent: Message = None

bot = commands.Bot(command_prefix=consts.CONF_PREFIX, intents=Intents.all())


@bot.command()
async def hello(ctx: commands.Context):
    message = ctx.message
    methods.log(
        strings.LOG_CMD_HELLO.format(message.author, message.guild, message.channel)
    )
    await ctx.send(strings.RSP_HELLO)


@bot.command()
async def list(ctx: commands.Context):
    response = rcon.rcon_list_users()
    await ctx.send(response)


async def mc_to_discord_worker():
    """
    Minecraft server log listener. Will listen for player actions and send them into a
    specified channel in a discord server in a form of embed.
    """
    # declare global variables
    global players_loaded, prev_log, prev_sent, prev_chat

    while True:
        try:
            if not players_loaded:
                methods.load_players()
                players_loaded = True

            channel = bot.get_channel(methods.get_channel_id())

            log_path = "{}/logs/latest.log".format(consts.CONF_MC_PATH)
            logs: List[str] = Pygtail(filename=log_path, save_on_end=True)
            if logs:
                for log in logs:
                    prev_log, embed = worker.get_embed(prev_log=prev_log, log=log)

                    # if no event then do nothing
                    if embed == None:
                        continue

                    # edit message if the embed type is Chat and if the player name is the same as the previous one
                    if type(embed) == Chat and embed.get_name() == prev_chat.get_name():
                        embed = worker.embed_player_chat_edit(prev_chat, embed)
                        await prev_sent.edit(embed=embed.get_embed())
                    # else just send a regular embed to the discord server
                    else:
                        prev_sent = await channel.send(embed=embed.get_embed())

                    # if the current type is Chat then set previous chat to be the embed
                    if type(embed) == Chat:
                        prev_chat = embed
                    # else reset previous chat to prevent the current message being edited when:
                    # player A chats > other event happens > player A chats again
                    else:
                        prev_chat = Chat("", "", "")
                    await asyncio.sleep(consts.CONF_READ_DLAY)
        except Exception as e:
            methods.log(strings.LOG_BOT_ERROR.format(format_exc()))
        await asyncio.sleep(consts.CONF_READ_DLAY)


@bot.event
async def on_message(message: Message):
    # process message to allow commands to be executed
    await bot.process_commands(message)

    if "herobrine" in message.content.lower():
        methods.log(strings.LOG_ONMESSAGE.format(message.author))
        await message.channel.send(strings.RSP_STEVE)

    # if not in the desired channel then do nothing
    if methods.get_channel_name() not in message.channel.name.lower():
        return

    # if last message was sent by the bot then ignore
    if message.author == bot.user:
        return

    # read all messages if all conditions were satisfied
    methods.log(strings.LOG_RCON_DCMC.format(message.author))

    # reset previous chat if someone sends a message from discord; for more clarity
    global prev_chat
    prev_chat = Chat("", "", "")

    # send message to mc server
    rcon.send_to_mc_server(message)


@bot.event
async def on_ready():
    await bot.change_presence(activity=Game(strings.BOT_GAME))
    methods.log(strings.BOT_READY)
    bot.loop.create_task(mc_to_discord_worker())


bot.run(token=consts.CONF_TOKEN)
