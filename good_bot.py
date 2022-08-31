# bot.py
import json
import os
import random
import asyncio
from datetime import datetime, timedelta, time, timezone
import math
import pymongo
from pymongo import MongoClient
import requests

import nextcord
from nextcord import SelectOption, ButtonStyle
from nextcord.ext import tasks, commands
from nextcord.interactions import Interaction, InteractionResponse
from nextcord.ui import button, View, Button, Select, TextInput, Modal

from cogs.Listeners import Listeners
from cogs.Ethan import Ethan
from cogs.Economy import Economy
from cogs.Gambling import Gambling

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
USER = os.getenv('USER')
PWD = os.getenv('PWD')

STOCKS_API_KEY = os.getenv("YAHOO_API_KEY")

# pping:
PP_START = time(20, 00, 00)
PP_END = time(22, 00, 00)

guild = None
intents = nextcord.Intents.all()
intents.members = True
prefix = "eb!"

class EthanBot(commands.Bot):
    def __init__(self, case_insensitive, command_prefix, intents):
        super().__init__(case_insensitive=case_insensitive, command_prefix=command_prefix, intents=intents)

bot = EthanBot(True, prefix, intents)

# currency symbols:
bot.token_symbol = "<:ethanger:763411726741143572>"
bot.coin_symbol = "<:ethoggers:868201785301561394>"

client = MongoClient(f"mongodb+srv://{USER}:{PWD}@ethanbotdb.jiyrt.mongodb.net/EthanBotDB")
db=client.bot_data

bot.ethan_tokens = db.ethan_tokens
bot.user_stocks = db.user_stocks
bot.general_info = db.general_info
bot.stock_info = db.stock_info

class BuyStocks(Select):
    options = []
    stocks = bot.stock_info.find()
    tokens_rate = 0.0

    def __init__(self, tokens_rate):
        self.tokens_rate = tokens_rate

        for stock in self.stocks:
            name = stock['name']
            converted_price = stock['price'] * self.tokens_rate
            currency = stock['currency']
            if (currency == 'USX'):
                converted_price /= 100
            description = f"{converted_price:,.2f}/unit\n"
            self.options.append(SelectOption
                (
                    label = name,
                    description = description,
                    emoji = bot.token_symbol
                )
            )
        super().__init__(
            placeholder = "Select a stock option!",
            options = self.options,
            row = 1
        )

    async def callback(self, interaction: Interaction):
        view: BuyStocksView = self.view
        view.continue_prompt = True
        view.stop()
        view.name = self.values[0]
        view.stock = bot.stock_info.find_one({'name': view.name})
        view.symbol = view.stock['symbol']
        view.converted_price = view.stock['price'] * self.tokens_rate
        if (view.stock['currency'] == 'USX'):
            view.converted_price /= 100
        embed = nextcord.Embed(title = f"Buying **{view.name}**:", description = f"How many units would you like to purchase? (Type 'max' for basically your entire balance)\n(`{view.converted_price:,.2f}`{self.bot.token_symbol}/unit)")
        await interaction.response.send_message(embed=embed)

class BuyStocksView(View):    
    name = ""
    stock = {}
    symbol = ""
    converted_price = 0.0
    continue_prompt = False

    def __init__(self, tokens_rate, timeout=30):
        self.tokens_rate = tokens_rate
        super().__init__(timeout=timeout)

        self.add_item(BuyStocks(tokens_rate))

    async def on_timeout(self):
        self.stop()

    async def on_error(self, interaction, select):
        await interaction.channel.send_message("lmao u suck")

