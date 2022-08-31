import nextcord
from nextcord.ext import tasks, commands
import random
import asyncio

prefix = "eb!"


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.VIRAJ = False
        bot.SAM = False

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     for guild in bot.guilds:
    #         if guild.name == GUILD:
    #             break
    #     print(
    #         f'{bot.user} is connected to the following guild:\n'
    #         f'{guild.name} (id: {guild.id})\n'
    #     )
    
    @commands.Cog.listener()
    async def on_message(self, message):
        num = random.randint(1, 200)
        if num == 69:
            guild = message.author.guild
            role = guild.get_role(829155593322364959)
            role_members = role.members
            if message.author not in role_members and message.author.id == 501505695091392527:
                await message.channel.send(f"{message.author.mention} YOU SHOULD PLAY OSU")
        if (message.content[:5].strip() == prefix):
            return
        if (self.bot.user.id != message.author.id):                
            msg = message.content.strip().lower()
            choices_all = ["runfunc", "no sex", "ethan!", "ethan lee!", "my king!", "love ethan lee", "ETHAN LEE!!!!!", ":hot_face:", "STAN ETHAN LEE!", "vote ethan gang", "ethan lee best boy", "ETHAN sdo[f-dsfpasfkhsalduhfluashdf uaudfsa", "wouhaoguhaeg"]
            choices_ngan = ["sex", "sex??", "sex!"]
            if 'ethan' in msg and message.channel.id != 765710257753948190:
                if message.author.id == 597628340203028485:
                    await message.channel.send(random.choice(choices_ngan))
                else:
                    choice = random.choice(choices_all)
                    if (choice == "runfunc"):
                        string = "ethan"
                        for x in string:
                            await message.channel.send(f"GIVE ME A {x.capitalize()},")
                            await asyncio.sleep(0.7)
                        await message.channel.send(f"ETHAN LEE, ETHAN LEE!")
                        return
                    x = random.randint(1, 200)
                    if (x == 69):
                        for x in range(24):        
                            choice = random.choice(choices_all)            
                            if (choice == "runfunc"):
                                string = "ethan"
                                for x in string:
                                    await message.channel.send(f"GIVE ME A {x.capitalize()},")
                                    await asyncio.sleep(0.7)
                                await message.channel.send(f"ETHAN LEE, ETHAN LEE!")
                                continue
                            await message.channel.send(choice)
                    await message.channel.send(choice)
            if 'connor' in msg:
                await message.channel.send("ethan sex")
            if 'edge' in msg and 'play' in msg:
                await message.channel.send("ethedge ethplay ethgasm")
            if 'higgy' in msg:
                await message.channel.send("ethan be gettin' real jiggy")
            if 'sam' in msg and ('sister' in msg or 'your mom' in msg):
                await message.channel.send("<:sexualrelations:803707185963991081>")
                await message.channel.send("https://i.imgur.com/W5Fq6tn.png")
            if msg == 'ethan\'s insane announcement' and (message.channel.id == 765710257753948190):
                await message.channel.send("ethan's insane announcement")
            if 'china' in msg:
                await message.channel.send("荣耀归于中国")
            if 'egg' in msg:
                await message.channel.send("egg")
            if 'penis' in msg:
                await message.channel.send("lol penis")
            if 'sex' in msg:
                await message.channel.send("sex ( ͡° ͜ʖ ͡°)")
            if 'cock' in msg:
                await message.channel.send("https://i.imgur.com/d7X724S.png")
            if 'knowledge' in msg:
                await message.channel.send("https://www.youtube.com/watch?v=Cv1RJTHf5fk")
            if 'boris' in msg:
                await message.channel.send("BORIS JOHNSON")
            if 'johnson' in msg:
                await message.channel.send("JOHNSON? BORIS JOHNSON???")
            if 'putin' in message.content.lower():
                await message.channel.send("Putin.")
                await asyncio.sleep(1)
                await message.channel.send("Putin....")
                await asyncio.sleep(1)
                await message.channel.send("PUTIN DEEZ NUTS IN YOUR MOUTH")
            if 'kenneth' in msg:
                await message.channel.send("shit")
            if "nou" in message.content.lower().replace(" ", "") and "enough" not in message.content.lower().replace(" ", "") and message.channel.id != 765710257753948190:
                await message.channel.send("https://i.pinimg.com/originals/d5/8b/67/d58b67b83ffff03e8fd15583c91017fb.png")
                await message.channel.send("**NO U LMAO**")
            if "equality" in msg:
                await message.channel.send("Kenny Calls Commie-nism")
            if "communism works" in msg:
                await message.channel.send("Communism works, just ignore the concen....")
                await asyncio.sleep(2)
                await message.channel.send("Wait... who is that?")
                await asyncio.sleep(2)
                await message.channel.send("OH FUCK LUKE NO GET AWAY FROM ME")
                await asyncio.sleep(1)
                await message.channel.send("no what are you doing with that knife")
                await asyncio.sleep(3)
                await message.channel.send("OKAY COMMUNISM WORKS COMMUNISM WORKS ITS THE BEST GOVERNMENT SYSTEM THAT HAS EVER BEEN INVENTED")
            if "died" in msg:
                await asyncio.sleep(10)
                times = random.randint(1, 500)
                await message.channel.send("EGG " * times)
            if "issue" in msg:
                await message.channel.send("lmao skill issue")
            if "second amendment" in msg:
                await message.channel.send("Own a musket for home defense, since that's what the founding fathers intended. Four ruffians break into my house. \"What the devil?\" As I grab my powdered wig and Kentucky rifle. Blow a golf ball sized hole through the first man, he's dead on the spot. Draw my pistol on the second man, miss him entirely because it's smoothbore and nails the neighbors dog. I have to resort to the cannon mounted at the top of the stairs loaded with grape shot, \"Tally ho lads\" the grape shot shreds two men in the blast, the sound and extra shrapnel set off car alarms. Fix bayonet and charge the last terrified rapscallion.He Bleeds out waiting on the police to arrive since triangular bayonet wounds are impossible to stitch up, Just as the founding fathers intended")
            if "fail" in msg:
                await message.channel.send("https://i.imgur.com/315P6Fs.png")
            if "based" in msg:
                await message.channel.send("**BASED AF**")
                await message.channel.send("https://i.imgur.com/frSl0Uq.jpeg")
            if "slave" in msg or "incest" in msg or "secession" in msg:
                await message.channel.send("https://i.imgur.com/ATsdJxc.png")
            if "obama meme" in msg:
                await message.channel.send("https://i.kym-cdn.com/entries/icons/original/000/030/329/cover1.jpg")
            if "too many channels" in msg:
                await message.channel.send(f"Hey {message.author.mention} you little shit, there can never be enough channels!")
                await message.delete()
            if "gold plated pocket watch" in msg and "diamond encrusted monocle" in msg:
                await message.channel.send(f"Hey {message.author.mention}, fuck you rich kid!")
        if (message.author.id == 292448459909365760):
            if 'sad' in message.content.strip().lower():
                await message.channel.send("<:zzwhoops_cries:813585484441714698>")
        if (message.author.id == 390601966423900162):
            if 'scribbles notes' in message.content.lower():
                await message.channel.send("https://tenor.com/bi7Db.gif")
            msg = message.content.lower().replace(" ", "")
            if ("invisible hand" in msg):
                await message.channel.send("Aw fuck you ethan you're not the invisible hand you're a bitch")
            if ("whim" in msg):
                await message.channel.send("I'll invert your asshole on a whim dipshit")
            # viraj is about to start ranting and ethan would like to stop him
            if "radical" in msg:
                self.bot.VIRAJ = not self.bot.VIRAJ
                print(f"VIRAJ: {self.VIRAJ}")
            # sam is about to start saying something stupid and ethan would like to stop him
            if "boner" in msg:
                self.bot.SAM = not self.bot.SAM
                print(f"SAM: {self.bot.SAM}")
        if (message.author.id == 501505695091392527):
            if (self.bot.SAM):
                chance = random.randint(1, 100)
                if (chance <= 15):
                    await message.channel.send("https://tenor.com/view/who-asked-gif-21634393")
            if 'sister' in message.content:
                await message.channel.send("<:sexualrelations:803707185963991081>")
            if (message.channel.id == 537757338300317739):
                if 'parsfuk' in message.content.lower().replace(" ", ""):
                    for x in range(7):
                        await message.channel.send("https://tenor.com/bMkPz.gif")
                    embed = nextcord.Embed(title="No, Sam, #parsfuk **WILL NOT** be ***FUCKING LIBERATED***", description="__***DENIED***__")
                    await message.channel.send(embed=embed)
            if "fight" in message.content.lower().replace(" ", "") and "continue" in message.content.lower().replace(" ", ""):
                embed = nextcord.Embed(title="*Not after I'm done with you*...")
                await message.channel.send(embed=embed)
                await asyncio.sleep(2)
                await message.channel.send(f"**Acquiring location of user {message.author.mention}...**")
                await asyncio.sleep(5)
                await message.channel.send("**Location found!**")
                await asyncio.sleep(1)
                await message.channel.send("https://www.google.com/maps/place/56+Leigh+Ave,+Princeton,+NJ+08540/")
            if "xd" in message.content.lower().replace(" ", "") or "haha" in message.content.lower().replace(" ", ""):
                embed = nextcord.Embed(title="Aw fuck you sam go suck a lemon", description="STFU or im taking away your ethan tokens")
                await message.channel.send(embed=embed)
        if (message.author.id == 712420717685112863):
            if (self.bot.VIRAJ):
                chance = random.randint(1, 100)
                if (chance <= 15):
                    await message.channel.send("https://tenor.com/view/who-asked-gif-21634393")
