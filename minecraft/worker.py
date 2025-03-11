from typing import Union, Tuple
from classes.advancement import Advancement
from classes.builder import MCEmbedBuilderBase
from classes.chat import Chat
from classes.death import Death
from classes.player import PlayerState
from classes.state import ServerState
from minecraft.embeds import *
import utils.constants as utils
import utils.methods as methods
import utils.strings as strings
import os


def get_embed_from_log(prev_msg: str = "", test_log: str = "") -> Tuple[
    str,
    Union[MCEmbedBuilderBase, Chat, PlayerState, Death, Advancement, ServerState, None],
]:
    try:
        with open("{}/logs/latest.log".format(utils.CONF_MC_PATH), "rb") as log:
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

            if any(prefix in latest_chat for prefix in utils.CONF_IGN_PREFIX):
                return (latest_chat, None)

            # player joined
            if "UUID" in latest_chat:
                return (latest_chat, embed_player_joined(latest_chat))

            # player left
            if "lost connection" in latest_chat:
                return (latest_chat, embed_player_leave(latest_chat))

            # player chat
            # finds character sequences after < and before >; gets the player name
            # is_chat = re.findall(r"(?<=<)\w+(?=>)", latest_chat)
            is_chat = utils.RE_CHAT.findall(latest_chat)
            if is_chat:
                return (latest_chat, embed_player_chat(latest_chat, is_chat))

            # advancement or challenge or goal
            is_advancement = utils.RE_ADVANCEMENT.findall(latest_chat)
            is_challenge = utils.RE_CHALLENGE.findall(latest_chat)
            is_goal = utils.RE_GOAL.findall(latest_chat)
            if is_advancement or is_challenge or is_goal:
                adv = is_advancement or is_challenge or is_goal
                return (latest_chat, embed_player_advancement(latest_chat, adv))

            # server start/stop
            if any(state in latest_chat for state in utils.CONF_SERVER_STATES):
                methods.log(strings.LOG_SERVER_STATE)
                return (latest_chat, embed_server_state(latest_chat))

            # matot
            is_death = utils.RE_DEAD.findall(latest_chat)
            try:
                if not any(trigger in is_death[0] for trigger in utils.CONF_NOT_DEATHS):
                    return (latest_chat, embed_player_death(is_death[0]))
            except IndexError:
                return (latest_chat, None)

            # if none of the above statements were satisfied
            return (latest_chat, None)
    except Exception as e:
        methods.log(strings.LOG_BOT_ERROR.format(repr(e)))

        # return nothing if an error was encountered
        return ("", None)
