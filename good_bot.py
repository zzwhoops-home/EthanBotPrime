# bot.py
import os
import random
import asyncio
import datetime
import time
import math
import pymongo
from pymongo import MongoClient
from pprint import pprint

import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
USER = os.getenv('USER')
PWD = os.getenv('PWD')

guild = None
intents = discord.Intents.default()
intents.members = True

prefix = "eb!"
bot = commands.Bot(command_prefix=prefix, intents=intents)
perms = discord.Permissions()

client = MongoClient(f"mongodb+srv://{USER}:{PWD}@ethanbotdb.jiyrt.mongodb.net/EthanBotDB")
db=client.bot_data

ethan_tokens = db.ethan_tokens

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})\n'
    )

@bot.command(name="set")
@commands.cooldown(1, 3, commands.BucketType.user)
async def set_balance(ctx, currency, member: discord.Member, amount):
    amount = round(float(str(amount).replace(",","")), 2)
    limit = 1000000
    types = ["tokens", "coins"]

    if (ctx.author.id != 390601966423900162):
        await ctx.channel.send("Only Ethan can use this dumbass")
        return
    if (currency not in types):
        await ctx.channel.send("Kid you gotta say 'tokens' or 'coins' so I know which to add")
        return
    if (abs(amount) > limit):
        await ctx.channel.send(f"Hey, you tryna devalue Ethan currencies?\nEnter a number between {-limit:,} and {limit:,}.")
        return

    id = member.id
    existing = ethan_tokens.find_one({"id": id})
    if existing == None:
        await ctx.channel.send(f"Records not found... creating account for {member.mention}.")
        data = {
            "id": id,
            "name": f"{member.name}#{member.discriminator}",
            "tokens": 0.00,
            "coins": 0.00
        }
        await asyncio.sleep(2)
        await ctx.channel.send(f"Account created!")
        if (currency == "tokens"):
            data["tokens"] = amount
            symbol = "<:ethanger:763411726741143572>"
        if (currency == "coins"):
            data["coins"] = amount
            symbol = "<:ethoggers:868201785301561394>"
        ethan_tokens.insert_one(data)        
        await ctx.channel.send(f"Okay, {member.mention} now has **{amount:,.2f}** {symbol}.")
    else:
        query = {
            "id": id
        }
        if (currency == "tokens"):
            cur_balance = existing["tokens"]
            new_balance = amount
            data = {
                "$set":
                {
                    "name": member.name,
                    "tokens": new_balance
                }
            }
            ethan_tokens.update_one(query, data)
        if (currency == "coins"):
            cur_balance = existing["coins"]
            new_balance = amount
            data = {
                "$set":
                {
                    "name": f"{member.name}#{member.discriminator}",
                    "coins": new_balance
                }
            }
            ethan_tokens.update_one(query, data)        
        if currency == "tokens":
            currency = "<:ethanger:763411726741143572>"
        elif currency == "coins":
            currency = "<:ethoggers:868201785301561394>"

        await ctx.channel.send(f"Okay, {member.mention} now has **{amount:,.2f}** {currency}.")

