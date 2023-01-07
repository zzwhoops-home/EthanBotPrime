import re
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
        # if (len(message.content) > 350):
        #     await message.channel.send(f"{message.author.mention} HEY TL;DR! THAT MESSAGE WAS {len(message.content)} characters!")
        if (message.content[:5].strip() == prefix):
            return
        if (self.bot.user.id != message.author.id):
            if re.search(r'\bmao\b', message.content.lower()):
                text = "Zedong Mao is the unique leader who is statesman, thinker, revolutionist, strategist, poet and penman in Chinese history. In all his life not only did he changed the Chinese history in 20 Century, but also had great effect on the world.\nThe collection of poker precious photo collection of Chairman Mao different periods, and valuable for collection. We will always cherish the memory of a great man, remember history!"
                await message.channel.send(text)
            msg = message.content.strip().lower()
            choices_all = ["no sex", "ethan!", "ethan lee!", "my king!", "love ethan lee", "ETHAN LEE!!!!!", ":hot_face:", "STAN ETHAN LEE!", "vote ethan gang", "ethan lee best boy", "ETHAN sdo[f-dsfpasfkhsalduhfluashdf uaudfsa", "wouhaoguhaeg"]
            if 'ethan' in msg and message.channel.id != 765710257753948190:
                x = random.randint(1, 200)
                if (x == 69):
                    for x in range(25):
                        choice = random.choice(choices_all)
                        await message.channel.send(choice)
                else:
                    choice = random.choice(choices_all)
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
                await message.channel.send("no u lmao")
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
                times = random.randint(1, 200)
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
            if "vaporeon" in msg:
                text = "Hey guys, did you know that in terms of male human and female Pokémon breeding, Vaporeon is the most compatible Pokémon for humans? Not only are they in the field egg group, which is mostly comprised of mammals, Vaporeon are an average of 3”03’ tall and 63.9 pounds, this means they’re large enough to be able handle human dicks, and with their impressive Base Stats for HP and access to Acid Armor, you can be rough with one. Due to their mostly water based biology, there’s no doubt in my mind that an aroused Vaporeon would be incredibly wet, so wet that you could easily have sex with one for hours without getting sore. They can also learn the moves Attract, Baby-Doll Eyes, Captivate, Charm, and Tail Whip, along with not having fur to hide nipples, so it’d be incredibly easy for one to get you in the mood. With their abilities Water Absorb and Hydration, they can easily recover from fatigue with enough water. No other Pokémon comes close to this level of compatibility. Also, fun fact, if you pull out enough, you can make your Vaporeon turn white. Vaporeon is literally built for human dick. Ungodly defense stat+high HP pool+Acid Armor means it can take cock all day, all shapes and sizes and still come for more"
                await message.channel.send(text)
            if "copium" in msg or "cope" in msg or "coping" in msg:
                await message.channel.send("https://pbs.twimg.com/media/FLTYc2FaUAAPzHp.jpg")
            if "chmiel" in msg:
                text = "huge ass, pumped full of blood, biceps... Not ass i meant biceps, just like the largest fucking biceps on earth... And its no longer a 2-split, no, it's fucking 4-split quadceps but for the arm just absolutely vascular"
                await message.channel.send(text)
            if "sound" in msg:
                text = "To the people who don’t know, sounding is a community where people are obsessed with random sounds. They are sort of like audiophiles in a way, but are known colloquially as “soundphiles”. I used to be apart of this community, it was fun, getting to learn about the noises around us. If you like “sounds” come and join the fellow “sounders” down at r/sounding"
                await message.channel.send(text)
            if re.search("\\b69\\b", message.content) is not None:
                text = "continual reorganization of the inner human body to surgically attatch the ending of the large intestine to the opening of the mouth, and then modifying the other ending of the large intestine to not point towards the rectum, but rather cross stitched towards the sexual organ of whatever subject is being performed upon"
                await message.channel.send(text)
            if "what the fuck" in msg:
                await message.channel.send("https://i.imgur.com/JeJQLMk.png")
            if "essential oils" in msg or "mlm" in msg:
                await message.channel.send("epic tessaro moment")
            if "cbt" in msg or "cock and ball torture" in msg:
                text = "Cognitive behavioral therapy (CBT) is a psycho-social intervention[1][2] that aims to reduce symptoms of various mental health conditions, primarily depression and anxiety disorders.[3] CBT focuses on challenging and changing cognitive distortions (such as thoughts, beliefs, and attitudes) and their associated behaviors to improve emotional regulation[2][4] and develop personal coping strategies that target solving current problems. Though it was originally designed to treat depression, its uses have been expanded to include the treatment of many mental health conditions, including anxiety,[5][6] substance use disorders, marital problems, and eating disorders.[7][8][9] CBT includes a number of cognitive or behavioral psychotherapies that treat defined psychopathologies using evidence-based techniques and strategies.[10][11][12]"
                await message.channel.send(text)
            if "turkey" in msg or "thanksgiving" in msg:
                await message.channel.send("https://i.imgur.com/IoWKuXR.png")
            if "40 clearview avenue" in msg:
                await message.channel.send("come for a good time")
            if "clearview" in msg:
                await message.channel.send("did i hear... clearview?")
                await asyncio.sleep(1)
                await message.channel.send("as in 40 clearview avenue???")
                await asyncio.sleep(2)
                await message.channel.send("come for a good time!!!")
                await asyncio.sleep(1)
            if "steve" in msg:
                text = "Anyone and everyone had become my target. Frenzy has overtaken me and I simply am now tethering on the edge--there is no escape, not even death. No blissful end shall greet me; only the sight of my deeds will bore into my soul."
                await message.channel.send(text)
            if "mwah" in msg:
                await message.channel.send(":kissing_heart:")
            if "thicc" in msg or "thick" in msg:
                await message.channel.send("thicc rhymes with zacc, it's also like ethan's thighs")
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
