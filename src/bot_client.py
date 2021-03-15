from typing import Optional

import asyncio
import re

import discord

from config import (
    TOKEN,
    NAME_REGEX_JOIN,
    NAME_REGEX_QUIT,
    ROYAL_ROLE_ID,
    PRISON_CHANNEL_ID,
    ROYAL_ROOM_ID,
    DISCONNECT_TIME,
    NATIONAL_ANTHEM
)
from src.utils.classes import Singleton
from src.classes.embed_factory import EmbedFactory
from src.classes.role_member import RoleMember
from src.utils.funtions import includes

ROYAL_ROOM_NAME = "皇室"
EXECUTE_REASON = "皇宮警察だ！！！"
HARASYO_JOIN_DESCRIPTION = "何かが始まる予感がする。"
HARASYO_QUIT_DESCRIPTION = "あいつは良い奴だったよ..."


class BotClient(discord.Client, Singleton):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        intents.members = True
        super(BotClient, self).__init__(presences=True, guild_subscriptions=True, intents=intents)

        self.guild: Optional[discord.Guild] = None
        self.prison_channel: Optional[discord.VoiceChannel] = None
        self.embed_factory: Optional[EmbedFactory] = None
        self.role_member: Optional[RoleMember] = None

    async def on_ready(self) -> None:
        self.guild = self.guilds[0]
        self.prison_channel = self.guild.get_channel(PRISON_CHANNEL_ID)

        my_avatar_url: str = self.user.avatar_url
        self.embed_factory = EmbedFactory(my_avatar_url)

        target_role: discord.Role = self.guild.get_role(ROYAL_ROLE_ID)
        self.role_member = RoleMember(target_role)

    async def on_message(self, message: discord.Message):
        if not message.embeds:
            return
        if not len(message.embeds) == 1:
            return

        embed = message.embeds[0]
        if ROYAL_ROOM_NAME not in embed.title:
            return

        if includes(embed.thumbnail.url, self.role_member.members_id):
            if embed.description == HARASYO_JOIN_DESCRIPTION:
                parsed_display_name = re.findall(NAME_REGEX_JOIN, embed.title)[0]
                response_embed = self.embed_factory.join(parsed_display_name)
                await message.channel.send(embed=response_embed)
                await message.delete(delay=None)

            elif embed.description == HARASYO_QUIT_DESCRIPTION:
                parsed_display_name = re.findall(NAME_REGEX_QUIT, embed.title)[0]
                response_embed = self.embed_factory.quit(parsed_display_name)
                await message.channel.send(embed=response_embed)
                await message.delete(delay=None)

    async def on_voice_state_update(self, member: discord.Member, _: discord.VoiceState, after: discord.VoiceState):
        if after.channel.id != ROYAL_ROOM_ID:
            return

        if member not in self.role_member.members:
            await self.execution(member)

    async def execution(self, member):
        await member.move_to(self.prison_channel, reason=EXECUTE_REASON)

        if not bool(self.voice_clients):
            return

        # TODO: VoiceChannel().connect() で戻ってくる型が変わっており、.play()がない
        voice_client = await self.prison_channel.connect(reconnect=False)
        voice_client.play(discord.FFmpegPCMAudio(source=NATIONAL_ANTHEM))
        await asyncio.sleep(DISCONNECT_TIME)
        await voice_client.disconnect(force=True)

    def run(self) -> None:
        super().run(TOKEN)
