from discord import Embed
import utilities
import time

colors = {"green": 0x36E066, "red": 0xE04536, "gray": 0xBEBEBE, "orange": 0xFF9100, "gold": 0xFFDE00}


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
        self.time = time.strftime("%H:%M")
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


class Chat(MCEmbedBuilderBase):
    def __init__(self, name: str, icon_url: str, msg: str):
        super().__init__(name, icon_url)
        self.description = [msg]
        self.embed.set_author(name=f"{self.name} · {self.get_time()}", icon_url=self.icon_url)
        self.embed.description = utilities.EMOJI_END + msg
        self.embed.color = colors["gray"]

    def add_description(self, msg: str) -> None:
        self.description.append(msg)
        new_desc = ""
        for desc in self.description:
            formatted = desc.replace("\n", "")
            if desc != self.description[-1]:
                new_desc += utilities.EMOJI_REPLY + formatted + "\n"
            else:
                new_desc += utilities.EMOJI_END + formatted
        self.embed.description = new_desc

    def get_description(self) -> list:
        return self.description


class PlayerState(MCEmbedBuilderBase):
    def __init__(self, name: str, icon_url: str, state: str):
        super().__init__(name, icon_url)
        self.state = state
        self.format_embed(state=self.state)

    def format_embed(self, state: str):
        if state == "JOIN":
            title = f"{self.name} {utilities.EMOJI_JOIN}"
            description = f"{utilities.EMOJI_END}Barusan masuk ke server"
            color = colors["green"]
        else:
            title = f"{self.name} {utilities.EMOJI_LEAVE}"
            description = f"{utilities.EMOJI_END}Barusan keluar dari server"
            color = colors["red"]
        self.embed.title = title
        self.embed.description = description
        self.embed.color = color
        self.embed.set_thumbnail(url=self.icon_url)
        self.embed.set_footer(text=f"Fazbear Entertainment • {self.get_time()}")


class Death(MCEmbedBuilderBase):
    def __init__(self, name: str, icon_url: str, cause: str):
        super().__init__(name, icon_url)
        self.cause = cause
        self.embed.title = f"Awokawok si {self.name} matot 🏃‍♂️💨"
        self.embed.description = utilities.EMOJI_END + self.cause
        self.embed.color = colors["orange"]
        self.embed.set_thumbnail(url=self.icon_url)
        self.embed.set_footer(text=f"Fazbear Entertainment • {self.get_time()}")


class Advancement(MCEmbedBuilderBase):
    def __init__(self, name: str, icon_url: str, advancement: str, adv_name: str):
        super().__init__(name, icon_url)
        self.advancement = advancement
        self.adv_name = adv_name
        self.embed.title = f"{self.name} puhh sepuhhh 🙏"
        self.embed.description = f"🏆 {self.advancement} **{self.adv_name}**"
        self.embed.color = colors["gold"]
        self.embed.set_thumbnail(url=self.icon_url)
        self.embed.set_footer(text=f"Fazbear Entertainment • {self.get_time()}")


class ServerState(MCEmbedBuilderBase):
    def __init__(self, state: str, name: str = "", icon_url: str = ""):
        super().__init__(name, icon_url)
        self.server_state = state
        self.format_embed(server_state=self.server_state)

    def format_embed(self, server_state: str):
        if server_state == "STARTING":
            title = "Servernya udah nyala lagi"
            desc = "Kemungkinan masih belum bisa join, tunggu dulu bentar"
            color = colors["green"]
        else:
            title = "Servernya mati"
            desc = "Lagi maintenance, sabar ya boti"
            color = colors["red"]
        self.embed.title = title
        self.embed.description = desc
        self.embed.color = color
        self.embed.set_footer(text=f"Fazbear Entertainment • {self.get_time()}")
