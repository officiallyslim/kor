
import json
import os

import discord
import dotenv
import requests
from discord.ext import commands

from src.global_src.global_embed import no_perm_embed
from src.global_src.global_path import embed_path
from src.global_src.global_roles import (
    assistant_director_role_id,
    community_manager_role_id,
    developer_role_id,
    head_of_operations_role_id,
    mr_boomsteak_role_id,
    staff_manager_role_id,
)

dotenv.load_dotenv()
private_url = str(os.getenv("PRIVATE_API"))

class ConfirmView(discord.ui.View):
    def __init__(self, ctx, channel, content=None, embeds=None):
        super().__init__()
        self.ctx = ctx
        self.channel = channel
        self.content = content
        self.embeds = embeds

    @discord.ui.button(label="Confirm Send", style=discord.ButtonStyle.green, emoji="<:send:1181980373501100053>")
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.channel.send(content=self.content, embeds=self.embeds)
        button.disabled = True
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        self.stop()

class embed_sender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name = "send_embed", description = "Send embed in specifically channel")
    async def embed_sender(self, ctx: discord.ApplicationContext, channel: discord.TextChannel, file: discord.Attachment = None, discohook_link: str = None):
        if int(ctx.author.id) != 756509638169460837 and not any(role.id in [staff_manager_role_id, community_manager_role_id, assistant_director_role_id, head_of_operations_role_id, developer_role_id, mr_boomsteak_role_id] for role in ctx.author.roles):
            await ctx.respond(embed=no_perm_embed, ephemeral=True)
            return
        if file and discohook_link:
            await ctx.respond("You can't send JSON file and Discohook link at the same time!", ephemeral=True)
            return
        elif not file and not discohook_link:
            await ctx.respond("You need add JSON file or Discohook link!", ephemeral=True)
            return

        try:
            if discohook_link:
                response = requests.get(f"{private_url}/getEmbed", params={'url': discohook_link})
                data = response.json()
                with open(embed_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)
            elif file:
                await file.save(embed_path)

            with open(embed_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if 'message' in data:
                if data['message'] == "Error: Invalid URL":
                    await ctx.respond(content="Error: Invalid Discohook URL", ephemeral=True)
                elif data['message'] == "Error: Request failed with status code 404":
                    await ctx.respond(content="Error: Failed get Discohook embed (404)", ephemeral=True)
                elif data['message'] == "Error: Request failed with status code 500":
                    await ctx.respond(content="Error: HTTP Internal Server Error (500)", ephemeral=True)
            else:
                content = data[0]['content']
                embeds = [discord.Embed.from_dict(embed_info) for embed_info in data[0]['embeds']] if data[0]['embeds'] else None
                files = data[0].get('files', None)

                if files:
                    await ctx.respond(content="Error: Attachments are not supported for now.", ephemeral=True)
                else:
                    if content and embeds:
                        view = ConfirmView(ctx, channel, content=content, embeds=embeds)
                        await ctx.respond(f"Please confirm to send the message to <#{channel.id}>.", view=view, ephemeral=True)
                        preview_content = "## Preview\n" + content
                        await ctx.followup.send(content=preview_content, embeds=embeds, ephemeral=True)
                    elif content:
                        view = ConfirmView(ctx, channel, content=content)
                        await ctx.respond(f"Please confirm to send the message to <#{channel.id}>.", view=view, ephemeral=True)
                        preview_content = "## Preview\n" + content
                        await ctx.followup.send(content=preview_content, ephemeral=True)
                    elif embeds:
                        view = ConfirmView(ctx, channel, embeds=embeds)
                        await ctx.respond(f"Please confirm to send the message to <#{channel.id}>.", view=view, ephemeral=True)
                        await ctx.followup.send(content="## Preview",embeds=embeds, ephemeral=True)

        except Exception as e:
            await ctx.respond(f"Failed load embed. Error:```{e}```", ephemeral=True)

    @discord.slash_command(name = "send_dm_embed", description = "Send embed in DM")
    async def dm_sender(self, ctx: discord.ApplicationContext, user: discord.User, file: discord.Attachment = None, discohook_link: str = None):
        if int(ctx.author.id) != 756509638169460837 and not any(role.id in [staff_manager_role_id, community_manager_role_id, assistant_director_role_id, head_of_operations_role_id, developer_role_id, mr_boomsteak_role_id] for role in ctx.author.roles):
            await ctx.respond(embed=no_perm_embed, ephemeral=True)
            return
        if file and discohook_link:
            await ctx.respond("You can't send a JSON file and a Discohook link at the same time!", ephemeral=True)
            return
        elif not file and not discohook_link:
            await ctx.respond("You need to add a JSON file or a Discohook link!", ephemeral=True)
            return

        try:
            if discohook_link:
                response = requests.get(f"{private_url}/getEmbed", params={'url': discohook_link})
                data = response.json()
                with open(embed_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)
            elif file:
                await file.save(embed_path)

            with open(embed_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if 'message' in data:
                if data['message'] == "Error: Invalid URL":
                    await ctx.respond(content="Error: Invalid Discohook URL", ephemeral=True)
                elif data['message'] == "Error: Request failed with status code 404":
                    await ctx.respond(content="Error: Failed get Discohook embed (404)", ephemeral=True)
                elif data['message'] == "Error: Request failed with status code 500":
                    await ctx.respond(content="Error: HTTP Internal Server Error (500)", ephemeral=True)
            else:
                content = data[0]['content']
                embeds = [discord.Embed.from_dict(embed_info) for embed_info in data[0]['embeds']] if data[0]['embeds'] else None
                files = data[0].get('files', None)

                if files:
                    await ctx.respond(content="Error: Attachments are not supported for now.", ephemeral=True)
                else:
                    if content and embeds:
                        view = ConfirmView(ctx, user, content=content, embeds=embeds)
                        await ctx.respond(f"Please confirm to send the message to {user.mention}.", view=view, ephemeral=True)
                        preview_content = "## Preview\n" + content
                        await ctx.followup.send(content=preview_content, embeds=embeds, ephemeral=True)
                    elif content:
                        view = ConfirmView(ctx, user, content=content)
                        await ctx.respond(f"Please confirm to send the message to {user.mention}.", view=view, ephemeral=True)
                        preview_content = "## Preview\n" + content
                        await ctx.followup.send(content=preview_content, ephemeral=True)
                    elif embeds:
                        view = ConfirmView(ctx, user, embeds=embeds)
                        await ctx.respond(f"Please confirm to send the message to {user.mention}.", view=view, ephemeral=True)
                        await ctx.followup.send(embeds=embeds, ephemeral=True)

        except Exception as e:
            await ctx.respond(f"Failed to load embed. Error:```{e}```", ephemeral=True)

def setup(bot):
    bot.add_cog(embed_sender(bot))
