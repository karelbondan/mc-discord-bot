# import os
import re
from os import path
from random import randint
from time import strftime

import utils.constants as const
from utils import strings


def log(log: str):
    print(f"{strftime('%Y-%m-%d %H:%M:%S')} INFO{' ' * const.TAB_AMOUNT}{log}")


def strip_codes_ansiesc(log: str) -> str:
    return re.sub(strings.RE_S_CMD_CHAT, "", log)


def strip_codes_color(resp: str) -> str:
    return re.sub(strings.RE_S_CMD_COLR, "", resp)


def initialize_player_cache():
    log(strings.LOG_GETPLAYER)

    # initialize player uuid cache on first run
    cache_path = f"{const.ROOT_PATH}/players.json"
    if not path.isfile(cache_path):
        with open(cache_path, "a") as cache:
            cache.write("{}")

    log(strings.LOG_GETPLRSCC)


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
