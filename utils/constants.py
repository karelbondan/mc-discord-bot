from dotenv import load_dotenv
from pathlib import Path
import json
import os
import re
import utils.strings as strings

load_dotenv(override=True)

# constants
with open("config.json") as config:
    _CONFIG = json.load(config)

## configs
CONF_COLORS = {
    "green": 0x36E066,
    "red": 0xE04536,
    "gray": 0xBEBEBE,
    "orange": 0xFF9100,
    "gold": 0xFFDE00,
}
CONF_ROOT: str = Path(__file__).parent.parent
CONF_TOKEN: str = os.getenv("TOKEN")
CONF_RCON_PASS: str = str(os.getenv("RCON_PASS"))
CONF_RCON_PORT: int = _CONFIG["rcon_port"]
CONF_PREFIX: str = _CONFIG["bot_prefix"]
CONF_MC_PATH: str = _CONFIG["mc_path"]
CONF_TAB: int = _CONFIG["log_tab_amount"]
CONF_READ_DLAY: float = _CONFIG["log_read_delay"]
CONF_HEAD_URL: str = _CONFIG["url_head"]
CONF_BODY_URL: str = _CONFIG["url_body"]
CONF_EMOJI_REPLY: str = _CONFIG["emoji_reply"]
CONF_EMOJI_END: str = _CONFIG["emoji_end"]
CONF_EMOJI_JOIN: str = _CONFIG["emoji_join"]
CONF_EMOJI_LEAVE: str = _CONFIG["emoji_leave"]
CONF_NOT_DEATHS: list[str] = _CONFIG["not_deaths"]
CONF_SERVER_STATES: list[str] = _CONFIG["server_states"]
CONF_IGN_PREFIX: list[str] = _CONFIG["ignore_prefixes"]
CONF_CHANNEL_ID: int = _CONFIG["channel_id"]
CONF_CHANNEL_NM: str = _CONFIG["channel_name"]
CONF_SERVER_ID: int = _CONFIG["server_id"]

# deprecated
WEBHOOK_URL_OLD: str = str(os.getenv("WEBHOOK_URL_OLD"))
WEBHOOK_URL: str = str(os.getenv("WEBHOOK_URL"))

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
