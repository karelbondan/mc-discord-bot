from time import strftime

from discord import Embed


class MCEmbedBuilderBase:
    def __init__(self, name: str, icon_url: str):
        """Required: player name and player icon url"""
        self.name = name
        self.icon_url = icon_url
        self.embed = Embed()

    def get_time(self) -> str:
        return strftime("%H:%M")

    def __repr__(self):
        return repr(
            {
                "author": self.embed.author,
                "title": self.embed.title,
                "color": self.embed.color,
                "description": self.embed.description,
                "thumbnail": self.embed.thumbnail,
                "footer": self.embed.footer,
            }
        )
