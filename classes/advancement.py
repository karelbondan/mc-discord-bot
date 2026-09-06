import utils.constants as utils
from classes.builder import MCEmbedBuilderBase
from utils import strings


class Advancement(MCEmbedBuilderBase):
    def __init__(self, name: str, icon_url: str, advancement: str, adv_name: str):
        super().__init__(name, icon_url)
        self.advancement = advancement
        self.adv_name = adv_name
        self.embed.title = strings.PLAYER_ACHV_TITLE.format(self.name)
        self.embed.description = strings.PLAYER_ACHV_DESCR.format(
            self.advancement, self.adv_name
        )
        self.embed.color = utils.Colors.GOLD.value
        self.embed.set_thumbnail(url=self.icon_url)
        self.embed.set_footer(text=strings.PLAYER_FOOT.format(self.get_time()))
