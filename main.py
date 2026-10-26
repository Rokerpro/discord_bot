import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
from datetime import timedelta

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.bans = True
intents.emojis = True
intents.integrations = True
intents.webhooks = True
intents.invites = True
intents.voice_states = True
intents.guilds = True
intents.guild_messages = True
intents.guild_reactions = True
intents.typing = True

bot = commands.Bot(command_prefix='!', intents=intents)

role_ = "Admin"
banned_words = ["book"]


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"{member.name} has left the server")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    for word in banned_words:
        if word in message.content.lower():
            await message.delete()
            await message.channel.send(f"{message.author.mention} dont use that kind of words")
            return

    await bot.process_commands(message)

@bot.command()
async  def hello(ctx):
    await ctx.send(f"Hello! {ctx.author.mention}")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=role_)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} has been assigned {role_}")
    else:
        await ctx.send(f"Role not found")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=role_)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has been removed from {role_}")
    else:
        await ctx.send(f"Role not found")

@bot.command()
async def dm(ctx, *, message):
    try:
        await ctx.author.send(message)
        await ctx.send("✅ DM sent!")
    except discord.Forbidden:
        await ctx.send("❌ I couldn't send you a DM. Please check if you have DMs enabled from server members.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")


@bot.command()
@commands.has_role(role_)
async def secret(ctx):
    await ctx.send("This is a secret command")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You don't have the required role")




@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def roll(ctx, sides: int = 6):
    if sides < 2:
        await ctx.send("❌ A dice needs at least 2 sides")
        return
    await ctx.send(f"🎲 {ctx.author.mention} rolled a {random.randint(1, sides)} (1-{sides})")

@bot.command()
async def coinflip(ctx):
    await ctx.send(f"🪙 {random.choice(['Heads', 'Tails'])}")

@bot.command(name="8ball")
async def eight_ball(ctx, *, question):
    answers = ["Yes", "No", "Maybe", "Definitely", "Ask again later", "I don't think so"]
    await ctx.send(f"🎱 {random.choice(answers)}")

@bot.command()
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name}'s avatar")
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)




@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name}'s info")
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Joined server", value=member.joined_at.strftime("%d %b %Y"))
    embed.add_field(name="Account created", value=member.created_at.strftime("%d %b %Y"))
    embed.add_field(name="Top role", value=member.top_role.name)
    embed.set_thumbnail(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=guild.name)
    embed.add_field(name="Members", value=guild.member_count)
    embed.add_field(name="Channels", value=len(guild.channels))
    embed.add_field(name="Roles", value=len(guild.roles))
    embed.add_field(name="Created", value=guild.created_at.strftime("%d %b %Y"))
    await ctx.send(embed=embed)




@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Deleted {amount} messages", delete_after=3)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to delete messages")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason given"):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.name} has been kicked. Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to kick that member")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to kick members")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Member not found")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason given"):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.name} has been banned. Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to ban that member")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to ban members")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Member not found")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int = 5):
    try:
        await member.timeout(timedelta(minutes=minutes))
        await ctx.send(f"🔇 {member.name} has been timed out for {minutes} minutes")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to timeout that member")

@timeout.error
async def timeout_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to timeout members")

@bot.command()
@commands.has_role(role_)
async def announce(ctx, *, message):
    embed = discord.Embed(title="📢 Announcement", description=message)
    embed.set_footer(text=f"By {ctx.author.name}")
    await ctx.send(embed=embed)

@announce.error
async def announce_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You don't have the required role")




@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument: {error.param.name}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Invalid argument")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)