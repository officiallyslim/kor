import discord

class jump_channel(discord.ui.View):
    def __init__(self, guild_id, channel_id):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label='Jump in!', url=f'https://discord.com/channels/{guild_id}/{channel_id}'))