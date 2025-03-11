from typing import List
from classes.advancement import Advancement
from classes.chat import Chat
from classes.death import Death
from classes.player import PlayerState
from classes.state import ServerState
import utils.constants as consts
import utils.methods as methods
import utils.strings as strings
import json


def embed_player_joined(log: str) -> PlayerState:
    # bugrock
    if "Floodgate" in log:
        player_name = consts.RE_PLYR_NAME_GYS_JOIN.findall(log)[0]
        player_uuid = consts.RE_PLYR_UUID_GYS_JOIN.findall(log)[0]
    # java
    else:
        player_name = consts.RE_PLYR_NAME_JOIN.findall(log)[0]
        player_uuid = consts.RE_PLYR_UUID_JOIN.findall(log)[0]

    player_body_icon = consts.CONF_BODY_URL.format(player_uuid)
    players_list = json.load(open("{}./players.json".format(consts.CONF_ROOT)))
    players_list[player_name] = player_uuid
    with open("{}./players.json".format(consts.CONF_ROOT), "w") as database:
        json.dump(players_list, database)

    methods.log(strings.LOG_PLAYRJOIN.format(player_name))
    return PlayerState(player_name, player_body_icon, state="JOIN")


def embed_player_leave(log: str) -> PlayerState:
    player_name = consts.RE_PLYR_LEAVE.findall(log)[0]

    methods.log(strings.LOG_PLAYRLEAV.format(player_name))

    with open("{}./players.json".format(consts.CONF_ROOT), "r") as database:
        players_list = json.load(database)
        player_uuid = players_list[player_name]
        player_body_icon = consts.CONF_BODY_URL.format(player_uuid)
        return PlayerState(player_name, player_body_icon, state="LEAVE")


def embed_player_chat(latest: str, message: str) -> Chat:
    player_list = open("{}./players.json".format(consts.CONF_ROOT))
    player_list_parsed = json.load(player_list)
    player_name = message[0]
    # finds character sequences with spaces after the sequence ">\s"
    player_chat = consts.RE_PLYR_MESSG.findall(latest)[0]
    player_icon = consts.CONF_HEAD_URL.format(player_list_parsed[player_name])
    player_list.close()

    methods.log(strings.LOG_PLAYRCHAT.format(player_name, player_chat))
    return Chat(player_name, player_icon, player_chat)


def embed_player_chat_edit(prev: Chat, new: Chat) -> Chat:
    new_msg = new.get_description()[-1]
    prev.add_description(new_msg)
    return prev


def embed_player_advancement(log: str, adv: List[str]) -> Advancement:
    with open("{}./players.json".format(consts.CONF_ROOT)) as database:
        players_list = json.load(database)

        # gets from log -> regex terminates before square brackets -> acv name
        advancement_msg = consts.RE_ADV_MESSAGE.findall(adv[0])[0]
        advancement_name = consts.RE_ADV_IDENTIF.findall(log)[2]

        player_name = consts.RE_ADV_PLAYER.findall(adv[0])[0]
        player_icon = consts.CONF_HEAD_URL.format(players_list[player_name])

        methods.log(strings.LOG_PLAYERADV.format(adv[0]))
        return Advancement(player_name, player_icon, advancement_msg, advancement_name)


def embed_player_death(cause: str) -> Death:
    with open("{}./players.json".format(consts.CONF_ROOT)) as database:
        players_list = json.load(database)
        player_name = consts.RE_PLYR_NAME_DEAD.findall(cause)[0]
        player_icon = consts.CONF_HEAD_URL.format(players_list[player_name])

        methods.log(strings.LOG_PLYRDEATH.format(cause))
        return Death(player_name, player_icon, cause)


def embed_server_state(latest_chat: str) -> ServerState:
    if "Starting" in latest_chat:
        state = "STARTING"
        methods.log(strings.LOG_SERVER_START)
    else:
        state = "STOPPING"
        methods.log(strings.LOG_SERVER_STOPS)
    return ServerState(state=state)
