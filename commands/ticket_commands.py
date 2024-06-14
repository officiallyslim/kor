import discord
from commands.ticket_cmd_group.ticket_remove import remove_user_ticket
from commands.ticket_cmd_group.ticket_close import close_ticket
from discord import option

ticket_group = discord.SlashCommandGroup("ticket", "Ticket utils command")


ticket_group.command(
    name="remove", description="Remove someone to the current ticket channel"
)(remove_user_ticket)

ticket_group.command(name="close", description="Close the ticket")(
    option("close_reason", description="Close ticket reason")(
        option(
            "ticket_id",
            description="The ID of the ticket you want to close",
            default=None,
        )(
            option(
                "password",
                description="Close the ticket even if it's claimed",
                default=None,
            )(close_ticket)
        )
    )
)
