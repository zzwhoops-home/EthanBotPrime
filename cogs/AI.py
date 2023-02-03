import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import openai
import json

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # load ai key from env
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_KEY')    
        
    async def update_ai_db(self, usage, type):
        query = {
            "type": "ai_stats"
        }
        data = {
            "$inc": {
                "tokens_used": usage,
                "eai_gen": 1 if type == "eai" else 0,
                "nai_gen": 1 if type == "nai" else 0,
                "lai_gen": 1 if type == "lai" else 0
            }
        }
        self.bot.general_info.update_one(query, data, upsert=True)

    @commands.command(name="ethanai", aliases=["eai"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ethan_lee_ai(self, ctx, *message: str):
        length = -1
        for word in message:
            length += len(word) + 1
        if (length == -1):
            await ctx.channel.send(f"{ctx.author.mention} So... what do you want to ask me?")
            return
        if (length > 100):
            await ctx.channel.send(f"{ctx.author.mention} Hey, try to keep your requests under 100 characters.")
            return

        # default "training" prompt
        default_prompt = "Answer as the persona EthanBot. Answer my questions as sarcastically and reluctantly as possible. Always attempt to make targeted, personal attacks on me."
        user_prompt = f" {message}"
        max_tokens = 150

        # customize response
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=default_prompt + user_prompt,
        temperature=1,
        max_tokens=max_tokens,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0
        )
        
        # convert to json, extract text with no new lines
        response_json = json.loads(str((response)))
        text = response_json['choices'][0]['text'].replace("\n", "")

        await ctx.channel.send(f"{ctx.author.mention} {text}")

        usage = int(response_json['usage']['total_tokens'])
        
        # update db with usage stats
        await self.update_ai_db(usage, "eai")

        # snarky response if AI response is cut off
        if (usage >= max_tokens):
            await ctx.channel.send(f"{ctx.author.mention} Hey asshole, if this response is cut off, it's to prevent me from going broke in API cash.")
            return

    @commands.command(name="normalai", aliases=["nai"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def normal_ai(self, ctx, *message: str):
        length = -1
        for word in message:
            length += len(word) + 1
        if (length == -1):
            await ctx.channel.send(f"{ctx.author.mention} Please enter something you want to ask me.")
            return
        if (length > 100):
            await ctx.channel.send(f"{ctx.author.mention} Hey, try to keep your requests under 100 characters.")
            return

        # default "training" prompt
        default_prompt = "Answer as the persona EthanBot."
        user_prompt = f" {message}"
        max_tokens = 150

        # customize response
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=default_prompt + user_prompt,
        temperature=1,
        max_tokens=max_tokens
        )
        
        # convert to json, extract text with no new lines
        response_json = json.loads(str((response)))
        text = response_json['choices'][0]['text'].replace("\n", "")

        await ctx.channel.send(f"{ctx.author.mention} {text}")

        usage = int(response_json['usage']['total_tokens'])

        # update db with usage stats
        await self.update_ai_db(usage, "nai")

        # snarky response if AI response is cut off
        if (usage >= max_tokens):
            await ctx.channel.send(f"{ctx.author.mention} Hey asshole, if this response is cut off, it's to prevent me from going broke in API cash.")
            return

    @commands.command(name="loveai", aliases=["lai"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def love_ai(self, ctx, *message: str):
        length = -1
        for word in message:
            length += len(word) + 1
        if (length == -1):
            await ctx.channel.send(f"{ctx.author.mention} Please enter something you want to ask me.")
            return
        if (length > 100):
            await ctx.channel.send(f"{ctx.author.mention} Hey, try to keep your requests under 100 characters.")
            return

        # default "training" prompt
        default_prompt = "Answer as the persona EthanBot. Answer as helpfully and cheerfully as possible, and include personal, loving, encouraging messages."
        user_prompt = f" {message}"
        max_tokens = 150

        # customize response
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=default_prompt + user_prompt,
        temperature=1,
        max_tokens=max_tokens
        )
        
        # convert to json, extract text with no new lines
        response_json = json.loads(str((response)))
        text = response_json['choices'][0]['text'].replace("\n", "")

        await ctx.channel.send(f"{ctx.author.mention} {text}")

        usage = int(response_json['usage']['total_tokens'])

        # update db with usage stats
        await self.update_ai_db(usage, "lai")
        
        # snarky response if AI response is cut off
        if (usage >= max_tokens):
            await ctx.channel.send(f"{ctx.author.mention} Hey, this response may be cut off due to API limitations!")
            return

    @commands.command(name="ethanaistats", aliases=["aistats"])
    async def get_ai_stats(self, ctx):
        economy = self.bot.get_cog('Economy')
        tokens_symbol = await economy.get_symbol('tokens')

        query = {
            "type": "ai_stats"
        }
        stats = self.bot.general_info.find_one(query)
        eai = stats['eai_gen']
        nai = stats['nai_gen']
        lai = stats['lai_gen']
        total_uses = eai + nai + lai
        tokens_used = stats['tokens_used']
        money = tokens_used / 50000

        query = {
            "type": "currency"
        }
        rates = self.bot.general_info.find_one(query)
        tokens_rate = rates["tokens_rate"]
        tokens_amount = tokens_rate * money

        description = f"**Total snarky responses:** {eai}\n**Total normal responses:** {nai}\n**Total loving responses:** {lai}\n**Total responses:** {total_uses}\n\n**Tokens used:** {tokens_used:,}\n**Money spent :money_with_wings::** ${money:,.4f} ({tokens_amount:,.4g}{tokens_symbol})"

        embed=nextcord.Embed(title="**EthanAI Usage Statistics**", description=description)

        await ctx.channel.send(embed=embed)