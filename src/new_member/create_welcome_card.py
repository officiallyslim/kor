import discord
from config import bot, default_pfp_path, pfp_img_path, background_img_path, welcome_img_folder_path, welcome_channel_id, new_members_log_channel_id
from easy_pil import Canvas, Editor, Font, Text, font
import requests

async def create_welcome_card(member: discord.Member):
    if member.avatar is None:
        avatar_path = default_pfp_path
    else:
        avatar_url = str(member.avatar.url)
        response = requests.get(avatar_url)
        with open(pfp_img_path, 'wb') as file:
            file.write(response.content)
        avatar_path = pfp_img_path
    
    background = Editor(Canvas((900, 240), "#23272a"))
    profile = Editor(avatar_path).resize((200, 200)).circle_image()

    poppins_big = Font.poppins(variant="bold", size=65)
    poppins_mediam = Font.poppins(variant="bold", size=38)
    poppins_thin = Font.poppins(variant="bold", size=18)

    custom_background = Editor(background_img_path)
    custom_background = Editor(background_img_path).resize((1100, 600))
    background.paste(custom_background, (-20, -170))
    background.rectangle((290,150),width=550, height=3, fill="white", radius=20)

    background.paste(profile, (20, 18))
    background.ellipse((20, 18), 200, 200, outline="white", stroke_width=2)

    background.text((555, 45), "WELCOME TO", font=poppins_big, color="white", align="center")
    background.text((555, 110), "BOOM BUILDING CORPORATION", font=poppins_mediam, color="white", align="center", stroke_width=0, stroke_fill="blue")
    background.text((860, 109), "!", font=poppins_mediam, color="white", align="center")
    background.text((652, 216), "discord.gg/boombuilding", font=poppins_thin, color="#8b8b8b", align="left", stroke_width=0, stroke_fill="white")

    background.text((560, 165), "Build everything imaginable", font=poppins_thin, color="white", align="center")

    member_name = member.name
    welcome_img_path = welcome_img_folder_path + member_name + "_welcome.png"

    background.save(welcome_img_path)
    await send_welcome_message(member, welcome_img_path)
    return welcome_img_path

async def send_welcome_message(member: discord.Member, welcome_img_path):
    welcome_channel = bot.get_channel(welcome_channel_id)
    await welcome_channel.send(content=f"Welcome {member.mention} to **BOOM BUILDING CORPORATION**!", file=discord.File(welcome_img_path))

async def send_welcome_message_and_DM(member: discord.Member, welcome_img_path):
    welcome_channel = bot.get_channel(welcome_channel_id)
    log_channel = bot.get_channel(new_members_log_channel_id)

    await welcome_channel.send(content=f"Welcome {member.mention} to **BOOM BUILDING CORPORATION**!", file=discord.File(welcome_img_path))
    try:    
        dm = await member.create_dm()
        await dm.send(content=f"## Welcome <@{member.id}> to **Boom Building Corporation**!\nThank you for joining and we hope you enjoy your stay.\nBefore start chatting, please keep a few things in mind:\n\n- Respect the server rules: <#1151613289537748992>\n- Wanna become a builder? Apply here: <#1151613313432703087>!\n- Need builds? Open a designated build ticket here: <#1153416115414892634>!\n\nAnd we hope you enjoy your experience with us! Ciao!", file=discord.File(welcome_img_path), view=fromserver())
    except discord.Forbidden:
        await log_channel.send(content=f"Failed send welcome message to {member.mention}")

class fromserver(discord.ui.View):
    @discord.ui.button(label="Sent from BOOM BUILDING CORPORATION", style=discord.ButtonStyle.secondary, disabled=True)
    async def button_callback(self, button, interaction):
        pass