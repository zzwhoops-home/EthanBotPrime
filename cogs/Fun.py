from typing import Union
import nextcord
from nextcord.ext import tasks, commands

import random
import datetime
import asyncio
import requests
import json

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll", aliases=['dice', 'r'])
    async def roll(self, ctx, number=str(100)):
        try:
            if (str(float(number)) == number):
                await ctx.channel.send(f"You ever find a {number} sided die? Well, no, so give me an integer idiot")
                return
        except ValueError:
            await ctx.channel.send(f"You like... what... <:are_you_high:847849655990485002> I can't roll letters nincompoop")
            return

        roll = random.randint(0, int(number))
        await ctx.channel.send(f"Rolling **d{number}**...")
        await ctx.channel.send(f"You rolled **{roll:,}**.")

    @commands.command(name="rollbetween", aliases=['rb', 'dicebetween', 'db'])
    async def roll_between(self, ctx, start_number=str(0), end_number=str(100)):
        try:
            if (str(float(start_number)) == start_number):
                await ctx.channel.send(f"You ever find a {start_number} sided die? Well, no, so give me an integer idiot")
                return
            if (str(float(end_number)) == end_number):
                await ctx.channel.send(f"I can't roll {end_number}, give me an integer dumb dumb")
                return
            if (int(start_number) > int(end_number)):
                await ctx.channel.send(f"Your second number has to be lower than the first bozo. If you don't specify a second number, it defaults to 100.")
        except ValueError:
            await ctx.channel.send(f"You like... what... <:are_you_high:847849655990485002> I can't roll letters nincompoop")
            return

        roll = random.randint(int(start_number), int(end_number))
        await ctx.channel.send(f"Rolling between **{start_number}** and **{end_number}**...")
        await ctx.channel.send(f"You rolled **{roll:,}**.")

    @commands.command(name="flip", aliases=['coin', 'coinflip', 'cf'])
    async def flip(self, ctx):
        response = random.choice(["heads", "tails"])
        await ctx.channel.send(f"Your coin landed on **{response}**!")

    @commands.command(name="eliminate", aliases=["elim"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def eliminate(self, ctx, member: nextcord.Member = None):
        if (member == None):
            await ctx.channel.send("Hey you little shit I can't eliminate no one")
            return
        if (member.guild_permissions.administrator):
            await ctx.channel.send("https://i.pinimg.com/originals/0f/fd/29/0ffd29da68cc8176440779fcdb5b87bb.jpg")
            self.eliminate.reset_cooldown(ctx)
            return
        nick = member.display_name
        await ctx.channel.send(f'{member.mention} is a lil shit')
        await asyncio.sleep(1)
        await ctx.channel.send('lmao L get eliminated')
        await member.edit(nick="Eliminated")
        await asyncio.sleep(9)
        await ctx.channel.send('oh wait nvm, zzwhoops told me odro days are over.')
        await asyncio.sleep(3)
        await ctx.channel.send('sorry!')
        await asyncio.sleep(1)
        await member.edit(nick=nick)

        await ctx.message.delete()

    @commands.command(name="randomword", aliases=["random", "rword"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def random_word(self, ctx):
        req = requests.get("https://random-word-api.herokuapp.com/word?number=1")
        words = json.loads(req.text)
        word = random.choice(words)
        await ctx.channel.send(f"Your word is: {word}")

    @commands.command(name="wtf")
    @commands.cooldown(1, 25, commands.BucketType.user)
    async def navy_seal(self, ctx):
        text = "What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little \"clever\" comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo."
        await ctx.channel.send(text)
        
    @commands.command(name="mock")
    async def mock(self, ctx, *args):
        await ctx.channel.send("".join(random.choice((str.upper, str.lower))(char) for char in (" ".join(list(args))).lower().replace("c", "k")))

    @commands.command(name="uwu", aliases=["owo", "cringify"])
    async def uwu(self, ctx, *args):
        await ctx.channel.send((" ".join(list(args))).replace("r", "w").replace("R", "W").replace("n", "ny").replace("N", "NY").replace("l", "w").replace("L", "W"))

    @commands.command(name="vaporeon")
    async def vaporeon(self, ctx):
        text = "Hey guys, did you know that in terms of male human and female Pokémon breeding, Vaporeon is the most compatible Pokémon for humans? Not only are they in the field egg group, which is mostly comprised of mammals, Vaporeon are an average of 3”03’ tall and 63.9 pounds, this means they’re large enough to be able handle human dicks, and with their impressive Base Stats for HP and access to Acid Armor, you can be rough with one. Due to their mostly water based biology, there’s no doubt in my mind that an aroused Vaporeon would be incredibly wet, so wet that you could easily have sex with one for hours without getting sore. They can also learn the moves Attract, Baby-Doll Eyes, Captivate, Charm, and Tail Whip, along with not having fur to hide nipples, so it’d be incredibly easy for one to get you in the mood. With their abilities Water Absorb and Hydration, they can easily recover from fatigue with enough water. No other Pokémon comes close to this level of compatibility. Also, fun fact, if you pull out enough, you can make your Vaporeon turn white. Vaporeon is literally built for human dick. Ungodly defense stat+high HP pool+Acid Armor means it can take cock all day, all shapes and sizes and still come for more"
        await ctx.channel.send(text)

    @commands.command(name="WOOO", aliases=["WOO", "cocaine"])
    async def woo(self, ctx, number=2):
        if (number == 1):
            await ctx.channel.send("Well 'WHO' doesn't really make any sense, does it?")
            return
        if (number < 1):
            await ctx.channel.send("Enter a number greater than 1.")
            return
        if (number > 1990):
            await ctx.channel.send("You gonna buy me nitro or something? Enter a smaller number.")
            return
        await ctx.channel.send(f"W{'O' * number}")
    
    @commands.command(name="kill", aliases=["terminate", "makedie"])
    async def kill(self, ctx, member: Union[nextcord.Member, str]):
        responses = open('./kill_responses.txt', "r").read().split("\n")

        if (isinstance(member, nextcord.Member)):
            choice = random.randint(1, 2)
            if (choice == 1):
                await ctx.channel.send(f"{member.name} {random.choice(responses)}")
            elif (choice == 2):
                await ctx.channel.send(f"{member.name} {random.choice(responses)}")
        else:
            await ctx.channel.send(f"{member} {random.choice(responses)}")

    @commands.command(name="andify", aliases=["andy", "andeth"])
    async def andify(self, ctx, message: str, andethpower=5):
        try:
            andethpower = int(andethpower)
        except TypeError:
            await ctx.channel.send("Enter a number from 1 to 10 idiot")
            return
        except ValueError:
            await ctx.channel.send("Give me an integer asshole")
            return
        if (andethpower > 10 or andethpower < 1):
            await ctx.channel.send("Give me a power level between 1 and 10, dumbass")
            return

        words = message.split(" ")
        for x in range(len(words)):
            andeth = random.randint(1, 10)
            if andeth <= andethpower:
                words[x] = f"like {words[x]}"
        
        string = ""
        for word in words:
            string += f"{word} "

        if (len(string) > 1999):
            await ctx.channel.send("That exceeds character limits bitch")
            return

        await ctx.channel.send(string)

    @commands.command(name="unandify", aliases=["unandy", "unandeth"])
    async def unandify(self, ctx, message: str):
        words = message.split(" ")

        for x in range(len(words)):
            if words[x].lower() == "like":
                words[x] = f""
        
        string = " ".join([word for word in words if word])

        await ctx.channel.send(string)

    @commands.command(name="graduation", aliases=["GRADWHEN", "WHENGRAD", "grad"])
    async def graduation(self, ctx):
        now = datetime.datetime.now()
        graduation = datetime.datetime(2023, 6, 15, 12, 30, 00)

        duration = graduation - now

        seconds = duration.total_seconds()

        days, remainder = divmod(seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        description = f"**{days:.0f}** days, **{hours:.0f}** hours, **{minutes:.0f}** minutes, **{seconds:.0f}** seconds until graduation on **June 15th, 2023** at **12:30 PM**!!!\n"

        seconds = duration.total_seconds()

        weeks = seconds / 604800
        days = seconds / 86400
        hours = seconds / 3600
        minutes = seconds / 60

        title = "Countdown until graduation:"
        description += f"\n__**That is:**__\n\n**{weeks:,.2f}** weeks\n**{days:,.2f}** days\n**{hours:,.2f}** hours\n**{minutes:,.0f}** minutes\n**{seconds:,.0f}** seconds"

        embed = nextcord.Embed(title=title, description=description)

        await ctx.channel.send(embed=embed)


    @commands.command(name="OHGODSITHINKWEAREHAVINGANOTHERFROLIGARCHYARGUMENTPLEASEMAKEITSTOP", aliases=["CODESHITSTORMIREPEATCODESHITSTORMWEAREINNEEDOFADEFUSAL"])
    @commands.cooldown(1, 25, commands.BucketType.user)
    async def oh_gods(self, ctx):
        text = "​\n" * 998
        for x in range(10):
            await ctx.channel.send(text)