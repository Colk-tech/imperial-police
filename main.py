import asyncio
import os
import random
import re
from typing import Optional, Set

import discord
import datetime

from lib.utils import includes
from lib.embed_factory import EmbedFactory


ROYAL_EMBLEM_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Imperial_Seal_of_Japan.svg/500px-Imperial_Seal_of_Japan.svg.png"
NAME_REGEX_IN = re.compile(r"(.*?)が.*に入りました")
NAME_REGEX_OUT = re.compile(r"(.*?)が.*から抜けました")
ROYAL_ROOM_ID = 727133544773845013
LAWLESS_CHANNEL_ID = 690909527461199922
PRISON_CHANNEL_ID = 724591472061579295
ROYAL_QUALIFICATION_ROLE_ID = 727046372456661012
HARACHO_BOT_ID = 684295118643265548

NATIONAL_ANTHEM = "ast/snd/broken_national_anthem.wav"


class MainClient(discord.Client):
    def __init__(self, token) -> None:
        super().__init__()
        self.token: str = token
        self.guild: Optional[discord.Guild] = None
        self.royal_role: Optional[discord.Role] = None
        self.royal_members: Set[discord.Member] = {}

        self.embed_factory: Optional[EmbedFactory] = None

    async def on_ready(self) -> None:
        self.guild = self.guilds[0]
        self.royal_role = self.guild.get_role(ROYAL_QUALIFICATION_ROLE_ID)
        self.royal_members = self.royal_role.members

        self.embed_factory = EmbedFactory(ROYAL_EMBLEM_URL, self.user.id, self.user.avatar)

    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:
        if self.royal_role in after.roles:
            self.royal_members.add(after)
        else:
            if after in self.royal_members:
                self.royal_members.remove(after)

    async def on_message(self, message) -> None:
        if message.author.id != HARACHO_BOT_ID:
            return
        if message.embeds is None:
            return
        if len(message.embeds) <= 0:
            return

        embed = message.embeds[0]
        if includes(embed.thumbnail.url, self.royal_members):
            if "皇室" not in embed.title:
                return

            if embed.description == "何かが始まる予感がする。":
                parsed_display_name = re.findall(NAME_REGEX_IN, embed.title)[0]
                await message.channel.send(
                    embed=self.embed_factory.create(parsed_display_name, True))

            elif embed.description == "あいつは良い奴だったよ...":
                parsed_display_name = re.findall(NAME_REGEX_OUT, embed.title)[0]
                await message.channel.send(
                    embed=self.embed_factory.create(parsed_display_name, False))

            else:
                return

            await message.delete(delay=None)

    def run(self) -> None:
        super().run(self.token)


if __name__ == "__main__":
    TOKEN = "Njk0OTI1NjkxODAzNjY0NTI1.XoSt_A.rZnMYe3WFHhkIMIC0o6-VANG6aw"

    client = MainClient(TOKEN)
    client.run()
