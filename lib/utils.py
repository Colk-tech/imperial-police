import typing

import discord
from typing import Set


def includes(query: str, members: Set[discord.Member]):
    member_ids = [member.id for member in members]
    for test_case in member_ids:
        if str(test_case) in str(query):
            return True
    return False
