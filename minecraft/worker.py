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


def get_embed(log: str, prev_log: str = "", test_log: str = "") -> Tuple[
    str,
    Union[MCEmbedBuilderBase, Chat, PlayerState, Death, Advancement, ServerState, None],
]:
    try:
        # get last line
        latest_log = log

        # test purposes
        if test_log:
            latest_log = test_log

        if latest_log == prev_log:
            return (latest_log, None)

        if any(prefix in latest_log for prefix in utils.CONF_IGN_PREFIX):
            return (latest_log, None)

        # player joined
        if "UUID" in latest_log:
            return (latest_log, embed_player_joined(latest_log))

        # player left
        if "lost connection" in latest_log:
            return (latest_log, embed_player_leave(latest_log))

        # player chat
        # finds character sequences after < and before >; gets the player name
        # is_chat = re.findall(r"(?<=<)\w+(?=>)", latest_log)
        is_chat = utils.RE_CHAT.findall(latest_log)
        if is_chat:
            return (latest_log, embed_player_chat(latest_log, is_chat))

        # advancement or challenge or goal
        is_advancement = utils.RE_ADVANCEMENT.findall(latest_log)
        is_challenge = utils.RE_CHALLENGE.findall(latest_log)
        is_goal = utils.RE_GOAL.findall(latest_log)
        if is_advancement or is_challenge or is_goal:
            adv = is_advancement or is_challenge or is_goal
            return (latest_log, embed_player_advancement(latest_log, adv))

        # server start/stop
        if any(state in latest_log for state in utils.CONF_SERVER_STATES):
            methods.log(strings.LOG_SERVER_STATE)
            return (latest_log, embed_server_state(latest_log))

        # matot
        is_death = utils.RE_DEAD.findall(latest_log)
        try:
            if not any(trigger in is_death[0] for trigger in utils.CONF_NOT_DEATHS):
                return (latest_log, embed_player_death(is_death[0]))
        except IndexError:
            return (latest_log, None)

        # if none of the above statements were satisfied
        return (latest_log, None)
    except Exception as e:
        methods.log(strings.LOG_BOT_ERROR.format(repr(e)))

        # return nothing if an error was encountered
        return ("", None)
