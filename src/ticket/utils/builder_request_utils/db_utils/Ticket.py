class Ticket:
    def __init__(
        self,
        ticket_id,
        ticket_type,
        open_user_id,
        open_time,
        open_reason,
        form_name,
        form_roblox_user,
        form_island_code,
        form_build,
        form_build_desp,
        form_build_img,
        form_payment,
        channel_id,
        welcome_msg_id,
        dm_msg_id,
        confirm_message_id,
        queue_msg_id,
        log_msg_id,
        transcript_key,
        claim_user_id,
        close_user_id,
        close_time,
        close_reason
    ):
        self.ticket_id = ticket_id
        self.ticket_type = ticket_type
        self.open_user_id = open_user_id
        self.open_time = open_time
        self.open_reason = open_reason
        self.form_name = form_name
        self.form_roblox_user = form_roblox_user
        self.form_island_code = form_island_code
        self.form_build = form_build
        self.form_build_desp = form_build_desp
        self.form_build_img = form_build_img
        self.form_payment = form_payment
        self.channel_id = channel_id
        self.welcome_msg_id = welcome_msg_id
        self.dm_msg_id = dm_msg_id
        self.confirm_message_id = confirm_message_id
        self.queue_msg_id = queue_msg_id
        self.log_msg_id = log_msg_id
        self.transcript_key = transcript_key
        self.claim_user_id = claim_user_id
        self.close_user_id = close_user_id
        self.close_time = close_time
        self.close_reason = close_reason

    def __repr__(self):
        return f"<Ticket(ticket_id={self.ticket_id}, ticket_type={self.ticket_type})>"

    def __str__(self):
        return (
            f"Ticket ID: {self.ticket_id}\n"
            f"Ticket Type: {self.ticket_type}\n"
            f"Open User ID: {self.open_user_id}\n"
            f"Open Time: {self.open_time}\n"
            f"Open Reason: {self.open_reason}\n"
            f"Form Name: {self.form_name}\n"
            f"Form Roblox User: {self.form_roblox_user}\n"
            f"Form Island Code: {self.form_island_code}\n"
            f"Form Build: {self.form_build}\n"
            f"Form Build Description: {self.form_build_desp}\n"
            f"Form Build Image: {self.form_build_img}\n"
            f"Form Payment: {self.form_payment}\n"
            f"Channel ID: {self.channel_id}\n"
            f"Welcome Message ID: {self.welcome_msg_id}\n"
            f"DM Message ID: {self.dm_msg_id}\n"
            f"Confirm Message ID: {self.confirm_message_id}\n"
            f"Queue Message ID: {self.queue_msg_id}\n"
            f"Log Message ID: {self.log_msg_id}\n"
            f"Transcript Key: {self.transcript_key}\n"
            f"Claim User ID: {self.claim_user_id}\n"
            f"Close User ID: {self.close_user_id}\n"
            f"Close Time: {self.close_time}\n"
            f"Close Reason: {self.close_reason}"
        )
