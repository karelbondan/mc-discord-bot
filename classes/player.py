import utils.constants as utils
import utils.strings as strings
from classes.builder import MCEmbedBuilderBase
from utils.constants import PlayerClient
from utils.constants import PlayerStateEnum


class PlayerState(MCEmbedBuilderBase):
    def __init__(
        self,
        name: str,
        icon_url: str,
        state: PlayerStateEnum,
        client: PlayerClient,
    ):
        super().__init__(name, icon_url)
        self.state = state
        self.client = client
        self.format_embed(state=self.state)

    def format_embed(self, state: PlayerStateEnum):
        if state == PlayerStateEnum.JOIN:
            title = f"{self.name} {utils.EMOJI_JOIN}"
            description = strings.PLAYER_JOIN.format(utils.EMOJI_END)
            color = utils.COLORS["green"]
        else:
            title = f"{self.name} {utils.EMOJI_LEAVE}"
            description = strings.PLAYER_LEAV.format(utils.EMOJI_END)
            color = utils.COLORS["red"]
        self.embed.title = title
        self.embed.description = description
        self.embed.color = color
        self.embed.set_thumbnail(url=self.icon_url)
        self.embed.set_footer(text=strings.PLAYER_FOOT.format(self.get_time()))
