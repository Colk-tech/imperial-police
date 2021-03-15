from typing import Optional

import discord

from config import ROYAL_EMBLEM_URL
from src.utils.classes import Singleton


class EmbedFactory(Singleton):
    def __init__(self, my_avatar_url):
        self.MY_AVATAR_URL: str = my_avatar_url

    def join(self, member_name: str) -> discord.Embed:
        return self._create(member_name, is_join=True)

    def quit(self, member_name: str) -> discord.Embed:
        return self._create(member_name, is_join=False)

    def _create(self, member_name: str, is_join: bool) -> discord.Embed:
        message_in_or_out = "還幸" if is_join else "行幸"

        embed = discord.Embed(
            title="†卍 {} 卍† ".format(message_in_or_out),
            description="{} が{}なさいました。".format(member_name, message_in_or_out),
            color=0xffd800)

        embed.set_author(
            name="皇宮警察からのお知らせ",
            icon_url=self.MY_AVATAR_URL)

        embed.set_thumbnail(url=ROYAL_EMBLEM_URL)

        return embed
