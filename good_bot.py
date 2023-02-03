# bot.py
import os
import random
import asyncio
from datetime import datetime, timedelta, time, timezone
import math
import pymongo
from pymongo import MongoClient
import requests
import json

import nextcord
from nextcord import SelectOption, ButtonStyle
from nextcord.ext import tasks, commands
from nextcord.interactions import Interaction, InteractionResponse
from nextcord.ui import button, View, Button, Select, TextInput, Modal

from cogs.Listeners import Listeners
from cogs.Ethan import Ethan
from cogs.Economy import Economy
from cogs.Gambling import Gambling
from cogs.Fun import Fun
from cogs.AI import AI

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
USER = os.getenv('USER')
PWD = os.getenv('PWD')

# pping:
PP_START = time(21, 00, 00)
PP_END = time(23, 00, 00)

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

bot.STOCKS_API_KEY = os.getenv("YAHOO_API_KEY")

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
            description = f"{converted_price:,.4g}/unit\n"
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
        embed = nextcord.Embed(title = f"Buying **{view.name}**:", description = f"How many units would you like to purchase? (Type 'max' for basically your entire balance)\n(`{view.converted_price:,.4g}`{bot.token_symbol}/unit)")
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

            stocks = list(bot.stock_info.find())

            query = {
                "id": ctx.author.id
            }
            user_stocks = bot.user_stocks.find_one(query)
            if (user_stocks == None):
                await self.create_stock_account(ctx)
                stock_data = {}
            else:
                stock_data = user_stocks["stock_data"]

            description = f"**Conversion Rate**: `{self.tokens_rate:,.4g}`{self.bot.token_symbol}/USD\n\n"

            for stock in stocks:
                symbol = stock['symbol'].replace('=F', '')
                name = stock['name']
                price = stock['price']
                currency = stock['currency']
                if (currency == 'USX'):
                    price /= 100
                converted_price = price * self.tokens_rate
                description += f"({symbol}) **{name}**: `{converted_price:,.4g}`{self.bot.token_symbol}/**unit** - ($`{price:,.2f}`)\n"

            query = {"type": "stocks"}
            last_update = bot.general_info.find_one(query)['update_time']
            date_time = last_update.strftime("%m/%d/%Y %I:%M:%S %p")
            description += f"\n**Data last updated at:** {date_time}\n\n**Stock Inventory:**"

            print(stock_data)
            if (stock_data == {}):
                description += f"\n`You haven't bought any shares.`"
            else:
                for stock in stocks:
                    name = stock['name']
                    price = stock['price']
                    currency = stock['currency']
                    if (currency == 'USX'):
                        price /= 100

                    if (name in stock_data.keys() and float(stock_data[name]) != 0.0):
                        shares = stock_data[name]
                        total_value_usd = shares * price
                        total_value_tokens = total_value_usd * self.tokens_rate
                        description += f"\n**{name}**: `{shares:,.3f}`**u** worth `{total_value_tokens:,.4g}`{bot.token_symbol} ($`{total_value_usd:,.2f}`)"

            embed = nextcord.Embed(title=f"{ctx.author.name}'s Stonks", description=description)
            await ctx.channel.send(embed=embed)

        async def buy_stocks(ctx):
            economy = self.bot.get_cog('Economy')
            member = ctx.author

            query = {"id": ctx.author.id}
            user = bot.ethan_tokens.find_one(query)
            if user == None:
                await economy.create_token_account(ctx, ctx.author)
            bal = user['tokens']

            if (bal == 0):
                await ctx.channel.send(f"{ctx.author.mention} Get outta here, broke ass. You need {self.bot.token_symbol} to purchase stocks.")
                return

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
                await ctx.channel.send(f"lmao you don't have enough money fool, you need **{total_price:,.4g}**{bot.token_symbol} to buy **{amount:,.3f}** units of {view.name}")
                return
            new_balance = bal - total_price
            
            # create user stocks collection if it doesn't exist, populate with data
            query = {
                "id": member.id  
            }
            user = bot.user_stocks.find_one(query)
            if (user == None):
                await self.create_stock_account(ctx)
                new_stocks = {}
            else:
                # two variables in case we want to show the user how many shares they had previously
                cur_stocks = user["stock_data"]
                new_stocks = cur_stocks

            if (view.name not in new_stocks.keys() or float(new_stocks[view.name]) == 0.0):
                new_stocks[view.name] = amount
            else:
                new_stocks[view.name] += amount

            data = {
                "$set": {
                    "name": f"{member.name}#{member.discriminator}",
                    "stock_data": new_stocks
                }
            }
            bot.user_stocks.update_one(query, data)

            # withdraw from user balance
            data = {
                "$set": {
                    "tokens": new_balance
                }
            }
            bot.ethan_tokens.update_one(query, data)

            embed = nextcord.Embed(title=f"Purchased **{view.name}** ({view.stock['symbol']})", description=f"**Total**: `{amount:,.3f}`u for **`{total_price:,.4g}`**{bot.token_symbol} (`{view.converted_price:,.4g}`{bot.token_symbol}/unit)\n**You now have: `{new_balance:,.4g}`**{bot.token_symbol}")
            await ctx.channel.send(embed=embed)
            return

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
            'x-api-key': bot.STOCKS_API_KEY
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

