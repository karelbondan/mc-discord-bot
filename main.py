"""
Copyright 2024-present Karel Bondan
This bot was speficially made for one discord server.
No decision is currently made to expand this to be able to
handle multiple discord servers.
"""

import asyncio
from traceback import format_exc

from discord import Game, Intents, Message
from discord.channel import TextChannel
from discord.ext import commands
from mcstatus import JavaServer
from pygtail import Pygtail

import minecraft.rcon as rcon
import minecraft.worker as worker
import utils.constants as consts
import utils.methods as methods
import utils.strings as strings
from classes.chat import Chat
from classes.offline import Offline
from minecraft.embeds import embed_player_chat_edit

players_loaded = False
# previous message properties
prev_log: str = ""
prev_chat: Chat = Chat("", "", "")
prev_sent: Message | None = None

bot = commands.Bot(command_prefix=consts.BOT_PREFIX, intents=Intents.all())


@bot.command()
async def hello(ctx: commands.Context):
    msg = ctx.message
    methods.log(strings.LOG_CMD_HELLO.format(msg.author, msg.guild, msg.channel))
    await ctx.send(strings.RSP_HELLO)


@bot.command()
async def list(ctx: commands.Context):
    await ctx.send(rcon.rcon_list_users())


@bot.command()
async def ping(ctx: commands.Context):
    def __ping():
        origin = f"{consts.MC_HOST}"
        if consts.MC_PORT:
            origin += f":{consts.MC_PORT}"
        server = JavaServer.lookup(origin)
        return server.status().latency

    result = await bot.loop.run_in_executor(None, __ping)
    await ctx.send(str(round(result, 2)))


@bot.command()
async def tps(ctx: commands.Context):
    await ctx.send(f"```{rcon.send_command('tps')}```")


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

            channel = bot.get_channel(consts.CHANNEL_ID)
            if not channel or not isinstance(channel, TextChannel):
                raise RuntimeError(strings.LOG_CHANNEL_NOT_FOUND)

            log_path = "{}/logs/latest.log".format(consts.MC_PATH)
            logs = Pygtail(filename=log_path, save_on_end=True)
            if not logs:
                continue
            for log in logs:
                log = methods.strip_codes_ansiesc(log=str(log))
                prev_log, embed = worker.get_embed(prev_log=prev_log, log=log)

                # if no event then do nothing
                if embed is None:
                    continue

                # edit message if the embed type is Chat and if the player name is the same as the previous one
                if (
                    isinstance(embed, Chat)
                    and embed.get_name() == prev_chat.get_name()
                    and prev_sent
                ):
                    embed = embed_player_chat_edit(prev_chat, embed)
                    await prev_sent.edit(embed=embed.get_embed())
                # else just send a regular embed to the discord server
                else:
                    prev_sent = await channel.send(embed=embed.get_embed())

                # if the current type is Chat then set previous chat to be the embed
                if isinstance(embed, Chat):
                    prev_chat = embed
                # else reset previous chat to prevent the current message being edited when:
                # player A chats > other event happens > player A chats again
                else:
                    prev_chat = Chat("", "", "")
                await asyncio.sleep(consts.LOG_READ_DELAY)
        except Exception:
            methods.log(strings.LOG_BOT_ERROR.format(format_exc()))
        await asyncio.sleep(consts.LOG_READ_DELAY)


@bot.event
async def on_message(message: Message):
    if not isinstance(message.channel, TextChannel):
        return

    # process message to allow commands to be executed
    await bot.process_commands(message)

    if "herobrine" in message.content.lower():
        methods.log(strings.LOG_ONMESSAGE.format(message.author))
        await message.channel.send(strings.RSP_STEVE)

    # if last message was sent by the bot or any other bot then ignore
    if message.author == bot.user or message.author.bot:
        return
    
    # if last message not in designated channel then ignore
    if message.channel.id != consts.CHANNEL_ID:
        return

    # read all messages if all conditions were satisfied
    methods.log(strings.LOG_RCON_DCMC.format(message.author))

    # reset previous chat if someone sends a message from discord; for more clarity
    global prev_chat
    prev_chat = Chat("", "", "")

    # send message to mc server
    assert message.guild
    if message.guild.id == consts.SERVER_ID:
        try:
            rcon.send_to_mc_server(message)
        except ConnectionRefusedError:
            await message.channel.send(embed=Offline().get_embed())
            methods.log(strings.LOG_SERVER_OFFLN)


@bot.event
async def on_ready():
    await bot.change_presence(activity=Game(strings.BOT_GAME))
    methods.log(strings.BOT_READY)
    bot.loop.create_task(mc_to_discord_worker())


bot.run(token=consts.BOT_TOKEN)
