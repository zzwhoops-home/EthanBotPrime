# import nextcord
# from nextcord import SelectOption, ButtonStyle
# from nextcord.ext import tasks, commands
# from nextcord.interactions import Interaction, InteractionResponse
# from nextcord.ui import button, View, Button, Select, TextInput, Modal
# import pymongo
# from pymongo import MongoClient

# import os
# import asyncio
# import math
# import random
# from datetime import datetime, timedelta, time, timezone

# class BuyStocks(Select):
#     options = []
#     stocks = bot.stock_info.find()
#     tokens_rate = 0.0

#     def __init__(self, tokens_rate):
#         self.tokens_rate = tokens_rate

#         for stock in self.stocks:
#             name = stock['name']
#             converted_price = stock['price'] * self.tokens_rate
#             currency = stock['currency']
#             if (currency == 'USX'):
#                 converted_price /= 100
#             description = f"{converted_price:,.2f}/unit\n"
#             self.options.append(SelectOption
#                 (
#                     label = name,
#                     description = description,
#                     emoji = bot.token_symbol
#                 )
#             )
#         super().__init__(
#             placeholder = "Select a stock option!",
#             options = self.options,
#             row = 1
#         )

#     async def callback(self, interaction: Interaction):
#         view: BuyStocksView = self.view
#         view.continue_prompt = True
#         view.stop()
#         view.name = self.values[0]
#         view.stock = bot.stock_info.find_one({'name': view.name})
#         view.symbol = view.stock['symbol']
#         view.converted_price = view.stock['price'] * self.tokens_rate
#         if (view.stock['currency'] == 'USX'):
#             view.converted_price /= 100
#         embed = nextcord.Embed(title = f"Buying **{view.name}**:", description = f"How many units would you like to purchase? (Type 'max' for basically your entire balance)\n(`{view.converted_price:,.2f}`{bot.token_symbol}/unit)")
#         await interaction.response.send_message(embed=embed)

# class BuyStocksView(View):    
#     name = ""
#     stock = {}
#     symbol = ""
#     converted_price = 0.0
#     continue_prompt = False

#     def __init__(self, tokens_rate, timeout=30):
#         self.tokens_rate = tokens_rate
#         super().__init__(timeout=timeout)

#         self.add_item(BuyStocks(tokens_rate))

#     async def on_timeout(self):
#         self.stop()

#     async def on_error(self, interaction, select):
#         await interaction.channel.send_message("lmao u suck")

# class Stocks(commands.Cog):
#     good_names = ["Crude Oil", "Gold", "Wheat", "Corn", "Ethanol"]
#     symbols = "CL=F,GC=F,ZW=F,ZC=F,CU=F"
#     base_rate = 12
#     tokens_rate = base_rate

#     def __init__(self, bot):
#         self.bot = bot
#         self.refresh_stocks.start()

#     async def create_stock_account(self, ctx, member = None):
#         if (member == None):
#             member = ctx.author
#         await ctx.channel.send(f"No stock account found for {member.mention}. Creating...")
#         data = {
#             "id": member.id,
#             "name": f"{member.name}#{member.discriminator}",
#             "stock_data": {}
#         }
#         print(data)
#         await asyncio.sleep(1)
#         await ctx.channel.send(f"Account created!")
#         bot.user_stocks.insert_one(data)        

#     @commands.command(name="stocks", aliases=["stock", "stonk", "stonks"])
#     @commands.cooldown(1, 5, commands.BucketType.user)
#     async def stocks(self, ctx, choice=""):
#         async def update_rate():
#             self.tokens_rate = self.base_rate * bot.general_info.find_one({"type": "currency"})["tokens_rate"]

#         async def view_stocks(ctx):
#             await update_rate()

#             stocks = list(bot.stock_info.find())

#             query = {
#                 "id": ctx.author.id
#             }
#             user_stocks = bot.user_stocks.find_one(query)
#             if (user_stocks == None):
#                 await self.create_stock_account(ctx)
#                 stock_data = {}
#             else:
#                 stock_data = user_stocks["stock_data"]

#             description = f"**Conversion Rate**: `{self.tokens_rate:,.2f}`{self.bot.token_symbol}/USD\n\n"

#             for stock in stocks:
#                 symbol = stock['symbol'].replace('=F', '')
#                 name = stock['name']
#                 price = stock['price']
#                 currency = stock['currency']
#                 if (currency == 'USX'):
#                     price /= 100
#                 converted_price = price * self.tokens_rate
#                 description += f"({symbol}) **{name}**: `{converted_price:,.2f}`{self.bot.token_symbol}/**unit** - ($`{price:,.2f}`)\n"

#             query = {"type": "stocks"}
#             last_update = bot.general_info.find_one(query)['update_time']
#             date_time = last_update.strftime("%m/%d/%Y %I:%M:%S %p")
#             description += f"\n**Data last updated at:** {date_time}\n\n**Stock Inventory:**"

#             print(stock_data)
#             if (stock_data == {}):
#                 description += f"\n`You haven't bought any shares.`"
#             else:
#                 for stock in stocks:
#                     name = stock['name']
#                     price = stock['price']
#                     currency = stock['currency']
#                     if (currency == 'USX'):
#                         price /= 100

#                     if (name in stock_data.keys() and float(stock_data[name]) != 0.0):
#                         shares = stock_data[name]
#                         total_value_usd = shares * price
#                         total_value_tokens = total_value_usd * self.tokens_rate
#                         description += f"\n**{name}**: `{shares:,.3f}`**u** worth `{total_value_tokens:,.2f}`{bot.token_symbol} ($`{total_value_usd:,.2f}`)"

