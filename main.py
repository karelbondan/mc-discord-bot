"""
Copyright 2024 Karel Bondan
This bot was speficially made for one discord server.
No decision is currently made to expand this to be able to 
handle multiple discord servers.
"""

import utilities
import worker
from discord import Intents, Message, Game
from discord.ext import commands, tasks
from embed_builder import *


players_loaded = False

# previous message properties
previous_log: str = ""
previous_chat: Chat = Chat("", "", "")
previous_sent: Message = None

bot = commands.Bot(command_prefix=".mc.", intents=Intents.all())


@bot.command()
async def hello(ctx: commands.Context):
    message = ctx.message
    utilities.log(f'"Hello" command invoked by {message.author} in {message.guild} at {message.channel}')
    await ctx.send("memek goreng")
    
@bot.command()
async def list(ctx: commands.Context):
    response = worker.rcon_list_users()
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
        worker.load_players()
        players_loaded = True

    channel = bot.get_channel(utilities.get_channel_id())
    previous_log, formatted_embed = worker.get_embed_from_log(prev_msg=previous_log)

    # if no event then do nothing
    if formatted_embed == None:
        return

    # edit message if the embed type is Chat and if the player name is the same as the previous one
    if type(formatted_embed) == Chat and formatted_embed.get_name() == previous_chat.get_name():
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

    if message.content.lower() == "herobrine":
        utilities.log(f'OnMessage event invoked for listener "herobrine" by {message.author}')
        await message.channel.send("Here be Steve...")

    # if not in the desired channel then do nothing
    if utilities.get_channel_name() not in message.channel.name.lower():
        return

    # if last message was sent by the bot then ignore
    if message.author == bot.user:
        return

    # read all messages if all conditions were satisfied
    utilities.log(f"OnMessage event invoked by {message.author} to forward the message to the mc server")

    # reset previous chat if someone sends a message from discord; for more clarity
    global previous_chat
    previous_chat = Chat("", "", "")

    # send message to mc server
    worker.send_to_mc_server(message)


@bot.event
async def on_ready():
    await bot.change_presence(activity=Game("on your Minecraft server"))
    utilities.log("Herobrine was summoned and is now stalking your Minecraft server")
    mc_to_discord_worker.start()


bot.run(token=utilities.TOKEN)
