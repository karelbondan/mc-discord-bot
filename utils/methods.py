from time import strftime
from typing import Dict
from random import randint
import json
import re
import utils.methods as methods
import utils.strings as strings
import utils.constants as const


def log(log: str):
    print(f"{strftime('%Y-%m-%d %H:%M:%S')} INFO{' ' * const.CONF_TAB}{log}")


def strip_codes_ansiesc(log: str) -> str:
    return re.sub(strings.RE_S_CMD_CHAT, "", log)


def strip_codes_color(resp: str) -> str:
    return re.sub(strings.RE_S_CMD_COLR, "", resp)


def load_players():
    methods.log(strings.LOG_GETPLAYER)
    with open("{}/usercache.json".format(const.CONF_MC_PATH)) as server_players:
        methods.log(const.CONF_ROOT)
        with open("{}/players.json".format(const.CONF_ROOT), "w") as database:
            parsed = json.load(server_players)
            players_list = {}

            for player in parsed:
                if player["name"] not in players_list:
                    players_list[player["name"]] = player["uuid"]

            json.dump(players_list, database)
    methods.log(strings.LOG_GETPLRSCC)


def load_config() -> Dict[str, str]:
    with open("config.json") as config:
        return json.load(config)


def offline_msg() -> str:
    msgs = [
        strings.SERVER_OFFLINE_1,
        strings.SERVER_OFFLINE_2,
        strings.SERVER_OFFLINE_3,
        strings.SERVER_OFFLINE_4,
        strings.SERVER_OFFLINE_5,
        strings.SERVER_OFFLINE_6,
        strings.SERVER_OFFLINE_7,
        strings.SERVER_OFFLINE_8,
        strings.SERVER_OFFLINE_9,
        strings.SERVER_OFFLINE_10,
    ]
    rand = randint(0, 9)
    return msgs[rand]
