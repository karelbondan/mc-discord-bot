from embed_builder import *
from typing import Union, Tuple, List
from discord import Message
from mcrcon import MCRcon
import utilities
import json
import os
import re

MC_VERSION = "1.21.4"


def load_players():
    utilities.log("Getting and appending players...")
    with open(f"/home/monty/Server/minecraft-{MC_VERSION}-spigot/usercache.json") as server_players:
        with open("./players.json", "w") as database:
            parsed = json.load(server_players)
            players_list = {}

            for player in parsed:
                if player["name"] not in players_list:
                    players_list[player["name"]] = player["uuid"]

            json.dump(players_list, database)
    utilities.log("Players appended successfully")


def embed_player_joined(latest_chat: str) -> PlayerState:
    # bugrock
    if "Floodgate" in latest_chat:
        player_name = re.findall(r"(?<=as\s)\w+", latest_chat)[0]
        player_uuid = re.findall(r"(?<=UUID:\s)[\w-]+", latest_chat)[0]
    # java
    else:
        player_name = re.findall(r"(?<=player\s)\w+", latest_chat)[0]
        player_uuid = re.findall(r"(?<=is\s)[\w-]+", latest_chat)[0]
    player_body_icon = utilities.BODY_URL.format(player_uuid)

    utilities.log(f"[JOIN] {player_name} joined the server")

    players_list = json.load(open("./players.json"))
    players_list[player_name] = player_uuid
    with open("./players.json", "w") as database:
        json.dump(players_list, database)

    return PlayerState(player_name, player_body_icon, state="JOIN")


def embed_player_leave(latest_chat: str) -> PlayerState:
    player_name = re.findall(r"(?<=]:\s)\w+", latest_chat)[0]

    utilities.log(f"[LEAVE] {player_name} left the server")

    with open("./players.json", "r") as database:
        players_list = json.load(database)
        player_uuid = players_list[player_name]
        player_body_icon = utilities.BODY_URL.format(player_uuid)
        return PlayerState(player_name, player_body_icon, state="LEAVE")


def embed_player_chat(latest_chat: str, is_chat: str) -> Chat:
    player_list = open("./players.json")
    player_list_parsed = json.load(player_list)
    player_name = is_chat[0]
    # finds character sequences with spaces after the sequence ">\s"
    player_chat = re.findall(r"(?<=>\s).+", latest_chat)[0]
    player_icon = utilities.HEAD_URL.format(player_list_parsed[player_name])
    player_list.close()

    utilities.log(f"[CHAT] {player_name}: {player_chat}")

    return Chat(player_name, player_icon, player_chat)


def embed_player_chat_edit(previous_chat: Chat, new_chat: Chat) -> Chat:
    new_msg = new_chat.get_description()[-1]
    previous_chat.add_description(new_msg)
    return previous_chat


def embed_player_advancement(latest_chat: str, player_advancement: List[str]) -> Advancement:
    with open("./players.json") as database:
        players_list = json.load(database)
        advancement_msg = re.findall(r"(?<=\[Server\sthread/INFO\]\:\s)[^\[]*", player_advancement[0])[0]
        # gets from latest_chat -> regex terminates before square brackets -> acv name
        advancement_name = re.findall(r"(?<=\[)[^\]]*", latest_chat)[2]
        player_name = re.findall(r"(?<=\[Server\sthread/INFO\]\:\s)[^\s]*", player_advancement[0])[0]
        player_icon = utilities.HEAD_URL.format(players_list[player_name])

        utilities.log(f"[ADV/CHAL] {player_advancement[0]}")

        return Advancement(player_name, player_icon, advancement_msg, advancement_name)


def embed_player_death(is_possible_death: List[str]) -> Death:
    with open("./players.json") as database:
        players_list = json.load(database)
        player_name = re.findall(r"^[^\s]*", is_possible_death[0])[0]
        player_icon = utilities.HEAD_URL.format(players_list[player_name])
        death_cause = is_possible_death[0]

        utilities.log(f"[DEATH] {death_cause}")

        return Death(player_name, player_icon, death_cause)


