import os
from os import getenv
from dotenv import load_dotenv

load_dotenv()
admins = {}

# REQUIRED VARIABLES
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
STRING_SESSION = getenv("STRING_SESSION", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "60"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "2021310005").split()))


# EXTRA VARIABLES
ALIVE_IMG = getenv("ALIVE_IMG", "https://telegra.ph/file/fc9d87ffd1c6f828eb7fc.png")
START_PIC = getenv("START_PIC", "https://telegra.ph/file/fc9d87ffd1c6f828eb7fc.png")
IMG_1 = getenv("IMG_1", "https://telegra.ph/file/d6f92c979ad96b2031cba.png")
IMG_2 = getenv("IMG_2", "https://telegra.ph/file/6213d2673486beca02967.png")
IMG_3 = getenv("IMG_3", "https://telegra.ph/file/f02efde766160d3ff52d6.png")
IMG_4 = getenv("IMG_4", "https://telegra.ph/file/be5f551acb116292d15ec.png")
IMG_5 = getenv("IMG_5", "https://telegra.ph/file/d08d6474628be7571f013.png")
