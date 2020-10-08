from typing import Optional
import discord


class EmbedFactory:
    def __init__(self, royal_emblem_url: str, my_id: int, avatar: int):
        self.ROYAL_EMBLEM_URL: str = royal_emblem_url
        self.MY_ID: int = my_id
        self.AVATAR: int = avatar

    def create(self, member_name: str, is_in: bool) -> discord.Embed:
        message_in_or_out = "還幸" if is_in else "行幸"
        embed = discord.Embed(
            title="†卍 {} 卍† ".format(message_in_or_out),
            description="{} が{}なさいました。".format(member_name, message_in_or_out),
            color=0xffd800)
        embed.set_author(
            name="皇宮警察からのお知らせ",
            icon_url="https://cdn.discordapp.com/avatars/{}/{}.png".format(self.MY_ID, self.AVATAR))
        embed.set_thumbnail(url=self.ROYAL_EMBLEM_URL)
        return embed
