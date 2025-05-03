import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN') #gets the bot token from mthe .env file

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') # will create a log file to see the bot log
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

bot = commands.Bot(command_prefix='!', intents=intents) #you may change the prifix to your liking

role_ = "Admin"

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "shit" in message.content.lower(): #if the pertifular word in "" is said then it is removed and a waring msg is sent you may as well link a file to it
        await message.delete()
        await message.channel.send(f"{message.author.mention} dont use that kind of words")

    await bot.process_commands(message) # as we are overwrithing the already existing command in discord

@bot.command()
async  def hello(ctx): #sends the hello msg
    await ctx.send(f"Hello! {ctx.author.mention}")

@bot.command()
async def assign(ctx): #assigns the role (for now admin as stored in role_ variable)
    role = discord.utils.get(ctx.guild.roles, name=role_)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} has been assigned {role_}")
    else:
        await ctx.send(f"Role not found")

@bot.command()
async def remove(ctx): #removes the role_ role
    role = discord.utils.get(ctx.guild.roles, name=role_)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has been removed from {role_}")
    else:
        await ctx.send(f"Role not found")
@bot.command()
async def dm(ctx, *, message): # send the dm and if dm could not be send or the user's dm is forbiddened then it will show an error
    try:
        await ctx.author.send(message)
        await ctx.send("✅ DM sent!")
    except discord.Forbidden:
        await ctx.send("❌ I couldn't send you a DM. Please check if you have DMs enabled from server members.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command()
async def reply(ctx): #replys to your msg
    await ctx.reply("This is a reply")

@bot.command()
async def poll(ctx, *, question): #create a poll (more like a enbaed msg)
    embed = discord.Embed(title="Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")


@bot.command()
@commands.has_role(role_) #if the author has a specific role then the msg will be sent
async def secret(ctx):
    await ctx.send("This is a secret command")

@secret.error
async def secret_error(ctx, error): # if the author is missing the role then this msg will come
    if isinstance(error, commands.MissingRole):
        await ctx.send("You don't have the required role")


bot.run(token, log_handler=handler, log_level=logging.DEBUG) #where bot runs
