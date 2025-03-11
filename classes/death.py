from classes.builder import MCEmbedBuilderBase
import utils.constants as utils
import utils.strings as strings


class Death(MCEmbedBuilderBase):
    def __init__(self, name: str, icon_url: str, cause: str):
        super().__init__(name, icon_url)
        self.cause = cause
        self.embed.title = strings.PLAYER_DEAD.format(self.name)
        self.embed.description = utils.CONF_EMOJI_END + self.cause
        self.embed.color = utils.CONF_COLORS["orange"]
        self.embed.set_thumbnail(url=self.icon_url)
        self.embed.set_footer(text=strings.PLAYER_FOOT.format(self.get_time()))
