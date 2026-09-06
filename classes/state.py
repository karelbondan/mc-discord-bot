import utils.constants as utils
from classes.builder import MCEmbedBuilderBase
from utils import strings
from utils.constants import ServerStateEnum


class ServerState(MCEmbedBuilderBase):
    def __init__(self, state: ServerStateEnum, name: str = "", icon_url: str = ""):
        super().__init__(name, icon_url)
        self.server_state = state
        self.format_embed(server_state=self.server_state)

    def format_embed(self, server_state: ServerStateEnum):
        if server_state == ServerStateEnum.STARTING:
            title = strings.SERVER_START_TITLE
            desc = strings.SERVER_START_DESCR
            color = utils.Colors.GREEN.value
        elif server_state == ServerStateEnum.RESTARTING:
            title = strings.SERVER_RESTART_TITLE
            desc = strings.SERVER_RESTART_DESCR
            color = utils.Colors.ORANGE.value
        else:
            title = strings.SERVER_STOP_TITLE
            desc = strings.SERVER_STOP_DESCR
            color = utils.Colors.RED.value
        self.embed.title = title
        self.embed.description = desc
        self.embed.color = color
        self.embed.set_footer(text=strings.PLAYER_FOOT.format(self.get_time()))