class Stocks(commands.Cog):
    good_names = ["Crude Oil", "Gold", "Wheat", "Corn", "Ethanol"]
    symbols = "CL=F,GC=F,ZW=F,ZC=F,CU=F"
    base_rate = 12
    tokens_rate = base_rate

    def __init__(self, bot):
        self.bot = bot
        self.refresh_stocks.start()

    async def create_stock_account(self, ctx, member = None):
        if (member == None):
            member = ctx.author
        await ctx.channel.send(f"No stock account found for {member.mention}. Creating...")
        data = {
            "id": member.id,
            "name": f"{member.name}#{member.discriminator}",
            "stock_data": {}
        }
        print(data)
        await asyncio.sleep(1)
        await ctx.channel.send(f"Account created!")
        bot.user_stocks.insert_one(data)        

    @commands.command(name="stocks", aliases=["stock", "stonk", "stonks"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stocks(self, ctx, choice=""):
        async def update_rate():
            self.tokens_rate = self.base_rate * bot.general_info.find_one({"type": "currency"})["tokens_rate"]

        async def view_stocks(ctx):
            await update_rate()

            stocks = bot.stock_info.find()

            description = f"**Conversion Rate**: `{self.tokens_rate:,.2f}`{self.bot.token_symbol}/USD\n\n"
            for stock in stocks:
                symbol = stock['symbol'].replace('=F', '')
                name = stock['name']
                price = stock['price']
                converted_price = price * self.tokens_rate
                currency = stock['currency']
                if (currency == 'USX'):
                    price /= 100
                description += f"({symbol}) **{name}**: `{converted_price:,.2f}`{self.bot.token_symbol}/unit - ($`{price:,.2f}`)\n"

            query = {"type": "stocks"}
            last_update = bot.general_info.find_one(query)['update_time']
            date_time = last_update.strftime("%m/%d/%Y %I:%M:%S %p")
            description += f"\n**Data last updated at:** {date_time}"
            
            embed = nextcord.Embed(title="Stonks", description=description)
            await ctx.channel.send(embed=embed)

        async def buy_stocks(ctx):
            economy = self.bot.get_cog('Economy')
            member = ctx.author

            query = {"id": ctx.author.id}
            user = bot.ethan_tokens.find_one(query)
            if user == None:
                await economy.create_token_account(ctx, ctx.author)
            bal = user['tokens']

            view = BuyStocksView(self.tokens_rate)
            await ctx.channel.send("**BUYING STOCKS**", view=view)
            await view.wait()
            if (not view.continue_prompt):
                return

            def check(m):
                return (
                    m.author == member
                    and m.channel == ctx.channel
                )
            try:
                msg = await self.bot.wait_for (
                    "message",
                    timeout=15,
                    check=check
                )
                if msg:
                    # take floor to nearest millionth or whatever precision is set to
                    precision = 0.000001
                    if (msg.content.lower() == "max"):
                        amount = (bal / view.converted_price) // precision * precision
                    else:
                        try:
                            amount = float(msg.content)
                        except ValueError:
                            await ctx.channel.send(f"Hey dumbass you can't buy {msg.content} units of {view.name}")
                            return
            except asyncio.TimeoutError:
                await ctx.channel.send("Well give me a number, don't just stare at me like that you creep", delete_after=10)
                return

            total_price = amount * view.converted_price
            # return if the user doesn't have enough money.
            if (bal < total_price):
                await ctx.channel.send(f"lmao you don't have enough money fool, you need **{total_price:,.2f}**{self.bot.token_symbol} to buy **{amount:,.3f}** units of {view.name}")
                return
            
            embed = nextcord.Embed(title=f"Buying **{view.name}** ({view.stock['symbol']})", description=f"**Total**: `{amount:,.3f}`u for **`{total_price:,.2f}`**{self.bot.token_symbol} (`{view.converted_price:,.2f}`{self.bot.token_symbol}/unit)")
            await ctx.channel.send(embed=embed)
            # create user stocks collection if it doesn't exist, populate with data
            query = {"id": member.id}
            cur_stocks = bot.user_stocks.find_one(query)
            if (cur_stocks == None):
                await self.create_stock_account(ctx)
            data = {
"""
                "$set": {
                    "name": f"{member.name}#{member.discriminator}",
                    "stock_data": {
                        "name": view.name,
                        "symbol": view.stock['symbol'],
                        "amount":
                        "buy_price":
                        "buy_worth":
                    }
                }
"""
            }
            bot.user_stocks.update_one(query, data)

        if (choice == ""):
            await ctx.channel.send("Bro you gotta tell me what you want to do,\nimagine if you went up to your teacher and\nasked hey, how do you stonks?\nDo you want to 'view', 'buy' or 'sell' your stocks?")
        if (choice == "view"):
            await view_stocks(ctx)
        if (choice == "buy"):
            await buy_stocks(ctx)

    @tasks.loop(hours=8)
    async def refresh_stocks(self):
        now = datetime.now()
        print("Refreshing stocks at " + str(now))
        query = {"type": "stocks"}
        data = {
            "$set": {
                "update_time": now
            }
        }
        bot.general_info.find_one_and_update(query, data, upsert=True)

        url = "https://yfapi.net/v6/finance/quote"
        querystring = {"symbols": self.symbols}
        headers = {
            'x-api-key': STOCKS_API_KEY
            }
        response = requests.request("GET", url, headers=headers, params=querystring)

        try:
            formatted = response.json()['quoteResponse']['result']
            for good in formatted:
                symbol = good['symbol']
                name = good['shortName']
                currency = good['currency']
                price = round(good['regularMarketPrice'], 2)
                
                for good_name in self.good_names:
                    if (good_name in name):
                        name = good_name
                        break

                query = {
                    "symbol": symbol
                }
                data = {
                    "symbol": symbol,
                    "name": name,
                    "currency": currency,
                    "price": price
                }
                bot.stock_info.find_one_and_replace(query, data, upsert=True)
        except KeyError as e:
            print(f"Thingy happened with stonks: {e.message}")
            return


    @refresh_stocks.before_loop
    async def before_refresh(self):
        # wait until X:00:00
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        start = datetime.combine((now + timedelta(hours=1)).date(), time((now + timedelta(hours=1)).time().hour, 0, 0)).replace(tzinfo=timezone.utc)
        wait_seconds = (start - now).total_seconds()
        print("Waiting " + str(wait_seconds) + " before starting refresh.")
        
        await asyncio.sleep(wait_seconds)

class Froligarch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.pping()

    @commands.command(name="manualtally")
    @commands.has_permissions(administrator=True)
    async def manual_pp(self, ctx, days=0):
        await bot.wait_until_ready()
        
        guild = bot.get_guild(423583970328838154)
        channel = guild.get_channel(866168036770578432)
        
        now = datetime.now(timezone.utc)
        after = datetime.combine(now.date(), PP_START).replace(tzinfo=timezone.utc) - timedelta(days=days)
        before = datetime.combine(now.date(), PP_END).replace(tzinfo=timezone.utc) - timedelta(days=days)

        await channel.send("**-=-=- Tallying manually because Zach fucked up -=-=-**")

        messages = await channel.history(limit=None, before=before, after=after).flatten()
        pps = {}
        for msg in messages:
            print(msg.created_at)
            if (msg.author.id != bot.user.id):
                continue
            embeds = msg.embeds
            if embeds == []:
                continue
            for embed in embeds:
                footer = str(embed.footer.text)
                if (embed.title != "peepee size machine"):
                    continue
                if (footer not in pps) or len(pps) == 0:
                    cur = embed.description.split("\n")
                    pps[footer] = str(cur[1]).count("=")
        pps = dict(sorted(pps.items(), key=lambda item: item[1], reverse=True))
        print(pps)
        description = ""
        if len(pps.items()) == 0:
            description = f"xd yall suck, not even a single pp. Disgracing the Glorious Froligarchy."
        else:
            count = 0
            units = random.choice(["cm", "mm", "m", "in", "ft", "yd"])
            for key, value in pps.items():
                count += 1
                text = f"**({count}).** "
                if (count <= 2):
                    text += "<:poggies:826811320073453598> **FROLIGARCH** "
                if (value <= 1):
                    text += ":pinching_hand: L BOZO "
                member = guild.get_member(int(key))
                text += f"**{member.name}**: {value} {units}\n"
                description += text

        embed = nextcord.Embed(title="LEADERBOARD FOR TODAY", url="https://www.youtube.com/watch?v=iik25wqIuFo", description=description)
        await channel.send(embed=embed)
        await self.remove_froligarchs(guild)
        await self.add_froligarchs(guild, list(pps.items())[:2])

    async def activate_pp(self, announce=False):
        await bot.wait_until_ready()
        
        guild = bot.get_guild(423583970328838154)
        channel = guild.get_channel(866168036770578432)
        
        now = datetime.now(timezone.utc)
        after = datetime.combine(now.date(), PP_START).replace(tzinfo=timezone.utc)
        before = datetime.combine(now.date(), PP_END).replace(tzinfo=timezone.utc)
        duration = (before - after).total_seconds()
        total_seconds = (before - now).total_seconds()

        if (announce == True):
            await channel.send(f"<@&652326925800570880> {prefix}pp")
        if (total_seconds > 0 and total_seconds <= duration):
            print(f"Frogging: {total_seconds}sec remaining")
            await asyncio.sleep(total_seconds)
        elif (total_seconds > duration):
            return
        await channel.send("**-=-=- FROLIGARCHY FOR THE DAY HAS CLOSED. -=-=-**")

        messages = await channel.history(limit=None, before=before, after=after).flatten()
        pps = {}
        for msg in messages:
            if (msg.author.id != bot.user.id):
                continue
            embeds = msg.embeds
            if embeds == []:
                continue
            for embed in embeds:
                footer = str(embed.footer.text)
                if (embed.title != "peepee size machine"):
                    continue
                if (footer not in pps) or len(pps) == 0:
                    cur = embed.description.split("\n")
                    pps[footer] = str(cur[1]).count("=")
        pps = dict(sorted(pps.items(), key=lambda item: item[1], reverse=True))
        print(pps)
        description = ""
        if len(pps.items()) == 0:
            description = f"xd yall suck, not even a single pp. Disgracing the Glorious Froligarchy."
        else:
            count = 0
            units = random.choice(["cm", "mm", "m", "in", "ft", "yd"])
            for key, value in pps.items():
                count += 1
                text = f"**({count}).** "
                if (count <= 2):
                    text += "<:poggies:826811320073453598> **FROLIGARCH** "
                if (value <= 1):
                    text += "<:pinching_hand:> L BOZO "
                member = guild.get_member(int(key))
                text += f"**{member.name}**: {value} {units}\n"
                description += text

        embed = nextcord.Embed(title="LEADERBOARD FOR TODAY", url="https://www.youtube.com/watch?v=iik25wqIuFo", description=description)
        await channel.send(embed=embed)
        await self.remove_froligarchs(guild)
        await self.add_froligarchs(guild, list(pps.items())[:2])

    async def pping(self):
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        target = datetime.combine(now.date(), PP_START).replace(tzinfo=timezone.utc)
        seconds_until_target = math.ceil((target - now).total_seconds())
        print(f"Seconds until target 1: {seconds_until_target}")

        if (seconds_until_target < 0):
            if (seconds_until_target >= -7200):
                await self.activate_pp()
            target = datetime.combine(now.date() + timedelta(days=1), PP_START).replace(tzinfo=timezone.utc)
            seconds_until_target = math.ceil((target - now).total_seconds())
            print(f"Seconds until target 2: {seconds_until_target}")
        # maybe replace 7200 with the difference b/w PP_START and PP_END
        await asyncio.sleep(seconds_until_target)
        await self.activate_pp(announce=True)
        while True:
            now = datetime.utcnow().replace(tzinfo=timezone.utc)
            target = datetime.combine(now.date() + timedelta(days=1), PP_START).replace(tzinfo=timezone.utc)
            seconds_until_target = math.ceil((target - now).total_seconds())
            print(f"Seconds until target 3: {seconds_until_target}")
            await asyncio.sleep(seconds_until_target)
            await self.activate_pp(announce=True)

    async def add_froligarchs(self, guild, members):
        role = guild.get_role(841482931255115816)
        for member in members:
            frog = guild.get_member(int(member[0]))
            await frog.add_roles(role)

    async def remove_froligarchs(self, guild):
        role = guild.get_role(841482931255115816)
        role_members = role.members
        for member in role_members:
            await member.remove_roles(role)

    @commands.command(name='pp')
    async def pp(self, ctx):
        def peepee():
            length = random.randint(0, 15)
            x = random.randint(1, 250)
            if (x == 69):
                length = random.randint(15, 3500)
            return length

        title = "peepee size machine"
        count = peepee()
        # if (ctx.author.id == 372841965198376963):
        #     count = random.randint(0, random.randint(1, 30))
        #     if (count > 14):
        #         await asyncio.sleep(3)
        #         await ctx.channel.send("congor moment")
        # if (ctx.author.id == 501505695091392527):
        #     count = random.randint(0, 20)
        #     pass
        # if (ctx.author.id == 597628340203028485):
        #     count = -(random.randint(11, 15))
        #     await ctx.send("some australia type shit")
        #     description = f"{ctx.message.author.name}'s penis\nᗡ{('=' * abs(count))}8 ({count})"
        #     embed=nextcord.Embed(title=title, url="https://www.youtube.com/watch?v=iik25wqIuFo", description=description)
        #     embed.set_footer(text=f"{ctx.message.author.id}")
        #     await ctx.send(embed=embed)
        #     return
        # if (ctx.author.id == 353531794018009088):
        #     count = random.randint(0, 24)
        # if (ctx.author.id == 485120076941623296):
        #     count = random.randint(3, 15)
        description = f"{ctx.message.author.name}'s penis\n8{('=' * count)}D ({count})"
        embed=nextcord.Embed(title=title, url="https://www.youtube.com/watch?v=iik25wqIuFo", description=description)
        embed.set_footer(text=f"{ctx.message.author.id}")
        await ctx.send(embed=embed)

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

class Zach(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="exportchannels")
    async def export_channels(self, ctx):
        guild = bot.get_guild(423583970328838154)
        channels = {}

        for x in guild.text_channels:
            channels[x.name] = x.category

        for x in guild.voice_channels:
            channels[x.name] = x.category

        with open("channels.txt", "wb") as f:
            for key, value in channels.items(): 
                f.write(('%s:%s\n' % (key, value)).encode('utf8'))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.channel.send(f"Stop spamming me you dolt: try again in {round(error.retry_after, 2)}sec.", delete_after=4)
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.channel.send(f"Your input was invalid. Unfortunately, EthanBot does not have a snarky response for you! So, you suck!")
    else:
        print(error)

def setup(bot):
    bot.add_cog(Listeners(bot))
    bot.add_cog(Ethan(bot))
    bot.add_cog(Economy(bot))
    bot.add_cog(Stocks(bot))
    bot.add_cog(Gambling(bot))
    bot.add_cog(Fun(bot))
    bot.add_cog(Froligarch(bot))
    bot.add_cog(Zach(bot))

setup(bot)
bot.run(TOKEN)