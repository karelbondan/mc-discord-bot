from classes.builder import MCEmbedBuilderBase
import utils.constants as utils
import utils.strings as strings


class PlayerState(MCEmbedBuilderBase):
    def __init__(self, name: str, icon_url: str, state: str):
        super().__init__(name, icon_url)
        self.state = state
        self.format_embed(state=self.state)

    def format_embed(self, state: str):
        if state == "JOIN":
            title = f"{self.name} {utils.CONF_EMOJI_JOIN}"
            description = strings.PLAYER_JOIN.format(utils.CONF_EMOJI_END)
            color = utils.CONF_COLORS["green"]
        else:
            title = f"{self.name} {utils.CONF_EMOJI_LEAVE}"
            description = strings.PLAYER_LEAV.format(utils.CONF_EMOJI_END)
            color = utils.CONF_COLORS["red"]
        self.embed.title = title
        self.embed.description = description
        self.embed.color = color
        self.embed.set_thumbnail(url=self.icon_url)
        self.embed.set_footer(text=strings.PLAYER_FOOT.format(self.get_time()))
