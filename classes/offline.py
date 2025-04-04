from classes.chat import Chat
from utils.methods import offline_msg
import utils.strings as strings


class Offline(Chat):
    def __init__(self):
        self.message = offline_msg()
        super().__init__(strings.HEROBRINE, strings.HEROBRINE_IC, self.message)
        self.embed.set_footer(text="({})".format(strings.SERVER_STOP_TITLE))

    def get_description(self):
        return self.message
