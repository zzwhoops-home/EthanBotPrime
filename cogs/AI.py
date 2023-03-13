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
                "money_spent": usage / 500000,
                "eai_gen": 1 if type == "eai" else 0,
                "nai_gen": 1 if type == "nai" else 0,
                "lai_gen": 1 if type == "lai" else 0,
                "aai_gen": 1 if type == "aai" else 0,
                "sai_gen": 1 if type == "sai" else 0
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
        if (length > 200):
            await ctx.channel.send(f"{ctx.author.mention} Hey, try to keep your requests under 200 characters.")
            return

        # default "training" prompt
        default_prompt = "Answer as EthanBot, a chatbot that answers as rudely as possible. EthanBot always attempts to give a definitive answer to questions, accompanied with personal, insulting attacks."
        user_prompt = f"{message}"
        max_tokens = 256

        # customize response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": default_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=1,
            max_tokens=max_tokens,
            presence_penalty=0
        )
        
        # convert to json, extract text with no new lines
        response_json = json.loads(str((response)))
        text = response_json['choices'][0]['message']['content'].strip()

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
        if (length > 200):
            await ctx.channel.send(f"{ctx.author.mention} Hey, try to keep your requests under 200 characters.")
            return

        # default "training" prompt
        default_prompt = "Answer as EthanBot, a chatbot."
        user_prompt = f" {message}"
        max_tokens = 256

        # customize response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": default_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=max_tokens,
            presence_penalty=0
        )
        
        # convert to json, extract text with no new lines
        response_json = json.loads(str((response)))
        text = response_json['choices'][0]['message']['content'].strip()

        await ctx.channel.send(f"{ctx.author.mention} {text}")

        usage = int(response_json['usage']['total_tokens'])
        
        # update db with usage stats
        await self.update_ai_db(usage, "nai")

        # snarky response if AI response is cut off
        if (usage >= max_tokens):
            await ctx.channel.send(f"{ctx.author.mention} Hey, this response may be cut off due to API limitations!")
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
        if (length > 200):
            await ctx.channel.send(f"{ctx.author.mention} Hey, try to keep your requests under 200 characters.")
            return

        # default "training" prompt
        default_prompt = "Answer as EthanBot, a chatbot, who responds as helpfully and cheerfully as possible, including personal, encouraging, uplifting messages."
        user_prompt = f" {message}"
        max_tokens = 256

        # customize response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": default_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6,
            max_tokens=max_tokens
        )
        
        # convert to json, extract text with no new lines
        response_json = json.loads(str((response)))
        text = response_json['choices'][0]['message']['content'].strip()

        await ctx.channel.send(f"{ctx.author.mention} {text}")

        usage = int(response_json['usage']['total_tokens'])
        
        # update db with usage stats
        await self.update_ai_db(usage, "lai")

        # snarky response if AI response is cut off
        if (usage >= max_tokens):
            await ctx.channel.send(f"{ctx.author.mention} Hey, this response may be cut off due to API limitations!")
            return

    @commands.command(name="andyai", aliases=["aai"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def andy_ai(self, ctx, *message: str):
        length = -1
        for word in message:
            length += len(word) + 1
        if (length == -1):
            await ctx.channel.send(f"{ctx.author.mention} uh so what like did you want to ask me?")
            return
        if (length > 200):
            await ctx.channel.send(f"{ctx.author.mention} hey like try to keep it under like 200 like characters")
            return

        # default "training" prompt
        default_prompt = "Answer as a frustrated teenager, Andy. Use the filler word 'like' even when it doesn't make sense, and do so frequently. Use 'fuck', 'bitch', and 'shit' frequently. Do not capitalize, punctuate, or use commas."
        user_prompt = f"{message}"
        max_tokens = 256

        # customize response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": default_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=1,
            max_tokens=max_tokens,
            presence_penalty=0
        )
        
        # convert to json, extract text with no new lines
        response_json = json.loads(str((response)))
        text = response_json['choices'][0]['message']['content'].strip()

        await ctx.channel.send(f"{ctx.author.mention} {text}")

        usage = int(response_json['usage']['total_tokens'])
        
        # update db with usage stats
        await self.update_ai_db(usage, "aai")

        # snarky response if AI response is cut off
        if (usage >= max_tokens):
            await ctx.channel.send(f"{ctx.author.mention} Hey like you're gonna make me go broke in API cash so like stop please")
            return

    @commands.command(name="shakespeareai", aliases=["sai"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def old_ai(self, ctx, *message: str):
        length = -1
        for word in message:
            length += len(word) + 1
        if (length == -1):
            await ctx.channel.send(f"{ctx.author.mention} What did you want to ask me?")
            return
        if (length > 200):
            await ctx.channel.send(f"{ctx.author.mention} 200 characters and below, please.")
            return

        # default "training" prompt
        default_prompt = "Reply comedically, in Shakespearean English."
        user_prompt = f"{message}"
        max_tokens = 150

        # customize response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": default_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=1,
            max_tokens=max_tokens,
            presence_penalty=0
        )
        
        # convert to json, extract text with no new lines
        response_json = json.loads(str((response)))
        text = response_json['choices'][0]['message']['content'].strip()

        await ctx.channel.send(f"{ctx.author.mention} {text}")

        usage = int(response_json['usage']['total_tokens'])
        
        # update db with usage stats
        await self.update_ai_db(usage, "sai")

        # snarky response if AI response is cut off
        if (usage >= max_tokens):
            await ctx.channel.send(f"{ctx.author.mention} Hey asshole, if this response is cut off, it's to prevent me from going broke in API cash.")
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
        aai = stats['aai_gen']
        sai = stats['sai_gen']
        total_uses = eai + nai + lai + aai + sai
        tokens_used = stats['tokens_used']
        money_spent = stats['money_spent']

        query = {
            "type": "currency"
        }
        rates = self.bot.general_info.find_one(query)
        tokens_rate = rates["tokens_rate"]
        tokens_amount = tokens_rate * money_spent

        description = f"**Total snarky responses:** {eai}\n**Total normal responses:** {nai}\n**Total loving responses:** {lai}\n**Total Andeth responses:** {aai}\n**Total Shakespearean responses:** {sai}\n**Total responses:** {total_uses}\n\n**Tokens used:** {tokens_used:,}\n**Money spent :money_with_wings::** ${money_spent:,.4f} ({tokens_amount:,.4g}{tokens_symbol})"

        embed=nextcord.Embed(title="**EthanAI Usage Statistics**", description=description)

        await ctx.channel.send(embed=embed)