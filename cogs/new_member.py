from config import *

class new_member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.Cog.listener()
    async def on_member_join(self, member):
        await self.assign_roles(member)
        await self.create_welcome_card(member)
        await self.send_welcome_message(member)


    async def assign_roles(self, member):
        log_channel = bot.get_channel(log_channel_id)

        print(f"{member} joined")
        role1 = discord.utils.get(member.guild.roles, id=1125431114798989352)
        role2 = discord.utils.get(member.guild.roles, id=1125430088628961440)
        role3 = discord.utils.get(member.guild.roles, id=1125420722983018577)
        role4 = discord.utils.get(member.guild.roles, id=1125524962640408718)

        max_attempts = 10
        attempts = 0
        while attempts < max_attempts:
            await member.add_roles(role1, role2, role3,role4)

            # Verificar si los roles se han añadido correctamente
            if role1 in member.roles and role2 in member.roles and role3 in member.roles and role4 in member.roles:
                await log_channel.send(f"Roles 1, 2, 3 and 4 were assigned to {member} ({member.mention})")
                break
            else:
                attempts += 1

        if attempts == max_attempts:
            await log_channel.send(f"<@&1147506414110126190>\nCould not assign all roles to {member} after {max_attempts} attempts")

    async def create_welcome_card(self, member):
        if member.avatar is None:
            avatar_path = default_pfp
        else:
            avatar_url = str(member.avatar.url)
            response = requests.get(avatar_url)
            with open(pfp_img, 'wb') as file:
                file.write(response.content)
            avatar_path = pfp_img
        
        background = Editor(Canvas((900, 240), "#23272a"))
        profile = Editor(avatar_path).resize((200, 200)).circle_image()

        poppins_big = Font.poppins(variant="bold", size=65)
        poppins_mediam = Font.poppins(variant="bold", size=38)
        poppins_thin = Font.poppins(variant="bold", size=18)

        card_left_shape = [(0, 0), (0, 270), (330, 270), (260, 0)]

        custom_background = Editor(background_img)
        custom_background = Editor(background_img).resize((900, 506))
        background.paste(custom_background, (100, -250))
        background.polygon(card_left_shape, (0, 0, 0, 0))
        background.rectangle((350,175),width=500, height=3, fill="cyan", radius=20)

        background.paste(profile, (40, 18))
        background.ellipse((40, 18), 200, 200, outline="cyan", stroke_width=5)

        background.text((600, 70), "WELCOME", font=poppins_big, color="cyan", align="center")
        background.text((600, 130), "to BestGamez Discord Server!", font=poppins_mediam, color="cyan", align="center")

        background.text((600, 190), "THANK YOU FOR JOINING. WE HOPE YOU ENJOY YOUR STAY!", font=poppins_thin, color="cyan", align="center")

        background.save(welcome_img)

    async def send_welcome_message(self, member):
        welcome_channel = bot.get_channel(welcome_channel_id)
        log_channel = bot.get_channel(log_channel_id)

        await welcome_channel.send(file=discord.File(welcome_img))
        try:
            dm = await member.create_dm()
            await dm.send(content=f"## Welcome {member.mention} to the **Official BestGamez Discord server**!\nThank you for joining and we hope you enjoy your stay.\nBefore start chatting, please keep a few things in mind:\n\n- Respect the server rules: <#934367707212677150>\n- Verify before chatting: <#1147839409278963794>\n- Looking for server information? Find  it here: <#1141740532553502720>!\n- Need help? Open ticket now: <#1136261793535246446>", file=discord.File(welcome_img), view=frombest())
        except discord.Forbidden:
            await log_channel.send(content=f"Failed send welcome message to {member.mention}")


def setup(bot):
    bot.add_cog(new_member(bot))

class frombest(discord.ui.View):
    @discord.ui.button(label="Sent from BestGamez Server", style=discord.ButtonStyle.secondary, disabled=True)
    async def button_callback(self, button, interaction):
        pass