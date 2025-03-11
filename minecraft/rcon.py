from mcrcon import MCRcon
from discord import Message
import utils.constants as consts
import utils.strings as strings
import utils.methods as methods


def send_command(command: str):
    with MCRcon(host="0.0.0.0", port=42013, password=consts.CONF_RCON_PASS) as mcr:
        response = mcr.command(command)
        methods.log(strings.LOG_RCONMCSCC.format(response))
        return response


def send_to_mc_server(context: Message):
    tellraw = strings.RCON_TELLRAW.format(context.author, context.content)
    send_command(tellraw)


def rcon_list_users():
    return send_command("list")
