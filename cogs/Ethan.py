import nextcord
from nextcord.ext import tasks, commands
import pymongo
from pymongo import MongoClient

import os
import asyncio

class Ethan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ethelp")
    async def ethan_help(self, ctx):
        if (ctx.author.id != 390601966423900162 and ctx.author.id != 292448459909365760):
            await ctx.channel.send("Only Ethan can use this dumbass")
            return

        embed = nextcord.Embed(title="**Fun:**", description=f"**Viraj**: {self.bot.VIRAJ}\n**Sam**: {self.bot.SAM}")
        await ctx.author.send(embed=embed)

    @commands.command(name="set")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def set_balance(self, ctx, currency, member: nextcord.Member, amount):
        economy = self.bot.get_cog('Economy')
        amount = round(float(str(amount).replace(",","")), 2)
        symbol = await economy.get_symbol(currency)
        types = ["tokens", "coins"]

        if (ctx.author.id != 390601966423900162):
            await ctx.channel.send("Only Ethan can use this dumbass")
            self.set_balance.reset_cooldown(ctx)
            return
        if (currency not in types):
            await ctx.channel.send(f"Ethan{currency.capitalize()}:tm: doesn't exist. Nice try! Type 'coins' or 'tokens'.")
            self.set_balance.reset_cooldown(ctx)
            return

        id = member.id
        existing = self.bot.ethan_tokens.find_one({"id": id})
        if existing == None:
            await economy.create_token_account(ctx, member)
            if (currency == "tokens"):
                data["tokens"] = amount
            if (currency == "coins"):
                data["coins"] = amount
            self.bot.ethan_tokens.insert_one(data)        
            await ctx.channel.send(f"Okay, {member.mention} now has **{amount:,.4g}** {symbol}.")
        else:
            query = {
                "id": id
            }
            if (currency == "tokens"):
                new_balance = amount
                data = {
                    "$set":
                    {
                        "name": f"{member.name}#{member.discriminator}",
                        "tokens": new_balance
                    }
                }
                self.bot.ethan_tokens.update_one(query, data)
            if (currency == "coins"):
                new_balance = amount
                data = {
                    "$set":
                    {
                        "name": f"{member.name}#{member.discriminator}",
                        "coins": new_balance
                    }
                }
                self.bot.ethan_tokens.update_one(query, data)

            await ctx.channel.send(f"Okay, {member.mention} now has **{amount:,.4g}** {symbol}.")

    @commands.command(name="edit", aliases=["add"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def edit_balance(self, ctx, currency, member: nextcord.Member, amount):
        economy = self.bot.get_cog('Economy')
        amount = round(float(str(amount).replace(",","")), 2)
        symbol = await economy.get_symbol(currency)
        types = ["tokens", "coins"]

        if (ctx.author.id != 390601966423900162):
            await ctx.channel.send("Only Ethan can use this dumbass")
            self.edit_balance.reset_cooldown(ctx)
            return
        if (currency not in types):
            await ctx.channel.send(f"Ethan{currency.capitalize()}:tm: doesn't exist. Nice try! Type 'coins' or 'tokens'.")
            self.edit_balance.reset_cooldown(ctx)
            return

        id = member.id
        existing = self.bot.ethan_tokens.find_one({"id": id})
        if existing == None:
            if (currency == "tokens"):
                await economy.create_token_account(ctx, member, tokens=amount)
            if (currency == "coins"):
                await economy.create_token_account(ctx, member, coins=amount)
            await ctx.channel.send(f"Okay, {member.mention} now has **{amount:,.4g}** {symbol}")
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
                self.bot.ethan_tokens.update_one(query, data)
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
                self.bot.ethan_tokens.update_one(query, data)

            if (amount < 0):
                await ctx.channel.send(f"Okay, I've taken **{amount:,.4g}** {symbol} from {member.mention}.\nThey now have **{new_balance:,.4g}** {symbol}.")
            else:
                await ctx.channel.send(f"Okay, I've added **{amount:,.4g}** {symbol} to {member.mention}.\nThey now have **{new_balance:,.4g}** {symbol}.")

    @commands.command(name="editall", aliases=["addall"])
    @commands.cooldown(1, 5)
    async def edit_all_balances(self, ctx, currency, amount):
        economy = self.bot.get_cog('Economy')
        amount = round(float(str(amount).replace(",","")), 2)
        types = ["tokens", "coins"]
        symbol = await economy.get_symbol(currency)

        if (ctx.author.id != 390601966423900162):
            await ctx.channel.send("Stop trying to be Ethan")
            self.edit_all_balances.reset_cooldown(ctx)
            return
        if (currency == ""):
            await ctx.channel.send("Well pick a currency to add to.")
            self.edit_all_balances.reset_cooldown(ctx)
            return
        if (currency not in types):
            await ctx.channel.send(f"Ethan{currency.capitalize()}:tm: doesn't exist. Nice try!")
            self.edit_all_balances.reset_cooldown(ctx)
            return
        if (amount == 0.0):
            await ctx.channel.send("You're a dumb dumb, dumb dumb")
            self.edit_all_balances.reset_cooldown(ctx)
            return
            
        # increment all currency values by amount
        data = {
            "$inc":
            {
                currency: amount
            }
        }
        self.bot.ethan_tokens.update_many(filter={}, update=data)
        count = self.bot.ethan_tokens.count_documents(filter={})

        await ctx.channel.send(f"Okay, I've added **{amount}**{symbol} to **{count}** users. Please be careful Ethan")

    @commands.command(name="HYPERINFLATION", aliases=["inflate"])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def hyperinflation(self, ctx, currency = "", multi = 0.0):
        economy = self.bot.get_cog('Economy')
        types = ["tokens", "coins"]
        symbol = await economy.get_symbol(currency)

        if (ctx.author.id != 390601966423900162):
            await ctx.channel.send("Only Ethan can cause hyperinflation!")
            self.hyperinflation.reset_cooldown(ctx)
            return
        if (currency == ""):
            await ctx.channel.send("Well pick a currency to inflate, idiot")
            self.hyperinflation.reset_cooldown(ctx)
            return
        if (currency not in types):
            await ctx.channel.send(f"Ethan{currency.capitalize()}:tm: doesn't exist. Nice try!")
            self.hyperinflation.reset_cooldown(ctx)
            return
        if (multi <= 0.0):
            await ctx.channel.send("Canceling EthanCurrency, are you? Enter a number above 0 dumbass")
            self.hyperinflation.reset_cooldown(ctx)
            return
        elif (multi == 1.0):
            await ctx.channel.send("I mean, okay, sure, but you do realize this changes jackshit right")
            self.hyperinflation.reset_cooldown(ctx)
            return
        """
        elif (multi > 1.1):
            await ctx.channel.send("I have removed the limit!")
            await asyncio.sleep(20)
            await ctx.channel.send("AND REPLACED IT WITH 1.1X LMAO GET FUCKED")
            self.hyperinflation.reset_cooldown(ctx)
            return
        """

        data = {
            "$mul":
            {
                currency: multi
            }
        }
        self.bot.ethan_tokens.update_many(filter={currency:{"$not":{"$eq":0}}}, update=data)

        query = {
            "type": "currency"
        }
        cur_rate = self.bot.general_info.find_one(query)[f"{currency}_rate"]
        new_rate = cur_rate * multi
        # using f-string to select either "coins_rate" or "tokens_rate"
        data = {
            "$set": {
                f"{currency}_rate": new_rate
            }
        }
        self.bot.general_info.update_one(query, data)

        await ctx.channel.send(f"Okay, I've inflated {symbol} by {multi}.\nYour inflation rate is now **{new_rate:,.3f}**x.\nI hope you know what you're doing...")

    @commands.command(name="MURDERINFLATIONWITHARUSTYFUCKINGKNIFE")
    @commands.has_permissions(administrator=True)
    async def murder(self, ctx):
        murder = 0.001
        image="https://cms.qz.com/wp-content/uploads/2016/12/demon.jpg?quality=75&strip=all&w=1600&h=900&crop=1"
        data = {
            "$mul":
            {
                "tokens": murder
            }
        }
        self.bot.ethan_tokens.update_many(filter={"tokens":{"$not":{"$eq":0}}}, update=data)
        query = {
            "type": "currency"
        }
        cur_rate = self.bot.general_info.find_one(query)["tokens_rate"]
        new_rate = cur_rate * murder
        data = {
            "$set": {
                "tokens_rate": new_rate
            }
        }
        self.bot.general_info.update_one(query, data)
        await ctx.channel.send(image)
