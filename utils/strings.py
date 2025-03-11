# strings
## regex strings
RE_S_ADV = r"\[Server\sthread/INFO\]\:\s[^\s]*\shas\smade\sthe\sadvancement"
RE_S_ADV_MSGE = r"(?<=\[Server\sthread/INFO\]\:\s)[^\[]*"
RE_S_ADV_NAME = r"(?<=\[)[^\]]*"
RE_S_ADV_PLYR = r"(?<=\[Server\sthread/INFO\]\:\s)[^\s]*"
RE_S_CHAL = r"\[Server\sthread/INFO\]\:\s[^\s]*\shas\scompleted\sthe\schallenge"
RE_S_GOAL = r"\[Server\sthread/INFO\]\:\s[^\s]*\shas\sreached\sthe\sgoal"
RE_S_DEATH = r"(?<=\[Server\sthread/INFO\]\:\s)[^\[\:\.]+$"
RE_S_CHAT = r"(?<=<)\w+(?=>)"
RE_S_PLYR_NAME_JOIN = r"(?<=player\s)\w+"
RE_S_PLYR_UUID_JOIN = r"(?<=is\s)[\w-]+"
RE_S_PLYR_NAME_DEAD = r"^[^\s]*"
RE_S_PLYR_NAME_GYSR_JOIN = r"(?<=as\s)\w+"
RE_S_PLYR_UUID_GYSR_JOIN = r"(?<=UUID:\s)[\w-]+"
RE_S_PLYR_LEAVE = r"(?<=]:\s)\w+"
RE_S_PLYR_MESSG = r"(?<=>\s).+"

## bot stuff
BOT_GAME = "on your Minecraft server"
BOT_READY = "Herobrine was summoned and is now stalking your Minecraft server"

## responses
RSP_HELLO = "memek goreng"
RSP_STEVE = "Here be Steve..."

## log strings
LOG_CMD_HELLO = '"Hello" command invoked by {} in {} at {}'
LOG_GETPLAYER = "Getting and appending players..."
LOG_GETPLRSCC = "Players appended successfully"
LOG_ONMESSAGE = 'OnMessage event invoked for listener "herobrine" by {}'
LOG_PLAYERADV = "[ADV/CHAL] {}"
LOG_PLAYRCHAT = "[CHAT] {}: {}"
LOG_PLYRDEATH = "[DEATH] {}"
LOG_PLAYRLEAV = "[LEAVE] {} left the server"
LOG_PLAYRJOIN = "[JOIN] {} joined the server"
LOG_RCON_DCMC = "OnMessage event invoked by {} to forward the message to the mc server"
LOG_RCONMCSCC = "Minecraft server successfully received command: {}"
LOG_SERVER_STATE = "[START/STOP] Server state embed format triggered"
LOG_SERVER_START = "[START] Starting server..."
LOG_SERVER_STOPS = "[STOP] Stopping server..."
LOG_BOT_ERROR = "[ERR] {}"

## embeds
SERVER_START_TITLE = "Servernya udah nyala lagi"
SERVER_START_DESCR = "Kemungkinan masih belum bisa join, tunggu dulu bentar"
SERVER_STOP_TITLE = "Servernya mati"
SERVER_STOP_DESCR = "Lagi maintenance, sabar ya boti"
PLAYER_JOIN = "{}Barusan masuk ke server"
PLAYER_LEAV = "{}Barusan keluar dari server"
PLAYER_DEAD = "Awokawok si {} matot 🏃‍♂️💨"
PLAYER_FOOT = "Fazbear Entertainment • {}"
PLAYER_CHAT = "{} · {}"
PLAYER_ACHV_TITLE = "{} puhh sepuhhh 🙏"
PLAYER_ACHV_DESCR = "🏆 {} **{}**"

## others
RCON_TELLRAW = 'tellraw @a [{{"text": "<{}> ", "color": "blue"}}, {{"text": "{}", "color": "white"}}]'
