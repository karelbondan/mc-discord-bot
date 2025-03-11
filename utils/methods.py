from time import strftime
from typing import Dict
import json
import utils.methods as methods
import utils.strings as strings
import utils.constants as const


def log(log: str):
    print(f"{strftime('%Y-%m-%d %H:%M:%S')} INFO{' ' * const.CONF_TAB}{log}")


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


def get_channel_name() -> str:
    config = load_config()
    return config["channel_name"]


def get_channel_id() -> int:
    config = load_config()
    return config["channel_id"]
