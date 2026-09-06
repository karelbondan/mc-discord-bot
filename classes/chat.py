import utils.constants as utils
from classes.builder import MCEmbedBuilderBase
from utils import strings


class Chat(MCEmbedBuilderBase):
    def __init__(self, name: str, icon_url: str, msg: str):
        super().__init__(name, icon_url)
        self.description = [msg]
        self.embed.set_author(
            name=strings.PLAYER_CHAT.format(self.name, self.get_time()),
            icon_url=self.icon_url,
        )
        self.embed.description = utils.EMOJI_END + msg
        self.embed.color = utils.Colors.GRAY.value

    def add_description(self, msg: str) -> None:
        self.description.append(msg)
        new_desc = ""
        for desc in self.description:
            formatted = desc.replace("\n", "")
            if desc != self.description[-1]:
                new_desc += utils.EMOJI_REPLY + formatted + "\n"
            else:
                new_desc += utils.EMOJI_END + formatted
        self.embed.description = new_desc

    def get_description(self) -> list:
        return self.description
