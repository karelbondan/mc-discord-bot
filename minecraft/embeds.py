import json
from traceback import print_exc
from typing import Any, cast

from curl_cffi import requests

import utils.constants as consts
from classes.advancement import Advancement
from classes.chat import Chat
from classes.death import Death
from classes.player import PlayerState
from classes.state import ServerState
from utils import methods, strings
from utils.constants import PlayerClient, ServerStateEnum
from utils.constants import PlayerStateEnum as ConnectState


def is_bedrock(player_uuid: str):
    # > 39 because the texture id is saved as the "player uuid"
    # for bedrock (floodgate) players in players.json
    # and java uid when converted to base 16 is length 39
    return len(player_uuid) == 16 or len(player_uuid) > 39


def get_player_body(player_uuid: str):
    if is_bedrock(player_uuid):
        return consts.BEDROCK_BODY_URL.format(player_uuid)
    else:
        return consts.BODY_URL.format(player_uuid)


def get_player_head(player_uuid: str):
    if is_bedrock(player_uuid):
        return consts.BEDROCK_HEAD_URL.format(player_uuid)
    else:
        return consts.HEAD_URL.format(player_uuid)


def embed_player_joined(log: str) -> PlayerState:
    # try getting based on java pattern
    try:
        player_uuid: str = consts.RE_PLYR_UUID_JOIN.findall(log)[0]
        player_name = consts.RE_PLYR_NAME_JOIN.findall(log)[0]
        player_body_icon = consts.BODY_URL.format(player_uuid)
        player_client = PlayerClient.JAVA
        methods.log(f"{player_name} is a Java player")

    # get based on geyser pattern if fail
    except IndexError:
        player_uuid: str = consts.RE_PLYR_UUID_GYS_JOIN.findall(log)[0]
        player_name = consts.RE_PLYR_NAME_GYS_JOIN.findall(log)[0]
        player_body_icon = consts.BEDROCK_BODY_URL.format(player_uuid)
        player_client = PlayerClient.BEDROCK
        methods.log(f"{player_name} is a Bedrock player")

    # check if it's a floodgate uuid. the converted decimal will be 10^16
    possible_xuid = str(int(player_uuid.replace("-", ""), 16))

    if is_bedrock(possible_xuid):
        # get skin
        try:
            # if player is using minecraft official skin it will return error
            session = requests.Session(impersonate="chrome")
            headers = {
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://www.google.com/",
            }
            skin_data = session.get(
                consts.BEDROCK_SKIN_DATA_URL.format(possible_xuid),
                headers=headers,
            )
            methods.log(str(skin_data))
            player_uuid = skin_data.json()["texture_id"]
        except Exception:  # noqa
            print_exc()

    with open(f"{consts.ROOT_PATH}/players.json", "r+") as players_list:
        db = json.load(players_list)
        db[player_name] = player_uuid
        players_list.seek(0)
        players_list.truncate(0)
        json.dump(db, players_list, indent=4)

    methods.log(strings.LOG_PLAYRJOIN.format(player_name))
    return PlayerState(player_name, player_body_icon, ConnectState.JOIN, player_client)


def embed_player_leave(log: str) -> PlayerState:
    player_name = consts.RE_PLYR_LEAVE.findall(log)[0]
    player_name = cast(str, player_name).strip()

    methods.log(strings.LOG_PLAYRLEAV.format(player_name))

    with open(f"{consts.ROOT_PATH}/players.json", "r") as database:
        players_list = json.load(database)
    player_uuid = players_list[player_name]

    if is_bedrock(player_uuid):
        player_client = PlayerClient.BEDROCK
        player_body_icon = consts.BEDROCK_BODY_URL.format(player_uuid)
    else:
        player_client = PlayerClient.JAVA
        player_body_icon = consts.BODY_URL.format(player_uuid)

    return PlayerState(player_name, player_body_icon, ConnectState.LEAVE, player_client)


def embed_player_chat(latest: str, message: list[Any]) -> Chat:
    with open(f"{consts.ROOT_PATH}/players.json") as player_list:
        player_list_parsed = json.load(player_list)
        player_name = message[0]

        # finds character sequences with spaces after the sequence ">\s"
        player_chat = consts.RE_PLYR_MESSG.findall(latest)[0]
        player_uuid = player_list_parsed[player_name]
        player_icon = get_player_head(player_uuid)

        methods.log(strings.LOG_PLAYRCHAT.format(player_name, player_chat))
        return Chat(player_name, player_icon, player_chat)


def embed_player_chat_edit(prev: Chat, new: Chat) -> Chat:
    new_msg = new.get_description()[-1]
    prev.add_description(new_msg)
    return prev


def embed_player_advancement(adv: list[str]) -> Advancement:
    with open(f"{consts.ROOT_PATH}/players.json") as database:
        players_list = json.load(database)

        player_name = adv[0][-5]
        advancement_msg = adv[0][-4]
        advancement_name = adv[0][-1]

        player_uuid = players_list[player_name]
        player_icon = get_player_head(player_uuid)

        methods.log(strings.LOG_PLAYERADV.format(adv[0]))
        return Advancement(player_name, player_icon, advancement_msg, advancement_name)


def embed_player_death(cause: str) -> Death:
    with open(f"{consts.ROOT_PATH}/players.json") as database:
        players_list = json.load(database)
        player_name = consts.RE_PLYR_NAME_DEAD.findall(cause)[0]
        player_uuid = players_list[player_name]
        player_icon = get_player_head(player_uuid)

        methods.log(strings.LOG_PLYRDEATH.format(cause))
        return Death(player_name, player_icon, cause)


def embed_server_state(latest_chat: str) -> ServerState:
    if "Starting" in latest_chat:
        state = ServerStateEnum.STARTING
        methods.log(strings.LOG_SERVER_START)
    elif "auto-restart-initiated" in latest_chat:
        state = ServerStateEnum.RESTARTING
        methods.log(strings.LOG_SERVER_RESTART)
    else:
        state = ServerStateEnum.STOPPING
        methods.log(strings.LOG_SERVER_STOPS)
    return ServerState(state=state)
