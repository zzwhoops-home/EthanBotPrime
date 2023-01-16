import nextcord
from nextcord.ext import tasks, commands
import pymongo
from pymongo import MongoClient

import os
import asyncio
import math
import random
from datetime import datetime, timedelta, time, timezone

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def create_token_account(self, ctx, member=None, tokens=0.00, coins=0.00):
        if (member == None):
            member = ctx.author
        await ctx.channel.send(f"Records not found... creating account for {member.mention}.")
        data = {
            "id": member.id,
            "name": f"{member.name}#{member.discriminator}",
            "tokens": tokens,
            "coins": coins
        }
        print(data)
        await asyncio.sleep(1)
        await ctx.channel.send(f"Account created!")
        self.bot.ethan_tokens.insert_one(data)

    async def get_symbol(self, currency):
        if currency == "tokens":
            return(f"{self.bot.token_symbol}")
        elif currency == "coins":
            return(f"{self.bot.coin_symbol}")

    @commands.command(name="balance", aliases=["bal"])
    async def view_balance(self, ctx, member: nextcord.Member = None):
        if member is None:
            member = ctx.author
        
        id = member.id
        existing = self.bot.ethan_tokens.find_one({"id": id})
        tokens = 0.00
        coins = 0.00
        if existing == None:
            await self.create_token_account(ctx, member)
        else:
            tokens = f"{existing['tokens']:,.4g}"
            coins = f"{existing['coins']:,.4g}"

        embed = nextcord.Embed(title=f"{member.name}'s EthanBalance:tm:")
        embed.add_field(name="<:ethanger:763411726741143572> (ET)", value=tokens, inline=True)        
        embed.add_field(name="<:ethoggers:868201785301561394> (EC)", value=coins, inline=True)
        await ctx.channel.send(embed=embed)

    @commands.command(name="pay", aliases=["donate", "give"])
    async def pay(self, ctx, currency, receiver: nextcord.Member = None, amount = ""):
        giver = ctx.author
        types = ["tokens", "coins"]
        symbol = await self.get_symbol(currency)

        if (currency not in types):
            await ctx.channel.send(f"Ethan{currency.capitalize()}:tm: doesn't exist. Nice try! Type 'coins' or 'tokens'.")
            return
        if (receiver == None):
            await ctx.channel.send("Who you payin', yourself? That ain't how it works.")
            return

        giver_existing = self.bot.ethan_tokens.find_one({"id": giver.id})
        giver_balance = giver_existing[currency]
        try:
            amount = float(amount)
        except ValueError:
            if (amount == "all"):
                amount = giver_balance
            else:
                await ctx.channel.send(f"How the fuck am I supposed to give {receiver.display_name} {amount}{symbol}?")
                return
        if (float(amount) <= 0.0):
            await ctx.channel.send("Hey you gotta *pay* the person a positive number that isn't 0 bitch")
            return
            
        receiver_existing = self.bot.ethan_tokens.find_one({"id": receiver.id})
        if (giver_existing == None):
            await ctx.channel.send(f"You need an account and to like... not be broke to pay someone lmao. Try {ctx.prefix}bal to create one.")
            return
        if (receiver_existing == None):
            await self.create_token_account(ctx, receiver)
            receiver_existing = self.bot.ethan_tokens.find_one({"id": receiver.id})
        
        if (amount == "all"):
            amount = giver_balance
        receiver_balance = receiver_existing[currency]
        new_giver_balance = giver_balance - amount
        new_receiver_balance = receiver_balance + amount

        if (new_giver_balance < 0):
            await ctx.channel.send(f"You can't give that much, ha poor")
            return

        give_data = {
            "$set": {
                currency: new_giver_balance
            }
        }
        receive_data = {
            "$set": {
                currency: new_receiver_balance
            }
        }
        self.bot.ethan_tokens.update_one({"id": giver.id}, give_data)
        self.bot.ethan_tokens.update_one({"id": receiver.id}, receive_data)

        # maybe replace with another database call to make sure everything is consistent?
        await ctx.channel.send(f"You gave **{amount:,.4g}**{symbol} to {receiver.mention}.\nYour balance: **{new_giver_balance:,.4g}**{symbol}\nTheir balance: **{new_receiver_balance:,.4g}{symbol}**")

    @commands.command(name="circulation", aliases=['circ', 'total', 'all'])
    async def total_wealth(self, ctx):
        agg = self.bot.ethan_tokens.aggregate([{
            "$group": {
                "_id": 1,
                "tokens": {"$sum": "$tokens"},
                "coins": {"$sum": "$coins"},
                "count": {"$sum": 1}
            }
        }])

        total_value = list(agg)[0]
        db_count = total_value['count']
        tokens = total_value['tokens']
        coins = total_value['coins']
        avg_tokens = tokens / db_count
        avg_coins = coins / db_count

        description = f"**Members in database: __{db_count}__**\n\n**Tokens:** `{tokens:,.4g}`{self.bot.token_symbol}\n**Average:** `{avg_tokens:,.4g}`{self.bot.token_symbol}\n\n**Coins:** `{coins:,.4g}`{self.bot.coin_symbol}\n**Average:** `{avg_coins:,.4g}`{self.bot.coin_symbol}"
        embed = nextcord.Embed(title=f"__{ctx.guild.name}'s Server Worth__", description=description)
        await ctx.channel.send(embed=embed)
        
    @commands.command(name="leaderboard", aliases=["top", "rich"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def leaderboard(self, ctx, currency = ""):
        member = ctx.author
        types = ["tokens", "coins"]
        if (currency not in types):
            await ctx.channel.send(f"Ethan{currency.capitalize()}:tm: doesn't exist. Nice try! Type 'coins' or 'tokens'.")
            self.leaderboard.reset_cooldown(ctx)
            return
        
        description = ""
        count = 0
        if currency == "tokens":
            accounts = self.bot.ethan_tokens.find().sort("tokens", pymongo.DESCENDING).limit(20)
            for account in accounts:
                print(account)
                if (account['name'] == f"{member.name}#{member.discriminator}"):
                    is_user = "***"
                else:
                    is_user = ""
                if (account['tokens'] == 0):
                    break
                count += 1
                description += f"**#{count}**: `{account['tokens']:,.4g}`<:ethanger:763411726741143572> - {is_user}{account['name']}{is_user}\n"
        elif currency == "coins":
            accounts = self.bot.ethan_tokens.find().sort("coins", pymongo.DESCENDING).limit(20)
            for account in accounts:
                if (account['name'] == f"{member.name}#{member.discriminator}"):
                    is_user = "***"
                else:
                    is_user = ""
                if (account['coins'] == 0):
                    break
                count += 1
                description += f"**#{count}**: `{account['coins']:,.4g}`<:ethoggers:868201785301561394> - {is_user}{account['name']}{is_user}\n"

        embed = nextcord.Embed(title=f"{ctx.guild.name}'s {currency.capitalize()} Leaderboard", description=description)
        await ctx.channel.send(embed=embed)

    @commands.command(name="inflation", aliases=["rates"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def get_rate(self, ctx):
        query = {
            "type": "currency"
        }
        rates = self.bot.general_info.find_one(query)
        coins_rate = rates["coins_rate"]
        tokens_rate = rates["tokens_rate"]
        coins_symbol = await self.get_symbol("coins")
        tokens_symbol = await self.get_symbol("tokens")
        embed = nextcord.Embed(title=f"__{ctx.guild}'s Inflation Rates:__", description=f"{tokens_symbol}: **{tokens_rate:,.3f}x**\n{coins_symbol}: **{coins_rate:,.3f}x**")
        await ctx.channel.send(embed=embed)

    @commands.command(name="ETHANEDGEPLAY", aliases=["ELEP", "EEP", "EDGEPLAY"])
    @commands.cooldown(1, 45, commands.BucketType.guild)
    async def eth_edge(self, ctx, success="100"):
        try:
            success = int(success)
        except ValueError:
            await ctx.channel.send("Bro you gotta give me an integer")
            return
        time = 30
        rates = self.bot.general_info.find_one({"type": "currency"})
        tokens_rate = rates["tokens_rate"]
        coins_rate = rates["coins_rate"]

        limit = 1000
        if (success <= 0):
            await ctx.channel.send(f"Enter a number between 1 and {limit}, dumbass. Victory doesn't come *that* easy.")
            self.eth_edge.reset_cooldown(ctx)
            return
        elif (success >= limit):
            await ctx.channel.send(f"I will leak my OnlyFans if you somehow get over {limit}. Pick another number!")
            self.eth_edge.reset_cooldown(ctx)
            return

        async def calculate_tokens(users, messages, target, inflation):
            user_score = math.pow(users * 15, 1.2)
            message_score = math.pow(messages, 1.3) / 2
            bonus = random.randint(0, messages)
            multiplier = math.pow(target / 50, 0.4)
            total = (user_score + message_score + bonus) * multiplier
            inflation_total = total * inflation
            data = {
                "user_score": user_score,
                "message_score": message_score,
                "multiplier": multiplier,
                "bonus": bonus,
                "total": total,
                "inflation_total": round(inflation_total, 2)
            }
            return data

        async def calculate_coins(users, messages, target, inflation):
            msg_rate_user = (messages / users) / time

            rate_score = math.pow(msg_rate_user * 75, 0.9)
            multiplier = math.pow(target / 50, 0.4)
            total = rate_score * multiplier
            inflation_total = total * inflation
            data = {
                "msg_rate_user": msg_rate_user,
                "rate_score": rate_score,
                "multiplier": multiplier,
                "total": total,
                "inflation_total": round(inflation_total, 2)
            }
            return data

        async def update_user_account(self, member=None, tokens=0.00, coins=0.00):
            id = int(member.id)

            existing = self.bot.ethan_tokens.find_one({ "id": id })

            if (existing == None):
                data = {
                    "id": id,
                    "name": f"{member.name}#{member.discriminator}",
                    "tokens": tokens,
                    "coins": coins
                }
                self.bot.ethan_tokens.insert_one(data)
            else:
                query = {
                    "id": id
                }
                data = {
                    "$inc": {
                        "tokens": tokens,
                        "coins": coins
                    }
                }
                self.bot.ethan_tokens.update_one(query, data)
            return

        async def counter(ctx, START_TIME, END_TIME):
            count = 0
            users = 0
            per_user_stats = {}

            await asyncio.sleep(time)

            embed = nextcord.Embed(title="__**STOP**__", description="Tallying love for edge play...")
            await ctx.channel.send(embed=embed)
            await asyncio.sleep(1)

            messages = await ctx.channel.history(before=END_TIME, after=START_TIME).flatten()

            for msg in messages:
                if (msg.content != "ELEP"):
                    continue
                id = msg.author.id
                count += 1
                if (id not in per_user_stats):
                    per_user_stats[id] = 1
                elif (id in per_user_stats):
                    per_user_stats[id] = per_user_stats.get(id) + 1

            users = len(per_user_stats)
            user_earnings = ""
            if (int(count) >= int(success)):
                tokens = await calculate_tokens(users, count, success, tokens_rate)
                coins = await calculate_coins(users, count, success, coins_rate)
                for key, value in per_user_stats.items():
                    msg_percent = value / count
                    earned_tokens = msg_percent * tokens['inflation_total']
                    earned_coins = msg_percent * coins['inflation_total']
                    user = self.bot.get_user(key)
                    user_name = user.name

                    await update_user_account(self, member=user, tokens=earned_tokens, coins=earned_coins)

                    user_earnings += f"**{user_name}**: **{value}** msgs (**{msg_percent * 100:.2f}**%) = **{earned_tokens:,.4g}**{self.bot.token_symbol} + **{earned_coins:,.4g}**{self.bot.coin_symbol}\n"
                description = f"Token Payout: **{tokens['inflation_total']:,.4g}**{self.bot.token_symbol}\nCoin Payout: **{coins['inflation_total']:,.4g}**{self.bot.coin_symbol}\n\n__**Breakdown:**__\nMessages: **{count}**/**{success}**\nUsers Participated: **{users}**\n\n__**User Earnings:**__\n{user_earnings}"
            else:
                tokens = 0
                coins = 0            
                for key, value in per_user_stats.items():
                    user = self.bot.get_user(key)
                    user_name = user.name
                    msg_percent = value / count
                    user_earnings += f"**{user_name}**: **{value}** msgs (**{msg_percent * 100:.2f}**%)"
                description = f"Token Payout: **{tokens}**{self.bot.token_symbol}\nCoin Payout: **{coins}**{self.bot.coin_symbol}\n\n__**Breakdown:**__\nMessages: **{count}**/**{success}**\nUsers Participated: **{users}**\n\n__**User Earnings**__\n{user_earnings}"

            embed = nextcord.Embed(title="__**Results:**__", description=description)
            await ctx.channel.send(embed=embed)
            await asyncio.sleep(2)

            if (int(count) >= int(success)):
                await ctx.channel.send("https://ih1.redbubble.net/image.724682828.9041/flat,1000x1000,075,f.jpg")
            else:
                await ctx.channel.send("you tried lmao you suck\n**YOU SUCK SKILL ISSUE LMAO**")
                await ctx.channel.send("https://i.imgur.com/BSSVwl6.png")

            return ([count, users])

        async def record_check(ctx, stats):
            query = {
                "type": "records"
            }
            records = self.bot.general_info.find_one(query)["EEP"]
            msgs = records["msgs"]
            users = records["users"]

            if (stats[0] > msgs):
                description = f"Original: **{msgs}** msgs, **{users}** users\nNew: **{stats[0]}** msgs, **{stats[1]}** users"
                embed = nextcord.Embed(title="**New Record!**", description=description)
                await ctx.channel.send(embed=embed)
            else:
                return

            data = {
                "$set":
                {
                    "EEP": {
                        "msgs": stats[0],
                        "users": stats[1]
                    }
                }
            }
            self.bot.general_info.update_one(query, data)
            

        embed=nextcord.Embed(title="I LOVE EDGE PLAY. PREPARE TO SEND 'ELEP' FOR 30 SECONDS", description=f"Goal: {success}\n")
        await ctx.channel.send(embed=embed)
        
        delay = 3
        first = await ctx.channel.send(f"**READY**")
        for x in range(delay):
            await asyncio.sleep(1)
            await first.edit(f"**{str(delay - x)}**")

        await asyncio.sleep(1)
        go_msg = await ctx.channel.send("**-=-=- GO -=-=-**")

        # get timestamp of go msg so system clock never fails me
        START_TIME = (go_msg.created_at)
        END_TIME = START_TIME + timedelta(seconds=30)

        stats = await counter(ctx, START_TIME, END_TIME)
        await record_check(ctx, stats)

    @commands.command(name="FREETOKENS", aliases=["beg", "mooch"])
    async def free_tokens(self, ctx):
        query = {
            "type": "currency"
        }
        rates = self.bot.general_info.find_one(query)
        # coins_rate = rates["coins_rate"]
        tokens_rate = rates["tokens_rate"]

        choice = random.randint(1, 3)
        if (choice == 1):
            base_amount = random.randint(20, 45) / 10
            amount = tokens_rate * base_amount
            
            id = ctx.author.id
            existing = self.bot.ethan_tokens.find_one({"id": id})
            if existing == None:
                await self.create_token_account(ctx)
                existing_tokens = 0
            else:
                existing_tokens = existing["tokens"]

            new_tokens = existing_tokens + amount

            query = {
                "id": id
            }
            data = {
                "$set": {
                    "tokens": new_tokens
                }
            }
            self.bot.ethan_tokens.update_one(query, data)

            await ctx.channel.send(f"{ctx.author.mention} You've been awarded **{amount:,.4g}**{self.bot.token_symbol}. You now have **{new_tokens:,.4g}**{self.bot.token_symbol}")
        else:
            await ctx.channel.send(f"{ctx.author.mention} lol no.")

    @commands.command(name="steal", aliases=["rob", "indefinitelyborrow"])
    # change to 120 SECONDS AFTER UR DONE
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def steal(self, ctx, victim: nextcord.Member = None):
        if (victim == None or victim.id == ctx.author.id):
            await ctx.channel.send("You can't steal from yourself, nice try! Give me a user to rob!")
            return
        
        robber = ctx.author
            
        tokens_symbol = await self.get_symbol("tokens")
        query = {
            "type": "currency"
        }
        rates = self.bot.general_info.find_one(query)
        tokens_rate = rates["tokens_rate"]

        robber_id = robber.id
        robber_existing = self.bot.ethan_tokens.find_one({"id": robber_id})
        if robber_existing == None:
            await ctx.channel.send("lmao u gotta create an account with eb!bal before you can rob someone.")
            return
        
        robber_current = robber_existing['tokens']

        if robber_current <= 0:
            await ctx.channel.send(f"Well I would let you go into more debt, but you gotta have a positive token balance to rob someone. You have **{robber_current}**{tokens_symbol}.")
            return

        victim_id = victim.id
        victim_existing = self.bot.ethan_tokens.find_one({"id": victim_id})
        
        if victim_existing == None or victim_existing['tokens'] <= 0:
            fine = random.randint(0, 100) * tokens_rate
            await ctx.channel.send(f"Hey, leave this penniless person alone, you heartless freak. I'm taking **{fine:,.4g}**{tokens_symbol} because of that. Jerk. Scum of the earth.")
            
            robber_new = robber_current - fine

            robber_data = {
                "$set": {
                    "tokens": robber_new
                }
            }
            self.bot.ethan_tokens.update_one({"id": robber_id}, robber_data)

            await ctx.channel.send(f"You now have **{robber_new:,.4g}**{tokens_symbol}, asshole.")
            return

        victim_current = victim_existing['tokens']

        async def update_balances(amount):
            robber_new = robber_current + amount
            victim_new = victim_current - amount

            robber_data = {
                "$set": {
                    "tokens": robber_new
                }
            }
            victim_data = {
                "$set": {
                    "tokens": victim_new
                }
            }
            self.bot.ethan_tokens.update_one({"id": robber_id}, robber_data)
            self.bot.ethan_tokens.update_one({"id": victim_id}, victim_data)
            await ctx.channel.send(f"{robber.mention} now has **{robber_new:,.4g}**{tokens_symbol}. {victim.mention} now has **{victim_new:,.4g}**{tokens_symbol}.")     

        async def update_balances_fractions(fraction):
            actual = fraction / 100
            amount = victim_current * actual

            robber_new = robber_current + amount
            victim_new = victim_current - amount

            robber_data = {
                "$set": {
                    "tokens": robber_new
                }
            }
            victim_data = {
                "$set": {
                    "tokens": victim_new
                }
            }
            self.bot.ethan_tokens.update_one({"id": robber_id}, robber_data)
            self.bot.ethan_tokens.update_one({"id": victim_id}, victim_data)
            await ctx.channel.send(f"{robber.mention}, you stole **{amount:,.4g}**{tokens_symbol} ({actual:.1%}) from {victim.mention}.")
            await ctx.channel.send(f"{robber.mention} now has **{robber_new:,.4g}**{tokens_symbol}. {victim.mention} now has **{victim_new:,.4g}**{tokens_symbol}.")     


        roll = random.randint(1, 100)
        if (roll <= 25):
            fine = random.randint(0, 100) * tokens_rate

            await ctx.channel.send(f"Well {robber.mention}, you tried to rob {victim.mention} but Ethan's police force caught you in the act. They don't believe in prisons, but you were forced to pay {victim.mention} **{fine:,.4g}**{tokens_symbol}. Get better at robbing other people next time, idiot.")
            await update_balances(-fine)
            return
        elif (roll <= 80):
            theft = random.randint(40, 80) / 10

            await ctx.channel.send(f"{robber.mention}, you stole a little bit! {victim.mention} will probably not be too happy.")
            await update_balances_fractions(theft)
            return
        elif (roll <= 98):
            theft = random.randint(150, 400) / 10

            await ctx.channel.send(f"{robber.mention}, you stole a good chunk from {victim.mention}!")
            await update_balances_fractions(theft)
            return
        elif (roll > 98):
            theft = random.randint(700, 950) / 10

            await ctx.channel.send(f"{robber.mention}, you stole BASICALLY EVERYTHING LOL {victim.mention} just got rolled <:andeth:763036789174435910>")
            await update_balances_fractions(theft)
            return