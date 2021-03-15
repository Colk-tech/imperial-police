from typing import Optional, List

import discord

from src.utils.classes import Singleton


class RoleMember(Singleton):
    def __init__(self, target_role: discord.Role):
        self.role: discord.Role = target_role

    @property
    def members(self) -> Optional[List[discord.Member]]:
        return self.role.members

    @property
    def members_id(self) -> List[int]:
        return [member.id for member in self.members]