#             embed = nextcord.Embed(title=f"{ctx.author.name}'s Stonks", description=description)
#             await ctx.channel.send(embed=embed)

#         async def buy_stocks(ctx):
#             economy = self.bot.get_cog('Economy')
#             member = ctx.author

#             query = {"id": ctx.author.id}
#             user = bot.ethan_tokens.find_one(query)
#             if user == None:
#                 await economy.create_token_account(ctx, ctx.author)
#             bal = user['tokens']

#             if (bal == 0):
#                 await ctx.channel.send(f"{ctx.author.mention} Get outta here, broke ass. You need {self.bot.token_symbol} to purchase stocks.")
#                 return

#             view = BuyStocksView(self.tokens_rate)
#             await ctx.channel.send("**BUYING STOCKS**", view=view)
#             await view.wait()
#             if (not view.continue_prompt):
#                 return

#             def check(m):
#                 return (
#                     m.author == member
#                     and m.channel == ctx.channel
#                 )
#             try:
#                 msg = await self.bot.wait_for (
#                     "message",
#                     timeout=15,
#                     check=check
#                 )
#                 if msg:
#                     # take floor to nearest millionth or whatever precision is set to
#                     precision = 0.000001
#                     if (msg.content.lower() == "max"):
#                         amount = (bal / view.converted_price) // precision * precision
#                     else:
#                         try:
#                             amount = float(msg.content)
#                         except ValueError:
#                             await ctx.channel.send(f"Hey dumbass you can't buy {msg.content} units of {view.name}")
#                             return
#             except asyncio.TimeoutError:
#                 await ctx.channel.send("Well give me a number, don't just stare at me like that you creep", delete_after=10)
#                 return

#             total_price = amount * view.converted_price
#             # return if the user doesn't have enough money.
#             if (bal < total_price):
#                 await ctx.channel.send(f"lmao you don't have enough money fool, you need **{total_price:,.2f}**{bot.token_symbol} to buy **{amount:,.3f}** units of {view.name}")
#                 return
#             new_balance = bal - total_price
            
#             # create user stocks collection if it doesn't exist, populate with data
#             query = {
#                 "id": member.id  
#             }
#             user = bot.user_stocks.find_one(query)
#             if (user == None):
#                 await self.create_stock_account(ctx)
#                 new_stocks = {}
#             else:
#                 # two variables in case we want to show the user how many shares they had previously
#                 cur_stocks = user["stock_data"]
#                 new_stocks = cur_stocks

#             if (view.name not in new_stocks.keys() or float(new_stocks[view.name]) == 0.0):
#                 new_stocks[view.name] = amount
#             else:
#                 new_stocks[view.name] += amount

#             data = {
#                 "$set": {
#                     "name": f"{member.name}#{member.discriminator}",
#                     "stock_data": new_stocks
#                 }
#             }
#             bot.user_stocks.update_one(query, data)

#             # withdraw from user balance
#             data = {
#                 "$set": {
#                     "tokens": new_balance
#                 }
#             }
#             bot.ethan_tokens.update_one(query, data)

#             embed = nextcord.Embed(title=f"Purchased **{view.name}** ({view.stock['symbol']})", description=f"**Total**: `{amount:,.3f}`u for **`{total_price:,.2f}`**{bot.token_symbol} (`{view.converted_price:,.2f}`{bot.token_symbol}/unit)\n**You now have: `{new_balance:,.2f}`**{bot.token_symbol}")
#             await ctx.channel.send(embed=embed)
#             return

#         if (choice == ""):
#             await ctx.channel.send("Bro you gotta tell me what you want to do,\nimagine if you went up to your teacher and\nasked hey, how do you stonks?\nDo you want to 'view', 'buy' or 'sell' your stocks?")
#         if (choice == "view"):
#             await view_stocks(ctx)
#         if (choice == "buy"):
#             await buy_stocks(ctx)

#     @tasks.loop(hours=8)
#     async def refresh_stocks(self):
#         now = datetime.now()
#         print("Refreshing stocks at " + str(now))
#         query = {"type": "stocks"}
#         data = {
#             "$set": {
#                 "update_time": now
#             }
#         }
#         bot.general_info.find_one_and_update(query, data, upsert=True)

#         url = "https://yfapi.net/v6/finance/quote"
#         querystring = {"symbols": self.symbols}
#         headers = {
#             'x-api-key': bot.STOCKS_API_KEY
#             }
#         response = requests.request("GET", url, headers=headers, params=querystring)

#         try:
#             formatted = response.json()['quoteResponse']['result']
#             for good in formatted:
#                 symbol = good['symbol']
#                 name = good['shortName']
#                 currency = good['currency']
#                 price = round(good['regularMarketPrice'], 2)
                
#                 for good_name in self.good_names:
#                     if (good_name in name):
#                         name = good_name
#                         break

#                 query = {
#                     "symbol": symbol
#                 }
#                 data = {
#                     "symbol": symbol,
#                     "name": name,
#                     "currency": currency,
#                     "price": price
#                 }
#                 bot.stock_info.find_one_and_replace(query, data, upsert=True)
#         except KeyError as e:
#             print(f"Thingy happened with stonks: {e.message}")
#             return


#     @refresh_stocks.before_loop
#     async def before_refresh(self):
#         # wait until X:00:00
#         now = datetime.utcnow().replace(tzinfo=timezone.utc)
#         start = datetime.combine((now + timedelta(hours=1)).date(), time((now + timedelta(hours=1)).time().hour, 0, 0)).replace(tzinfo=timezone.utc)
#         wait_seconds = (start - now).total_seconds()
#         print("Waiting " + str(wait_seconds) + " before starting refresh.")
        
#         await asyncio.sleep(wait_seconds)
