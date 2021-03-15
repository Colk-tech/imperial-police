import os
import re

TOKEN: str = os.environ["IMPERIAL_POLICE_TOKEN"]

RESPONSE_CHANNEL_ID: int = 690909527461199922
ROYAL_ROLE_ID: int = 727046372456661012
ROYAL_ROOM_ID: int = 727133544773845013
PRISON_CHANNEL_ID: int = 724591472061579295

NATIONAL_ANTHEM: str = "ast/snd/broken_national_anthem.wav"
DISCONNECT_TIME: int = 67

ROYAL_EMBLEM_URL: str = \
    "https://upload.wikimedia.org/wikipedia/commons/" + \
    "thumb/3/37/Imperial_Seal_of_Japan.svg/500px-Imperial_Seal_of_Japan.svg.png"

NAME_REGEX_JOIN: re.Pattern = re.compile(r"(.*?)が.*に入りました")
NAME_REGEX_QUIT: re.Pattern = re.compile(r"(.*?)が.*から抜けました")
