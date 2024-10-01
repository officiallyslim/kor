import discord
from commands.ticket_cmd_group.ticket_claim import claim_ticket_cmd
from commands.ticket_cmd_group.ticket_unclaim import unclaim_ticket_cmd
from commands.ticket_cmd_group.ticket_remove import remove_user_ticket
from commands.ticket_cmd_group.ticket_close import close_ticket
from commands.ticket_cmd_group.ticket_add import add_user_ticket
from commands.ticket_cmd_group.ticket_info import view_ticket_info_callback
from discord import option

ticket_group = discord.SlashCommandGroup("ticket", "Ticket utils command")


ticket_group.command(
    name="remove", description="Remove someone to the current ticket channel"
)(remove_user_ticket)

ticket_group.command(name="close", description="Close the ticket")(
    option("close_reason", description="Close ticket reason")(
    option("ticket_id", description="The ID of the ticket you want to close", default=None,)(
    option("password", description="Close the ticket even if it's claimed", default=None,)
    (close_ticket))))

ticket_group.command(
    name="add", description="Add someone to the current ticket channel"
)(add_user_ticket)

ticket_group.command(
    name="info", description="View specific information")(
    option("ticket_id", description="The ticket ID for view information", default=None)
    (view_ticket_info_callback))

ticket_group.command(
    name="claim", description="Claim the current ticket channel"
)(claim_ticket_cmd)

ticket_group.command(
    name="unclaim", description="Unclaim the current ticket channel"
)(unclaim_ticket_cmd)