@bot.command(name="edit", aliases=["add"])
@commands.cooldown(1, 3, commands.BucketType.user)
async def edit_balance(ctx, currency, member: discord.Member, amount):
    amount = round(float(str(amount).replace(",","")), 2)
    limit = 10000
    types = ["tokens", "coins"]

    if (ctx.author.id != 390601966423900162):
        await ctx.channel.send("Only Ethan can use this dumbass")
        return
    if (currency not in types):
        await ctx.channel.send("Kid you gotta say 'tokens' or 'coins' so I know which to add")
        return
    if (abs(amount) > limit):
        await ctx.channel.send(f"Hey, you tryna cause hyperinflation or something dumbass?\nEnter a number between {-limit:,} and {limit:,}.")
        return

    id = member.id
    existing = ethan_tokens.find_one({"id": id})
    if existing == None:
        await ctx.channel.send(f"Records not found... creating account for {member.mention}.")
        data = {
            "id": id,
            "name": f"{member.name}#{member.discriminator}",
            "tokens": 0.00,
            "coins": 0.00
        }
        await asyncio.sleep(2)
        await ctx.channel.send(f"Account created!")
        if (currency == "tokens"):
            data["tokens"] = amount
            symbol = "<:ethanger:763411726741143572>"
        if (currency == "coins"):
            data["coins"] = amount
            symbol = "<:ethoggers:868201785301561394>"
        ethan_tokens.insert_one(data)        
        await ctx.channel.send(f"Okay, {member.mention} now has **{amount:,.2f}** {symbol}")
    else:
        query = {
            "id": id
        }
        if (currency == "tokens"):
            cur_balance = existing["tokens"]
            new_balance = cur_balance + amount
            data = {
                "$set":
                {
                    "name": f"{member.name}#{member.discriminator}",
                    "tokens": new_balance
                }
            }
            ethan_tokens.update_one(query, data)
        if (currency == "coins"):
            cur_balance = existing["coins"]
            new_balance = cur_balance + amount
            data = {
                "$set":
                {
                    "name": f"{member.name}#{member.discriminator}",
                    "coins": new_balance
                }
            }
            ethan_tokens.update_one(query, data)
        if currency == "tokens":
            symbol = "<:ethanger:763411726741143572>"
        elif currency == "coins":
            symbol = "<:ethoggers:868201785301561394>"

        if (amount < 0):
            await ctx.channel.send(f"Okay, I've taken **{amount:,.2f}** {symbol} from {member.mention}.\nThey now have **{new_balance:,.2f}** {symbol}.")
        else:
            await ctx.channel.send(f"Okay, I've added **{amount:,.2f}** {symbol} to {member.mention}.\nThey now have **{new_balance:,.2f}** {symbol}.")

@bot.command(name="balance", aliases=["bal"])
async def view_balance(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    
    id = member.id
    existing = ethan_tokens.find_one({"id": id})
    tokens = 0.00
    coins = 0.00
    if existing == None:
        await ctx.channel.send(f"Records not found... creating account for {member.mention}.")
        data = {
            "id": id,
            "name": f"{member.name}#{member.discriminator}",
            "tokens": tokens,
            "coins": coins
        }
        await asyncio.sleep(2)
        await ctx.channel.send(f"Account created!")
        ethan_tokens.insert_one(data)
    else:
        tokens = f"{existing['tokens']:,.2f}"
        coins = f"{existing['coins']:,.2f}"

    embed = discord.Embed(title=f"{member.name}'s EthanBalance:tm:")
    embed.add_field(name="<:ethanger:763411726741143572> (ET)", value=tokens, inline=True)        
    embed.add_field(name="<:ethoggers:868201785301561394> (EC)", value=coins, inline=True)
    await ctx.channel.send(embed=embed)

@bot.command(name="leaderboard", aliases=["top", "rich"])
@commands.cooldown(1, 3, commands.BucketType.user)
async def leaderboard(ctx, currency = ""):
    member = ctx.author
    types = ["tokens", "coins"]
    if currency not in types:
        await ctx.channel.send("You have to specify either 'tokens' or 'coins', dimwit")
        return
    
    description = ""
    count = 0
    if currency == "tokens":
        accounts = ethan_tokens.find().sort("tokens", pymongo.DESCENDING).limit(7)
        for account in accounts:
            if (account['name'] == f"{member.name}#{member.discriminator}"):
                is_user = "***"
            else:
                is_user = ""
            if (account['tokens'] == 0):
                break
            count += 1
            description += f"**#{count}**: `{account['tokens']:,.2f}`<:ethanger:763411726741143572> - {is_user}{account['name']}{is_user}\n"
    elif currency == "coins":
        accounts = ethan_tokens.find().sort("coins", pymongo.DESCENDING).limit(7)
        for account in accounts:
            if (account['name'] == f"{member.name}#{member.discriminator}"):
                is_user = "***"
            else:
                is_user = ""
            if (account['coins'] == 0):
                break
            count += 1
            description += f"**#{count}**: `{account['coins']:,.2f}`<:ethoggers:868201785301561394> - {is_user}{account['name']}{is_user}\n"

    embed = discord.Embed(title=f"{ctx.guild.name}'s {currency.capitalize()} Leaderboard", description=description)
    await ctx.channel.send(embed=embed)   

@bot.command(name="roll", aliases=['dice', 'r'])
async def roll(ctx, number=str(100)):
    try:
        if (str(float(number)) == number):
            await ctx.channel.send(f"You ever find a {number} sided die? Well, no, so give me an integer idiot")
            return
    except ValueError:
        await ctx.channel.send(f"You like... fucking... <:are_you_high:847849655990485002> I can't roll letters nincompoop")

    roll = random.randint(0, int(number))
    await ctx.channel.send(f"Rolling **d{number}**...")
    await ctx.channel.send(f"You rolled **{roll:,}**.")

async def activate_pp():
    await bot.wait_until_ready()
    guild = bot.get_guild(423583970328838154)
    channel = guild.get_channel(866168036770578432)
    created = datetime.datetime.utcnow()
    await channel.send(f"<@&652326925800570880> {prefix}pp")
    await asyncio.sleep(7200)
    await channel.send("**-=-=- FROLIGARCHY FOR THE DAY HAS CLOSED. -=-=-**")

    now_utc = datetime.datetime.utcnow()
    messages = await channel.history(limit=None, before=now_utc, after=created).flatten()
    pps = {}
    for msg in messages:
        if (msg.author.id != bot.user.id):
            continue
        embeds = msg.embeds
        if embeds == []:
            continue
        for embed in embeds:
            footer = str(embed.footer.text)
            if (footer not in pps) or len(pps) == 0:
                cur = embed.description.split("\n")
                pps[footer] = str(cur[1]).count("=")
    pps = dict(sorted(pps.items(), key=lambda item: item[1], reverse=True))
    description = ""
    count = 0
    units = random.choice(["cm", "mm", "m", "in", "ft", "yd"])
    for key, value in pps.items():
        count += 1
        text = f"**({count}).** "
        if (count <= 2):
            text += "<:poggies:826811320073453598> **FROLIGARCH** "
        member = guild.get_member(int(key))
        text += f"**{member.name}**: {value} {units}\n"
        description += text
            
    if len(pps.items()) == 0:
        description = f"xd yall suck, not even a single pp. Fuckin disgracing the Glorious Froligarchy."

    embed = discord.Embed(title="LEADERBOARD FOR TODAY", url="https://www.youtube.com/watch?v=iik25wqIuFo", description=description)
    await channel.send(embed=embed)
    await remove_froligarchs(guild)
    await add_froligarchs(guild, list(pps.items())[:2])

WHEN = datetime.time(20, 00, 00)
async def pping():
    while True:
        now = datetime.datetime.utcnow() # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
        target_time = datetime.datetime.combine(now.date(), WHEN)  # 6:00 PM today (In UTC)
        seconds_until_target = -1
        if (seconds_until_target < 0):
            target_time = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), datetime.time(second=1))
            seconds_until_target = (target_time - now).total_seconds()
        print(f"Seconds until target: {seconds_until_target}")
        await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
        await activate_pp()  # Call the helper function that sends the message
        tomorrow = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), datetime.time(second=1))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        print(f"Seconds until tmr: {seconds}")
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start a new iteration

