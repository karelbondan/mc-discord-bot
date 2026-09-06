from traceback import format_exc

import utils.constants as utils
from classes.advancement import Advancement
from classes.builder import MCEmbedBuilderBase
from classes.chat import Chat
from classes.death import Death
from classes.player import PlayerState
from classes.state import ServerState
from minecraft import embeds
from utils import methods, strings


def get_embed(
    log: str, prev_log: str = "", test_log: str = ""
) -> tuple[
    str,
    MCEmbedBuilderBase | Chat | PlayerState | Death | Advancement | ServerState | None,
]:
    try:
        # get last line
        latest_log = log

        # test purposes
        if test_log:
            latest_log = test_log

        if latest_log == prev_log:
            return (latest_log, None)

        if any(prefix in latest_log for prefix in utils.IGNORE_PREFIX):
            return (latest_log, None)

        # player joined
        if "UUID" in latest_log:
            return (latest_log, embeds.embed_player_joined(latest_log))

        # player left
        if "lost connection" in latest_log:
            return (latest_log, embeds.embed_player_leave(latest_log))

        # player chat
        # finds character sequences after < and before >; gets the player name
        # is_chat = re.findall(r"(?<=<)\w+(?=>)", latest_log)
        is_chat = utils.RE_CHAT.findall(latest_log)
        if is_chat:
            return (latest_log, embeds.embed_player_chat(latest_log, is_chat))

        # advancement or challenge or goal
        is_advancement = utils.RE_ADVANCEMENT.findall(latest_log)
        if is_advancement:
            return (latest_log, embeds.embed_player_advancement(is_advancement))

        # server start/stop
        if any(state in latest_log for state in utils.SERVER_STATES):
            methods.log(strings.LOG_SERVER_STATE)
            return (latest_log, embeds.embed_server_state(latest_log))

        # matot
        is_death = utils.RE_DEAD.findall(latest_log)
        try:
            is_death = is_death[0][-1]
            if not any(trigger in is_death for trigger in utils.NOT_DEATHS):
                return (latest_log, embeds.embed_player_death(is_death))
        except IndexError, KeyError:
            return (latest_log, None)

        # if none of the above statements were satisfied
        return (latest_log, None)
    except Exception:  # noqa
        methods.log(strings.LOG_BOT_ERROR.format(format_exc()))

        # return nothing if an error was encountered
        return ("", None)
