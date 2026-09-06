from classes.chat import Chat
from utils import strings
from utils.methods import offline_msg


class Offline(Chat):
    def __init__(self):
        self.message = offline_msg()
        super().__init__(strings.HEROBRINE, strings.HEROBRINE_IC, self.message)
        self.embed.set_footer(text=f"({strings.SERVER_STOP_TITLE})")

    def get_description(self):
        return [self.message]