async def add_froligarchs(guild, members):
    role = guild.get_role(841482931255115816)
    for member in members:
        frog = guild.get_member(int(member[0]))
        await frog.add_roles(role)

async def remove_froligarchs(guild):
    role = guild.get_role(841482931255115816)
    role_members = role.members
    for member in role_members:
        await member.remove_roles(role)

@bot.command(name='pp')
async def egadpp(ctx):
    def peepee():
        length = random.randint(0, 15)
        return length

    title = "peepee size machine"
    count = peepee()
    description = f"{ctx.message.author.name}'s penis\n8{('=' * count)}D ({count})"
    embed=discord.Embed(title=title, url="https://www.youtube.com/watch?v=iik25wqIuFo", description=description)
    embed.set_footer(text=f"{ctx.message.author.id}")
    await ctx.send(embed=embed)

@bot.command(name="STIFFCOCKS", aliases=["SC", "SCOCKS"])
@commands.cooldown(1, 45, commands.BucketType.guild)
async def stiff_cocks(ctx, num=100):
    limit = 500
    if (num <= 0):
        await ctx.channel.send(f"Enter a number between 1 and {limit}, dumbass. Victory doesn't come *that* easy.")
        return
    elif (num >= limit):
        await ctx.channel.send(f"I will leak my nudes if you somehow get over {limit}. Pick another number, shitstick!")
        return

    stiff_cocks.stop = False

    async def timer(ctx):
        await asyncio.sleep(30)
        stiff_cocks.stop = True

    async def counter(ctx):
        count = 0
        users = []
        while True:
            if (stiff_cocks.stop == True):
                break
            try:
                msg = await bot.wait_for("message", check=check, timeout=5.0)
                if (msg.author.name not in users):
                    users.append(msg.author.name)
                count += 1
                print(count)
            except asyncio.TimeoutError:
                print("timeout")
                
        await ctx.channel.send("Tallying stiff cocks...")
        await asyncio.sleep(3)
        success = num
        await ctx.channel.send(f"Messages: {count}/{success}\nUsers Participated: {len(users)}")
        await asyncio.sleep(2)

        if (int(count) >= int(success)):
            embed=discord.Embed(description="LMAO YOUR DID IT BUT YOU GET ABSOLUTELY NOTHING DONUT!!!\nEthanBot IS PLEASED TO WASTE YOUR TIME")
            await ctx.channel.send(embed=embed)
            await ctx.channel.send("https://ih1.redbubble.net/image.724682828.9041/flat,1000x1000,075,f.jpg")
        else:
            await ctx.channel.send("you tried lmao you suck\n**YOU SUCK SKILL ISSUE LMAO**")
            await ctx.channel.send("https://imgur.com/a/vlkjkxv")

    def check(m):
        return (
            m.content.strip() == "STIFF COCKS"
            and m.channel.id == ctx.channel.id
        )

    embed=discord.Embed(title="I LOVE STIFF COCKS. PREPARE TO SEND 'STIFF COCKS' FOR 30 SECONDS", description=f"Goal: {num}")
    await ctx.channel.send(embed=embed)

    delay = 5
    for x in range(delay):
        await asyncio.sleep(1)
        await ctx.channel.send(str(delay - x))

    await asyncio.sleep(1)
    await ctx.channel.send("**-=-=- GO -=-=-**")

    tally = asyncio.create_task(counter(ctx))
    wait = asyncio.create_task(timer(ctx))

    await tally
    await wait