def embed_server_state(latest_chat: str) -> ServerState:
    if "Starting" in latest_chat:
        state = "STARTING"
        utilities.log("[START] Starting server...")
    else:
        state = "STOPPING"
        utilities.log("[STOP] Stopping server...")
    return ServerState(state=state)


def get_embed_from_log(
    prev_msg: str = "", test_log: str = ""
) -> Tuple[str, Union[MCEmbedBuilderBase, Chat, PlayerState, Death, Advancement, ServerState, None]]:
    try:
        with open(f"/home/monty/Server/minecraft-{MC_VERSION}-spigot/logs/latest.log", "rb") as log:
            # get last line
            try:
                log.seek(-2, os.SEEK_END)
                while log.read(1) != b"\n":
                    log.seek(-2, os.SEEK_CUR)
            except OSError:
                log.seek(0)

            latest_chat = log.readline().decode()

            # test purposes
            if test_log:
                latest_chat = test_log

            if latest_chat == prev_msg:
                return (latest_chat, None)

            if any(prefix in latest_chat for prefix in ["/w", "/msg", "/tell", "issued server command: /"]):
                return (latest_chat, None)

            # player joined
            if "UUID" in latest_chat:
                return (latest_chat, embed_player_joined(latest_chat))

            # player left
            if "lost connection" in latest_chat:
                return (latest_chat, embed_player_leave(latest_chat))

            # player chat
            # finds character sequences after < and before >; gets the player name
            is_chat = re.findall(r"(?<=<)\w+(?=>)", latest_chat)
            if is_chat:
                return (latest_chat, embed_player_chat(latest_chat, is_chat))

            # advancement or challenge or goal
            is_advancement = re.findall(r"\[Server\sthread/INFO\]\:\s[^\s]*\shas\smade\sthe\sadvancement", latest_chat)
            is_challenge = re.findall(r"\[Server\sthread/INFO\]\:\s[^\s]*\shas\scompleted\sthe\schallenge", latest_chat)
            is_goal = re.findall(r"\[Server\sthread/INFO\]\:\s[^\s]*\shas\sreached\sthe\sgoal", latest_chat)
            if is_advancement or is_challenge or is_goal:
                if is_advancement:
                    player_advancement = is_advancement
                elif is_challenge:
                    player_advancement = is_challenge
                else:
                    player_advancement = is_goal
                return (latest_chat, embed_player_advancement(latest_chat, player_advancement))

            # server start/stop
            if any(
                server_state in latest_chat
                for server_state in [
                    "Starting minecraft server",
                    "Starting Minecraft server on",
                    "Stopping the server",
                    "Stopping server",
                ]
            ):
                utilities.log("[START/STOP] Server state embed format triggered")
                return (latest_chat, embed_server_state(latest_chat))

            # matot
            is_possible_death = re.findall(r"(?<=\[Server\sthread/INFO\]\:\s)[^\[\:\.]+$", latest_chat)
            try:
                if not any(trigger in is_possible_death[0] for trigger in utilities.NOT_DEATHS):
                    return (latest_chat, embed_player_death(is_possible_death))
            except IndexError:
                return (latest_chat, None)

            # if none of the above statements were satisfied
            return (latest_chat, None)
    except Exception as e:
        utilities.log(f"[ERR] {repr(e)}")

        # return nothing if an error was encountered
        return ("", None)


def send_command(command: str):
    with MCRcon(host="0.0.0.0", port=42013, password=utilities.RCON_PASS) as mcr:
        response = mcr.command(command)
        utilities.log(f"Minecraft server successfully received command: {response}")
        return response


def send_to_mc_server(context: Message):
    tellraw = 'tellraw @a [{{"text": "<{}> ", "color": "blue"}}, {{"text": "{}", "color": "white"}}]'
    tellraw = tellraw.format(context.author, context.content)
    send_command(tellraw)


def rcon_list_users():
    return send_command("list")
