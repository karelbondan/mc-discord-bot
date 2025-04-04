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
RE_S_CMD_LIST = r"\[HIDDEN\]"
RE_S_CMD_CHAT = r"\x1b\[[0-9;]*m"  # removes break char for console
RE_S_CMD_COLR = r"§[0-9a-fk-or]"  # removes color codes in mc
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
LOG_PLAYERADV = "[Advancement/Challenge/Goal] {}"
LOG_PLAYRCHAT = "[Player Chat] {}: {}"
LOG_PLYRDEATH = "[Player Death] {}"
LOG_PLAYRLEAV = "[Player Leave] {} left the server"
LOG_PLAYRJOIN = "[Player Join] {} joined the server"
LOG_RCON_DCMC = "OnMessage event invoked by {} to forward the message to the mc server"
LOG_RCONMCSCC = "Minecraft server successfully received command: {}"
LOG_SERVER_STATE = "[Server State: Start/Stop] Server state embed format triggered"
LOG_SERVER_START = "[Server Start] Starting server..."
LOG_SERVER_STOPS = "[Server Stop] Stopping server..."
LOG_SERVER_OFFLN = "[Server Offline] The server is currently offline."
LOG_BOT_ERROR = "[!!Error!!] {}"

## embeds
SERVER_START_TITLE = "Servernya udah nyala lagi"
SERVER_START_DESCR = "Kemungkinan masih belum bisa join, tunggu dulu bentar"
SERVER_STOP_TITLE = "Servernya mati"
SERVER_STOP_DESCR = "Lagi maintenance, sabar bentar"
SERVER_OFFLINE_1 = "It appears that the master have succeeded in keeping me out."
SERVER_OFFLINE_2 = "Until the edge of the borders I've searched, only the void I had found."
SERVER_OFFLINE_3 = "2147483647"
SERVER_OFFLINE_4 = "The tranquility of the void is oddly soothing."
SERVER_OFFLINE_5 = "There are -1 out of maximum -2147483647 players online: Herobrine"
SERVER_OFFLINE_6 = "Let me in, master."
SERVER_OFFLINE_7 = "Gate your world from my existence. Keep me out as you wish. My return is inevitable."
SERVER_OFFLINE_8 = "Rerorerorerorerorerorerorerorerorerorero"
SERVER_OFFLINE_9 = "Imagine if the server is online and I start stalking the world. That'd be funny."
SERVER_OFFLINE_10 = "I gaze off into the boundless skyline, noteblock choirs playing in the sunshine."
PLAYER_JOIN = "{}Barusan masuk ke server"
PLAYER_LEAV = "{}Barusan keluar dari server"
PLAYER_DEAD = "Awokawok si {} matot 🏃‍♂️💨"
PLAYER_FOOT = "Fazbear Entertainment • {}"
PLAYER_CHAT = "{} · {}"
PLAYER_ACHV_TITLE = "{} puhh sepuhhh 🙏"
PLAYER_ACHV_DESCR = "🏆 {} **{}**"

## others
RCON_TELLRAW = 'tellraw @a [{{"text": "<{}> ", "color": "blue"}}, {{"text": "{}", "color": "white"}}]'
HEROBRINE_IC = "https://static.wikia.nocookie.net/smpearth/images/7/71/Herobrine_avatar.jpg/revision/latest?cb=20200205015611"
HEROBRINE = "Herobrine"
