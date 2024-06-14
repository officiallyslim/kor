import discord
from commands.ticket_cmd_group.ticket_remove import remove_user_ticket

ticket_group = discord.SlashCommandGroup("ticket", "Ticket utils command")


ticket_group.command(
    name="remove", description="Remove someone to the current ticket channel"
)(remove_user_ticket)
