"""
Copyright 2024 Karel Bondan
This bot was speficially made for one discord server.
No decision is currently made to expand this to be able to
handle multiple discord servers.
"""

import utils.constants as constants
import utils.methods as methods
import utils.strings as strings
import minecraft.worker as worker
import minecraft.rcon as rcon
from discord import Intents, Message, Game
from discord.ext import commands, tasks
from classes.chat import Chat


players_loaded = False

# previous message properties
previous_log: str = ""
previous_chat: Chat = Chat("", "", "")
previous_sent: Message = None

bot = commands.Bot(command_prefix=constants.CONF_PREFIX, intents=Intents.all())


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


@tasks.loop(seconds=0.001)
async def mc_to_discord_worker():
    """
    Minecraft server log listener. Will listen for player actions and send them into a
    specified channel in a discord server in a form of embed.
    """
    # declare global variables
    global players_loaded, previous_log, previous_sent, previous_chat

    if not players_loaded:
        methods.load_players()
        players_loaded = True

    channel = bot.get_channel(methods.get_channel_id())
    previous_log, formatted_embed = worker.get_embed_from_log(prev_msg=previous_log)

    # if no event then do nothing
    if formatted_embed == None:
        return

    # edit message if the embed type is Chat and if the player name is the same as the previous one
    if (
        type(formatted_embed) == Chat
        and formatted_embed.get_name() == previous_chat.get_name()
    ):
        formatted_embed = worker.embed_player_chat_edit(previous_chat, formatted_embed)
        await previous_sent.edit(embed=formatted_embed.get_embed())
    # else just send a regular embed to the discord server
    else:
        previous_sent = await channel.send(embed=formatted_embed.get_embed())

    # if the current type is Chat then set previous chat to be the embed
    if type(formatted_embed) == Chat:
        previous_chat = formatted_embed
    # else reset previous chat to prevent the current message being edited when:
    # player A chats > other event happens > player A chats again
    else:
        previous_chat = Chat("", "", "")


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
    global previous_chat
    previous_chat = Chat("", "", "")

    # send message to mc server
    rcon.send_to_mc_server(message)


@bot.event
async def on_ready():
    await bot.change_presence(activity=Game(strings.BOT_GAME))
    methods.log(strings.BOT_READY)
    mc_to_discord_worker.start()


bot.run(token=constants.CONF_TOKEN)
