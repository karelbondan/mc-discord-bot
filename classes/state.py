from classes.builder import MCEmbedBuilderBase
import utils.constants as utils
import utils.strings as strings


class ServerState(MCEmbedBuilderBase):
    def __init__(self, state: str, name: str = "", icon_url: str = ""):
        super().__init__(name, icon_url)
        self.server_state = state
        self.format_embed(server_state=self.server_state)

    def format_embed(self, server_state: str):
        if server_state == "STARTING":
            title = strings.SERVER_START_TITLE
            desc = strings.SERVER_START_DESCR
            color = utils.COLORS["green"]
        else:
            title = strings.SERVER_STOP_TITLE
            desc = strings.SERVER_STOP_DESCR
            color = utils.COLORS["red"]
        self.embed.title = title
        self.embed.description = desc
        self.embed.color = color
        self.embed.set_footer(text=strings.PLAYER_FOOT.format(self.get_time()))
