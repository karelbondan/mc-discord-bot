from mcrcon import MCRcon
from discord import Message
import utils.constants as consts
import utils.strings as strings
import utils.methods as methods
import re


def send_command(command: str):
    with MCRcon("0.0.0.0", consts.CONF_RCON_PORT, consts.CONF_RCON_PASS) as mcr:
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
