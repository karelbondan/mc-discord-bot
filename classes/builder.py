from discord import Embed
from time import strftime


class MCEmbedBuilderBase:
    def __init__(self, name: str, icon_url: str):
        """Required: player name and player icon url"""
        self.name = name
        self.icon_url = icon_url
        self.embed = Embed()

    def get_embed(self) -> Embed:
        """Gets the current embed set for this object"""
        return self.embed

    def get_name(self) -> str:
        return self.name

    def get_time(self) -> str:
        self.time = strftime("%H:%M")
        return self.time

    def set_embed(self, embed: Embed) -> None:
        """
        Warning: This will overwrite the previous embed that has been set for this object.
        Make sure you have set the new embed correctly before setting it as the new embed.
        """
        self.embed = embed

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
