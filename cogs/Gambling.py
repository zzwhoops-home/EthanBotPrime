import nextcord
from nextcord.ext import tasks, commands
import pymongo
from pymongo import MongoClient

import os
import asyncio
import math
import random
from datetime import datetime, timedelta, time, timezone

class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="luckynumbers", aliases=["lnums", "ln", "luckynums"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def lucky_numbers(self, ctx, currency = "", amount = ""):
        economy = self.bot.get_cog('Economy')
        types = ["tokens", "coins"]
        symbol = await economy.get_symbol(currency)
        
        if (currency not in types):
            await ctx.channel.send(f"{ctx.author.mention} Ethan{currency.capitalize()}:tm: doesn't exist. Nice try! Type 'coins' or 'tokens'.")
            self.lucky_numbers.reset_cooldown(ctx)
            return
        balance = self.bot.ethan_tokens.find_one({"id": ctx.author.id})[currency]
        try:
            amount = float(amount)
        except ValueError:
            if (amount == "all"):
                amount = balance
            else:
                await ctx.channel.send(f"{ctx.author.mention} tf is {amount}{symbol}?")
                return
        if (amount <= 0.0):
            await ctx.channel.send(f"{ctx.author.mention} You have to gamble some amount of tokens or coins.\nBroke ass lil shit lmao")
            return
        
        if (balance < amount):
            await ctx.channel.send(f"{ctx.author.mention} You don't have that much money idiot")
            return
        await ctx.channel.send(f"{ctx.author.mention} Gambling **{amount:,.4g}**{symbol}. Choose a number from **1-10**! Type 'e' to exit.")

        def check(m):
            return (
                m.channel.id == ctx.channel.id
                and m.author.id == ctx.author.id
            )
        try:
            guess = await self.bot.wait_for("message", check=check, timeout=30.0)
            guess = guess.content
            if (guess.strip().lower() == "e"):
                await ctx.channel.send(f"{ctx.author.mention} lmao pussy :chicken:")
                return
            if not (int(guess) <= 10 and int(guess) >= 0):
                await ctx.channel.send(f"{ctx.author.mention} Enter a number between 1 and 10.")
                return

            number = random.randint(1, 10)
            difference = abs(int(number) - int(guess))

            await ctx.channel.send(f"{ctx.author.mention} The number was **{number}**. Your guess, **{guess}** was **{difference}** off.")

            if (difference == 0):
                percent = random.randint(250, 600)
                change = amount * (percent / 100)
                await ctx.channel.send("https://ih1.redbubble.net/image.724682828.9041/flat,1000x1000,075,f.jpg")
                await ctx.channel.send(f"{ctx.author.mention} Spot on! Congratulations, you've won **{(change - amount):,.4g}**{symbol} (**{amount:,.4g}** --> **{change:,.4g}**) *({(percent / 100):.2f}x)*.")
            elif (difference == 1):
                percent = random.randint(125, 165)
                change = amount * (percent / 100)
                await ctx.channel.send(f"{ctx.author.mention} I mean, you were pretty close. You get... a lil bit: **{(change - amount):,.4g}**{symbol} (**{amount:,.4g}** --> **{change:,.4g}**) *({(percent / 100):.2f}x)*.")
            elif (difference == 2 or difference == 3):
                percent = random.randint(30, 99)
                change = amount * (percent / 100)
                await ctx.channel.send(f"{ctx.author.mention} You weren't that close, so I'll just give you some of your money back: **{(change - amount):,.4g}**{symbol} (**{amount:,.4g}** --> **{change:,.4g}**) *({(percent / 100):.2f}x)*.")
            else:
                change = 0
                await ctx.channel.send("https://i.imgur.com/BSSVwl6.png")
                await ctx.channel.send(f"{ctx.author.mention} lmao you suck, I'll be taking **{amount:,.4g}**{symbol}")

            member = ctx.author
            new_balance = balance + (change - amount)
            if (currency == "tokens"):
                query = {
                    "id": member.id
                }
                data = {
                    "$set":
                    {
                        "name": f"{member.name}#{member.discriminator}",
                        "tokens": new_balance
                    }
                }
            elif (currency == "coins"):
                query = {
                    "id": member.id
                }
                data = {
                    "$set":
                    {
                        "name": f"{member.name}#{member.discriminator}",
                        "coins": new_balance
                    }
                }
            self.bot.ethan_tokens.update_one(query, data)
                
            await asyncio.sleep(1)
            await ctx.channel.send(f"{ctx.author.mention} You now have **{new_balance:,.4g}**{symbol}")
        except asyncio.TimeoutError:
            await ctx.channel.send("{ctx.author.mention} Type at most **TWO NUMBERS** in *30* seconds **ITS NOT THAT HARD**.\nI should just take your money but... that would be a scam. EthanBot does not scam.")    