@bot.command(name="ELIMINATE", aliases=["eliminate", "elim", "ELIM"])
@commands.cooldown(1, 30, commands.BucketType.user)
async def eliminate(ctx, member: discord.Member):
    if (member.guild_permissions.administrator):
        await ctx.channel.send("https://i.pinimg.com/originals/0f/fd/29/0ffd29da68cc8176440779fcdb5b87bb.jpg")
        return
    nick = member.display_name
    await ctx.channel.send(f'{member.mention} is a lil shit')
    await asyncio.sleep(1)
    await ctx.channel.send('lmao fuck u get eliminated')
    await member.edit(nick="Eliminated")
    await asyncio.sleep(9)
    await ctx.channel.send('oh wait nvm, zzwhoops told me not to hurt anyone')
    await asyncio.sleep(3)
    await ctx.channel.send('sorry!')
    await asyncio.sleep(1)
    await member.edit(nick=nick)

    await ctx.message.delete()

@bot.event
async def on_message(message):
    if (message.content[:5].strip() == prefix):
        return
    if (bot.user.id != message.author.id):
        msg = message.content.strip().lower()
        if 'ethan' in msg and message.channel.id != 765710257753948190:
            await message.channel.send("sex")
        if 'connor' in msg:
            await message.channel.send("ethan sex")
        if 'edge' in msg and 'play' in msg:
            await message.channel.send("ethedge ethplay ethgasm")
        if 'higgy' in msg:
            await message.channel.send("ethan be gettin' real jiggy")
        if 'sam' in msg and ('sister' in msg or 'fisher' in msg):
            await message.channel.send("<:sexualrelations:803707185963991081>")
        if msg == 'ethan\'s insane announcement' and (message.channel.id == 765710257753948190):
            await message.channel.send("ethan's insane announcement")
        if 'china' in msg:
            await message.channel.send("荣耀归于中国")
        if 'egg' in msg:
            await message.channel.send("egg")
    if (message.author.id == 292448459909365760):
        if 'sad' in message.content.strip().lower():
            await message.channel.send("<:zzwhoops_cries:813585484441714698>")
    if (message.author.id == 390601966423900162):
        if 'scribbles notes' in message.content:
            await message.channel.send("https://tenor.com/bi7Db.gif")
    if (message.author.id == 501505695091392527):
        if 'sister' in message.content:
            await message.channel.send("<:sexualrelations:803707185963991081>")

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.channel.send(f"Stop spamming me you dolt: try again in {round(error.retry_after, 2)}sec.", delete_after=4)
    else:
        print(error)


bot.loop.create_task(pping())
bot.run(TOKEN)