import time
import requests
from typing import Dict
from utils.constants import WEBHOOK_URL, EMOJI_REPLY, EMOJI_END, EMOJI_JOIN, EMOJI_LEAVE


class Builder:
    def __init__(self, name: str, icon_url: str):
        self.name = name
        self.icon_url = icon_url
        self.payload = {
            "embeds": [
                {
                    "author": {"name": self.name, "icon_url": icon_url},
                }
            ]
        }

    def get_name(self) -> str:
        return self.name

    def get_time(self) -> str:
        self.time = time.strftime("%H:%M")
        return self.time

    def get_payload(self) -> Dict[str, str]:
        return self.payload

    def set_payload(self, new_payload) -> bool:
        self.payload = new_payload
        return True

    def send_embed(self, id: int = 0) -> requests.Response:
        headers = {"Content-Type": "application/json"}
        if id != 0:
            url = WEBHOOK_URL.format(f"/messages/{id}")
            res = requests.patch(url=url, headers=headers, json=self.payload)
        else:
            url = WEBHOOK_URL.format("")
            res = requests.post(url=url, headers=headers, json=self.payload)
        return res


class Chat(Builder):
    def __init__(self, name: str, icon_url: str, msg: str):
        super().__init__(name, icon_url)
        self.description = [msg]
        self.payload = {
            "embeds": [
                {
                    "author": {"name": self.get_name(), "icon_url": icon_url},
                    "description": EMOJI_END + msg,
                    "color": 12500670,
                }
            ]
        }

    def add_description(self, msg: str) -> None:
        self.description.append(msg)
        new_desc = ""
        for desc in self.description:
            formatted = desc.replace("\n", "")
            if desc != self.description[-1]:
                new_desc += EMOJI_REPLY + formatted + "\n"
            else:
                new_desc += EMOJI_END + formatted
        embeds = {
            "author": {"name": self.get_name(), "icon_url": self.icon_url},
            "description": new_desc,
            "color": 12500670,
        }
        self.payload = {"embeds": [embeds]}

    def get_name(self) -> str:
        return f"{self.name} · {self.get_time()}"


class PlayerState(Builder):
    def __init__(self, name: str, icon_url: str, state: str):
        super().__init__(name, icon_url)
        self.state = state
        self.set_payload(state=self.state)

    def set_payload(self, state):
        if state == "JOIN":
            title = f"{self.name} {EMOJI_JOIN}"
            description = f"{EMOJI_END}Barusan masuk ke server"
            color = 3596390
        else:
            title = f"{self.name} {EMOJI_LEAVE}"
            description = f"{EMOJI_END}Barusan keluar dari server"
            color = 14697782
        self.payload = {
            "embeds": [
                {
                    "title": title,
                    "description": description,
                    "color": color,
                    "thumbnail": {"url": self.icon_url},
                    "footer": {"text": f"Fazbear Entertainment • {self.get_time()}"},
                }
            ]
        }

    def update_state(self, state):
        self.state = state
        self.set_payload(state=self.state)


class Death(Builder):
    def __init__(self, name: str, icon_url: str, cause: str):
        super().__init__(name, icon_url)
        self.cause = cause
        self.payload = {
            "embeds": [
                {
                    "title": f"Awokawok si {self.name} matot 🏃‍♂️💨",
                    "description": EMOJI_END + self.cause,
                    "color": 16748800,
                    "thumbnail": {"url": self.icon_url},
                }
            ]
        }


class Advancement(Builder):
    def __init__(self, name: str, icon_url: str, advancement: str, adv_name: str):
        super().__init__(name, icon_url)
        self.advancement = advancement
        self.adv_name = adv_name
        self.prefix = f"🏆 "
        self.payload = {
            "embeds": [
                {
                    "title": f"{self.name} puhh sepuhhh 🙏",
                    "description": f"{self.prefix} {self.advancement} **{self.adv_name}**",
                    "color": 16768512,
                    "thumbnail": {"url": self.icon_url},
                }
            ]
        }



# a = Advancement("", "", "", "")
# print(type(a) == Advancement)