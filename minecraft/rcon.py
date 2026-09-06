import re

from discord import Message
from mcrcon import MCRcon

import utils.constants as consts
from utils import methods, strings


def send_command(command: str):
    with MCRcon(consts.RCON_HOST, consts.RCON_PASS, port=consts.RCON_PORT) as mcr:
        response = mcr.command(command)
        response = methods.strip_codes_color(resp=response)
        methods.log(strings.LOG_RCONMCSCC.format(response))
        return response


def send_to_mc_server(context: Message):
    tellraw = strings.RCON_TELLRAW.format(context.author, context.content)
    send_command(tellraw)


def rcon_list_users():
    online = send_command("list")
    online = re.sub(strings.RE_S_CMD_LIST, "", online)
    return online