class Zach(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="exportchannels")
    @commands.check_any(commands.is_owner())
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

    @commands.command(name="DOTHETHINGODROBOT")
    @commands.check_any(commands.is_owner())
    async def do_thing(self, ctx):
        guild = bot.get_guild(423583970328838154)
        channels = {}

        for channel in guild.text_channels:
            await channel.send("░██████╗░█████╗░███╗░░░███╗  ░██████╗██╗░░░██╗██╗░░██╗\n██╔════╝██╔══██╗████╗░████║  ██╔════╝██║░░░██║╚██╗██╔╝\n╚█████╗░███████║██╔████╔██║  ╚█████╗░██║░░░██║░╚███╔╝░\n░╚═══██╗██╔══██║██║╚██╔╝██║  ░╚═══██╗██║░░░██║░██╔██╗░\n██████╔╝██║░░██║██║░╚═╝░██║  ██████╔╝╚██████╔╝██╔╝╚██╗\n╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝  ╚═════╝░░╚═════╝░╚═╝░░╚═╝")

    @commands.command(name="purgenicks")
    @commands.has_permissions(administrator=True)
    async def purge_nicks(self, ctx):
        members = [member for member in ctx.guild.members if not member.bot]

        message = await ctx.channel.send("Purging nicknames...")
        done = 0
        for m in members:
            done += 1
            if (m.guild_permissions.administrator):
                continue
            await m.edit(nick=None)
        await message.edit(content=f"Purged nicknames from **{len(members)}** members.")

    @commands.command(name="randomnicks")
    @commands.has_permissions(administrator=True)
    async def random_nicks(self, ctx):
        members = [member for member in ctx.guild.members if not member.bot]
        req = requests.get(f"https://random-word-api.herokuapp.com/word?number=200")
        words = json.loads(req.text)

        message = await ctx.channel.send("Assigning random nicknames...")

        for m in range(len(members)):
            if (members[m].guild_permissions.administrator):
                continue
            nick = random.choice(words)
            while True:
                word = random.choice(words)
                length = len(nick)
                if (length + len(word) > 31):
                    break
                else:
                    nick += f" {word}"
            await members[m].edit(nick=nick)

        await message.edit(content=f"Assigned random nicknames to **{len(members)}** members.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.channel.send(f"Stop spamming me you dolt: try again in {round(error.retry_after, 2)}sec.", delete_after=4)
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.channel.send(f"You don't have permission to do this. Nice try lol")
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
    bot.add_cog(AI(bot))

setup(bot)
bot.run(TOKEN)