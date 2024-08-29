import discord
import dotenv
import os

from src.ticket.utils.builder_request_utils.db_utils.Ticket import Ticket

dotenv.load_dotenv()
private_api = str(os.getenv("PRIVATE_API"))

def create_ticket_info_embed(ticket_data: Ticket, current_ticket_status):
    if current_ticket_status == "Ticket is open":
        info_embed = discord.Embed(
            title=f"Ticket {ticket_data.ticket_id} information",
            description=f"""
                        **📢 Current status: {current_ticket_status}** 
                        **🙍 Open user:** <@{ticket_data.open_user_id}>
                        **❓ Ticket type:** <@{ticket_data.open_user_id}>
                        **🕑 Open time:** <t:{ticket_data.open_time}:F>
                        **🏠 Channel:** <#{ticket_data.channel_id}>""",
            colour=discord.Colour(int("5cb85c", 16)),
        )
        # info_embed.add_field(
        #     name="Roblox user (form)",
        #     value=f"```{ticket_data.form_roblox_user}```",
        #     inline=False,
        # )
        # info_embed.add_field(
        #     name="Island Code (form)",
        #     value=f"```{ticket_data.form_island_code}```",
        #     inline=False,
        # )
        # info_embed.add_field(
        #     name="Build (form)", value=f"```{ticket_data.form_build}```", inline=False
        # )
        # info_embed.add_field(
        #     name="Payment (form)",
        #     value=f"```{ticket_data.form_payment}```",
        #     inline=False,
        # )
        info_embed.set_footer(text=f"Ticket ID: {ticket_data.ticket_id}")
        return info_embed

    elif (
        current_ticket_status == f"Currently claimed by <@{ticket_data.claim_user_id}>"
    ):
        info_embed = discord.Embed(
            title=f"Ticket {ticket_data.ticket_id} information",
            description=f"""
                        **📢 Current status: {current_ticket_status}** 
                        **🙍 Open user:** <@{ticket_data.open_user_id}>
                        **💁 Claim user:** <@{ticket_data.claim_user_id}>
                        **❓ Ticket type:** <@{ticket_data.open_user_id}>
                        **🕑 Open time:** <t:{ticket_data.open_time}:F>
                        **🏠 Channel:** <#{ticket_data.channel_id}>""",
            colour=discord.Colour(int("5cb85c", 16)),
        )
        # info_embed.add_field(
        #     name="Roblox user (form)",
        #     value=f"```{ticket_data.form_roblox_user}```",
        #     inline=False,
        # )
        # info_embed.add_field(
        #     name="Island Code (form)",
        #     value=f"```{ticket_data.form_island_code}```",
        #     inline=False,
        # )
        # info_embed.add_field(
        #     name="Build (form)", value=f"```{ticket_data.form_build}```", inline=False
        # )
        # info_embed.add_field(
        #     name="Payment (form)",
        #     value=f"```{ticket_data.form_payment}```",
        #     inline=False,
        # )
        info_embed.set_footer(text=f"Ticket ID: {ticket_data.ticket_id}")
        return info_embed

    elif current_ticket_status == "Ticket is closed":
        info_embed = discord.Embed(
            title=f"Ticket {ticket_data.ticket_id} information",
            description=f"""
                        **📢 Current status: {current_ticket_status}** 
                        **🙍 Open user:** <@{ticket_data.open_user_id}>
                        **🙍‍♂️ Close user:** <@{ticket_data.close_user_id}>
                        **💁 Claim user:** <@{ticket_data.claim_user_id}>
                        **❓ Ticket type:** <@{ticket_data.open_user_id}>
                        **🕑 Open time:** <t:{ticket_data.open_time}:F>
                        **🕑 Close time:** <t:{ticket_data.close_time}:F>
                        **🏠 Channel:** <#{ticket_data.channel_id}>""",
            colour=discord.Colour(int("5cb85c", 16)),
        )
        info_embed.add_field(
            name="Close reason",
            value=f"```{ticket_data.close_reason}```",
            inline=False,
        )
        info_embed.add_field(
            name="Transcript",
            value=f"[Open in browser]({private_api}/getTranscript/{ticket_data.ticket_id}?ticket_key={ticket_data.transcript_key})",
            inline=False,
        )
        # info_embed.add_field(
        #     name="Island Code (form)",
        #     value=f"```{ticket_data.form_island_code}```",
        #     inline=False,
        # )
        # info_embed.add_field(
        #     name="Build (form)", value=f"```{ticket_data.form_build}```", inline=False
        # )
        # info_embed.add_field(
        #     name="Payment (form)",
        #     value=f"```{ticket_data.form_payment}```",
        #     inline=False,
        # )
        info_embed.set_footer(text=f"Ticket ID: {ticket_data.ticket_id}")
        return info_embed
    elif current_ticket_status == "Failed":
        info_embed = discord.Embed(
            title=f"Ticket {ticket_data.ticket_id} information",
            description="Failed to get ticket data",
            colour=discord.Colour(int("d9534f", 16)),
        )
        info_embed.set_footer(text=f"Ticket ID: {ticket_data.ticket_id}")
        return info_embed