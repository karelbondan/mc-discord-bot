import json
import os
from time import strftime
from typing import Dict
from dotenv import load_dotenv

load_dotenv(override=True)

TOKEN = os.getenv("TOKEN")
TAB = " " * int(os.getenv("TAB_AMT"))
HEAD_URL = str(os.getenv("HEAD_URL"))
BODY_URL = str(os.getenv("BODY_URL"))
EMOJI_REPLY = str(os.getenv("EMOJI_REPLY"))
EMOJI_END = str(os.getenv("EMOJI_END"))
EMOJI_JOIN = str(os.getenv("EMOJI_JOIN"))
EMOJI_LEAVE = str(os.getenv("EMOJI_LEAVE"))
WEBHOOK_URL_OLD = str(os.getenv("WEBHOOK_URL_OLD"))
WEBHOOK_URL = str(os.getenv("WEBHOOK_URL"))
NOT_DEATHS = json.loads(os.getenv("NOT_DEATHS"))
RCON_PASS = str(os.getenv("RCON_PASS"))


def log(log: str):
    print(f"{strftime('%Y-%m-%d %H:%M:%S')} INFO{TAB}{log}")


def load_config() -> Dict[str, str]:
    with open("config.json") as config:
        return json.load(config)


def get_prefix() -> str:
    config = load_config()
    print(config["prefix"])
    return config["prefix"]


def get_channel_name() -> str:
    config = load_config()
    return config["channel_name"]


def get_channel_id() -> int:
    config = load_config()
    return config["channel_id"]
