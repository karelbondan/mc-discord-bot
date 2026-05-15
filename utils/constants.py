import os
import re
from pathlib import Path

import yaml
from dotenv import load_dotenv
from enum import Enum

import utils.strings as strings

load_dotenv(override=True)

# constants
with open("config.yml", "r") as config:
    CONFIG = yaml.safe_load(config)
    CONFIG = CONFIG["settings"]

## configs
COLORS = {
    "green": 0x36E066,
    "red": 0xE04536,
    "gray": 0xBEBEBE,
    "orange": 0xFF9100,
    "gold": 0xFFDE00,
}
ROOT_PATH = Path(__file__).parent.parent

BOT_TOKEN: str = os.getenv("TOKEN") or ""
BOT_PREFIX = CONFIG["bot"]["prefix"]

MC_HOST = os.getenv("MC_HOST") or "0.0.0.0"
MC_PORT = os.getenv("MC_PORT")
MC_PATH = CONFIG["minecraft"]["server_path"]

RCON_PASS = os.getenv("RCON_PASS") or ""
RCON_HOST = os.getenv("RCON_HOST") or "0.0.0.0"
RCON_PORT = int(os.getenv("RCON_PORT") or 25575)

TAB_AMOUNT: int = CONFIG["logging"]["tab_amount"]
LOG_READ_DELAY: float = CONFIG["logging"]["read_delay"]

HEAD_URL: str = CONFIG["discord"]["embed"]["url_head"]
BODY_URL: str = CONFIG["discord"]["embed"]["url_body"]
BEDROCK_SKIN_DATA_URL: str = CONFIG["discord"]["embed"]["url_skin_data_bedrock"]
BEDROCK_HEAD_URL: str = CONFIG["discord"]["embed"]["url_head_bedrock"]
BEDROCK_BODY_URL: str = CONFIG["discord"]["embed"]["url_body_bedrock"]

EMOJI_REPLY: str = CONFIG["discord"]["embed"]["emoji_reply"]
EMOJI_END: str = CONFIG["discord"]["embed"]["emoji_end"]
EMOJI_JOIN: str = CONFIG["discord"]["embed"]["emoji_join"]
EMOJI_LEAVE: str = CONFIG["discord"]["embed"]["emoji_leave"]

NOT_DEATHS: list[str] = CONFIG["miscellaneous"]["not_deaths"]
SERVER_STATES: list[str] = CONFIG["miscellaneous"]["server_states"]
IGNORE_PREFIX: list[str] = CONFIG["miscellaneous"]["ignore_prefixes"]

CHANNEL_ID: int = CONFIG["discord"]["channel_id"]
SERVER_ID: int = CONFIG["discord"]["server_id"]

## regexes
RE_ADVANCEMENT: re.Pattern = re.compile(strings.RE_S_ADV)
RE_ADV_MESSAGE: re.Pattern = re.compile(strings.RE_S_ADV_MSGE)
RE_ADV_IDENTIF: re.Pattern = re.compile(strings.RE_S_ADV_NAME)
RE_ADV_PLAYER: re.Pattern = re.compile(strings.RE_S_ADV_PLYR)
RE_CHALLENGE: re.Pattern = re.compile(strings.RE_S_CHAL)
RE_GOAL: re.Pattern = re.compile(strings.RE_S_GOAL)
RE_DEAD: re.Pattern = re.compile(strings.RE_S_DEATH)
RE_CHAT: re.Pattern = re.compile(strings.RE_S_CHAT)
RE_PLYR_NAME_JOIN: re.Pattern = re.compile(strings.RE_S_PLYR_NAME_JOIN)
RE_PLYR_UUID_JOIN: re.Pattern = re.compile(strings.RE_S_PLYR_UUID_JOIN)
RE_PLYR_NAME_DEAD: re.Pattern = re.compile(strings.RE_S_PLYR_NAME_DEAD)
RE_PLYR_NAME_GYS_JOIN: re.Pattern = re.compile(strings.RE_S_PLYR_NAME_GYSR_JOIN)
RE_PLYR_UUID_GYS_JOIN: re.Pattern = re.compile(strings.RE_S_PLYR_UUID_GYSR_JOIN)
RE_PLYR_LEAVE: re.Pattern = re.compile(strings.RE_S_PLYR_LEAVE)
RE_PLYR_MESSG: re.Pattern = re.compile(strings.RE_S_PLYR_MESSG)
RE_TPS_THREAD_NO: re.Pattern = re.compile(strings.RE_S_TPS_THREAD_NO)


class McClient(Enum):
    JAVA = "Java"
    BEDROCK = "Bedrock"


class ConnectState(Enum):
    JOIN = "Join"
    LEAVE = "Leave"
