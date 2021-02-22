class SELFBOT():
    __version__ = 2.0

import discord, subprocess, sys, time, os, colorama, base64, codecs, datetime, io, random, numpy, datetime, smtplib, string, ctypes, sys
import urllib.parse, urllib.request, re, json, requests, webbrowser, aiohttp, asyncio, functools, logging, os, io, aiohttp, asyncio, datetime, requests, json, pypresence
import requests as req

from threading import Thread as thr
from colorama import Fore as Color

from discord.ext import commands, tasks
from bs4 import BeautifulSoup as bs4
from urllib.parse import urlencode
from pymongo import MongoClient
from selenium import webdriver
from threading import Thread
from subprocess import call
from itertools import cycle
from colorama import Fore
from sys import platform
from PIL import Image
from gtts import gTTS

#config
with open('config.json') as f:
    config = json.load(f)

token = config.get('token')
password = config.get('password')
prefix = config.get('prefix')
message_logger = config.get('mention_logger')

giveaway_sniper = config.get('giveaway_sniper')
slotbot_sniper = config.get('slotbot_sniper')
nitro_sniper = config.get('nitro_sniper')
privnote_sniper = config.get('privnote_sniper')

stream_url = config.get('stream_url')
tts_language = config.get('tts_language')

width = os.get_terminal_size().columns
start_time = datetime.datetime.utcnow()
loop = asyncio.get_event_loop()

languages = {
    'hu'    : 'Hungarian, Hungary',
    'nl'    : 'Dutch, Netherlands',
    'no'    : 'Norwegian, Norway',
    'pl'    : 'Polish, Poland',
    'pt-BR' : 'Portuguese, Brazilian, Brazil',
    'ro'    : 'Romanian, Romania',
    'fi'    : 'Finnish, Finland',
    'sv-SE' : 'Swedish, Sweden',
    'vi'    : 'Vietnamese, Vietnam',
    'tr'    : 'Turkish, Turkey',
    'cs'    : 'Czech, Czechia, Czech Republic',
    'el'    : 'Greek, Greece',
    'bg'    : 'Bulgarian, Bulgaria',
    'ru'    : 'Russian, Russia',
    'uk'    : 'Ukranian, Ukraine',
    'th'    : 'Thai, Thailand',
    'zh-CN' : 'Chinese, China',
    'ja'    : 'Japanese',
    'zh-TW' : 'Chinese, Taiwan',
    'ko'    : 'Korean, Korea'
}

locales = [
    "da", "de",
    "en-GB", "en-US",
    "es-ES", "fr",
    "hr", "it",
    "lt", "hu",
    "nl", "no",
    "pl", "pt-BR",
    "ro", "fi",
    "sv-SE", "vi",
    "tr", "cs",
    "el", "bg",
    "ru", "uk",
    "th", "zh-CN",
    "ja", "zh-TW",
    "ko"
]

m_numbers = [
    ":one:",
    ":two:",
    ":three:",
    ":four:",
    ":five:",
    ":six:"
]

m_offets = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1)
]

def async_executor():
    def outer(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            thing = functools.partial(func, *args, **kwargs)
            return loop.run_in_executor(None, thing)

        return inner

    return outer

@async_executor()
def do_tts(message):
    f = io.BytesIO()
    tts = gTTS(text=message.lower(), lang=tts_language)
    tts.write_to_fp(f)
    f.seek(0)
    return f

def searchq(link):
    return f"https://google.com/search?q={link}".replace(" ", "+")

def Clear():
    os.system('cls')
Clear()

def Nitro():
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return f'https://discord.gift/{code}'

def Init():
    if config.get('token') == "token-here":
        Clear()
        print(f"{Fore.RED}[ERROR] {Fore.YELLOW}You didnt put your token in config.json"+Fore.RESET)
    else:
        token = config.get('token')
        try:
            bot.run(token, bot=False, reconnect=True)
            os.system(f'title (Terminal Selfbot) - Version {SELFBOT.__version__}')
        except discord.errors.LoginFailure:
            print(f"{Fore.RED}[ERROR] {Fore.YELLOW}Improper token has been passed"+Fore.RESET)
            os.system('pause >NUL')

def GmailBomber():
    _smpt = smtplib.SMTP('smtp.gmail.com', 587)
    _smpt.starttls()
    username = input('Gmail: ')
    password = input('Gmail Password: ')
    try:
        _smpt.login(username, password)
    except:
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW} Incorrect Password or gmail, make sure you've enabled less-secure apps access"+Fore.RESET)
    target = input('Target Gmail: ')
    message = input('Message to send: ')
    counter = eval(input('Ammount of times: '))
    count = 0
    while count < counter:
        count = 0
        _smpt.sendmail(username, target, message)
        count += 1
    if count == counter:
        pass


bot = commands.Bot(command_prefix=prefix, self_bot=True, case_insensitive=True, intents=discord.Intents.all())
bot.remove_command('help')
mention_logger: True
bot.copycat = None
bot.msgsniper = True
bot.slotbot_sniper = True
bot.giveaway_sniper = True
bot.mee6 = False
bot.mee6_channel = None
bot.sniped_message_dict = {}
bot.sniped_edited_message_dict = {}

#events
@bot.event
async def on_command_error(ctx, error):
    error_str = str(error)
    error = getattr(error, 'original', error)
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CheckFailure):
        await ctx.send('[ERROR]: You\'re missing permission to execute this command', delete_after=3)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"[ERROR]: Missing arguments: {error}", delete_after=3)
    elif isinstance(error, numpy.AxisError):
        await ctx.send('Invalid Image', delete_after=3)
    elif isinstance(error, discord.errors.Forbidden):
        await ctx.send(f"[ERROR]: 404 Forbidden Access: {error}", delete_after=3)
    elif "Cannot send an empty message" in error_str:
        await ctx.send('[ERROR]: Message contents cannot be null', delete_after=3)
    else:
       await ctx.send(f'[ERROR]: {error_str}', delete_after=3)


@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)


@bot.event
async def on_message(message):
    if bot.copycat is not None and bot.copycat.id == message.author.id:
        await message.channel.send(chr(173) + message.content)


    def GiveawayData():
        print(
        f"{Fore.WHITE} - CHANNEL: {Fore.YELLOW}[{message.channel}]"
        f"\n{Fore.WHITE} - SERVER: {Fore.YELLOW}[{message.guild}]"
    +Fore.RESET)

    def SlotBotData():
        print(
        f"{Fore.WHITE} - CHANNEL: {Fore.YELLOW}[{message.channel}]"
        f"\n{Fore.WHITE} - SERVER: {Fore.YELLOW}[{message.guild}]"
    +Fore.RESET)

    def NitroData(elapsed, code):
        print(
        f"{Fore.WHITE} - CHANNEL: {Fore.YELLOW}[{message.channel}]"
        f"\n{Fore.WHITE} - SERVER: {Fore.YELLOW}[{message.guild}]"
        f"\n{Fore.WHITE} - AUTHOR: {Fore.YELLOW}[{message.author}]"
        f"\n{Fore.WHITE} - ELAPSED: {Fore.YELLOW}[{elapsed}]"
        f"\n{Fore.WHITE} - CODE: {Fore.YELLOW}{code}"
    +Fore.RESET)

    def PrivnoteData(code):
        print(
        f"{Fore.WHITE} - CHANNEL: {Fore.YELLOW}[{message.channel}]"
        f"\n{Fore.WHITE} - SERVER: {Fore.YELLOW}[{message.guild}]"
        f"\n{Fore.WHITE} - CONTENT: {Fore.YELLOW}[The content can be found at Privnote/{code}.txt]"
    +Fore.RESET)

    time = datetime.datetime.now().strftime("%H:%M %p")
    if 'discord.gift/' in message.content:
            start = datetime.datetime.now()
            code = re.search("discord.gift/(.*)", message.content).group(1)

            headers = {'Authorization': token}
            r = requests.post(
                f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem',
                headers=headers,
            ).text

            elapsed = datetime.datetime.now() - start
            elapsed = f'{elapsed.seconds}.{elapsed.microseconds}'

            if 'This gift has been redeemed already.' in r:
                print(""
                f"\n{Fore.CYAN}[{time} - Nitro Already Redeemed]"+Fore.RESET)
                NitroData(elapsed, code)

            elif 'subscription_plan' in r:
                print(""
                f"\n{Fore.CYAN}[{time} - Nitro Success]"+Fore.RESET)
                NitroData(elapsed, code)

            elif 'Unknown Gift Code' in r:
                print(""
                f"\n{Fore.CYAN}[{time} - Nitro Unknown Gift Code]"+Fore.RESET)
                NitroData(elapsed, code)

            elif 'You are being rate limited.' in r:
                print(""
                f"\n{Fore.CYAN}[{time} - Ratelimited]"+Fore.RESET)
                NitroData(elapsed, code)

    if 'Someone just dropped' in message.content:
        if slotbot_sniper == True:
            if message.author.id == 346353957029019648:
                try:
                    await message.channel.send('~grab')
                except discord.errors.Forbidden:
                    print(""
                    f"\n{Fore.CYAN}[{time} - SlotBot Couldnt Grab]"+Fore.RESET)
                    SlotBotData()
                print(""
                f"\n{Fore.CYAN}[{time} - Slotbot Grabbed]"+Fore.RESET)
                SlotBotData()
        else:
            return

    if 'GIVEAWAY' in message.content:
        if giveaway_sniper == True:
            if message.author.id == 294882584201003009:
                try:
                    await message.add_reaction("🎉")
                except discord.errors.Forbidden:
                    print(""
                    f"\n{Fore.CYAN}[{time} - Giveaway Couldnt React]"+Fore.RESET)
                    GiveawayData()
                print(""
                f"\n{Fore.CYAN}[{time} - Giveaway Sniped]"+Fore.RESET)
                GiveawayData()
        else:
            return

    if f'Congratulations <@{bot.user.id}>' in message.content:
        if giveaway_sniper == True:
            if message.author.id == 294882584201003009:
                print(""
                f"\n{Fore.CYAN}[{time} - Giveaway Won]"+Fore.RESET)
                GiveawayData()
        else:
            return

    await bot.process_commands(message)

#SNIPERS
@bot.command(aliases=["automee6"])
async def mee6(ctx, param=None):
    await ctx.message.delete()
    if param is None:
        await ctx.send("Please specify yes or no", delete_after=3)
        return
    if str(param).lower() == 'true' or str(param).lower() == 'on':
        if isinstance(ctx.message.channel, discord.DMChannel) or isinstance(ctx.message.channel, discord.GroupChannel):
            await ctx.send("You can't bind Auto-MEE6 to a DM or GC", delete_after=3)
            return
        else:
            bot.mee6 = True
            await ctx.send("Auto-MEE6 Successfully bound to `" + ctx.channel.name + "`", delete_after=3)
            bot.mee6_channel = ctx.channel.id
    elif str(param).lower() == 'false' or str(param).lower() == 'off':
        bot.mee6 = False
        await ctx.send("Auto-MEE6 Successfully **disabled**", delete_after=3)
    while bot.mee6 is True:
        sentences = ['Stop waiting for exceptional things to just happen.',
                     'The lyrics of the song sounded like fingernails on a chalkboard.',
                     'I checked to make sure that he was still alive.', 'We need to rent a room for our party.',
                     'He had a hidden stash underneath the floorboards in the back room of the house.',
                     'Your girlfriend bought your favorite cookie crisp cereal but forgot to get milk.',
                     'People generally approve of dogs eating cat food but not cats eating dog food.',
                     'I may struggle with geography, but I\'m sure I\'m somewhere around here.',
                     'She was the type of girl who wanted to live in a pink house.',
                     'The bees decided to have a mutiny against their queen.',
                     'She looked at the masterpiece hanging in the museum but all she could think is that her five-year-old could do better.',
                     'The stranger officiates the meal.', 'She opened up her third bottle of wine of the night.',
                     'They desperately needed another drummer since the current one only knew how to play bongos.',
                     'He waited for the stop sign to turn to a go sign.',
                     'His thought process was on so many levels that he gave himself a phobia of heights.',
                     'Her hair was windswept as she rode in the black convertible.',
                     'Karen realized the only way she was getting into heaven was to cheat.',
                     'The group quickly understood that toxic waste was the most effective barrier to use against the zombies.',
                     'It was obvious she was hot, sweaty, and tired.', 'This book is sure to liquefy your brain.',
                     'I love eating toasted cheese and tuna sandwiches.', 'If you don\'t like toenails',
                     'You probably shouldn\'t look at your feet.',
                     'Wisdom is easily acquired when hiding under the bed with a saucepan on your head.',
                     'The spa attendant applied the deep cleaning mask to the gentleman’s back.',
                     'The three-year-old girl ran down the beach as the kite flew behind her.',
                     'For oil spots on the floor, nothing beats parking a motorbike in the lounge.',
                     'They improved dramatically once the lead singer left.',
                     'The Tsunami wave crashed against the raised houses and broke the pilings as if they were toothpicks.',
                     'Excitement replaced fear until the final moment.', 'The sun had set and so had his dreams.',
                     'People keep telling me "orange" but I still prefer "pink".',
                     'Someone I know recently combined Maple Syrup & buttered Popcorn thinking it would taste like caramel popcorn. It didn’t and they don’t recommend anyone else do it either.',
                     'I liked their first two albums but changed my mind after that charity gig.',
                     'Plans for this weekend include turning wine into water.',
                     'A kangaroo is really just a rabbit on steroids.',
                     'He played the game as if his life depended on it and the truth was that it did.',
                     'He\'s in a boy band which doesn\'t make much sense for a snake.',
                     'She let the balloon float up into the air with her hopes and dreams.',
                     'There was coal in his stocking and he was thrilled.',
                     'This made him feel like an old-style rootbeer float smells.',
                     'It\'s not possible to convince a monkey to give you a banana by promising it infinite bananas when they die.',
                     'The light in his life was actually a fire burning all around him.',
                     'Truth in advertising and dinosaurs with skateboards have much in common.',
                     'On a scale from one to ten, what\'s your favorite flavor of random grammar?',
                     'The view from the lighthouse excited even the most seasoned traveler.',
                     'The tortoise jumped into the lake with dreams of becoming a sea turtle.',
                     'It\'s difficult to understand the lengths he\'d go to remain short.',
                     'Nobody questions who built the pyramids in Mexico.',
                     'They ran around the corner to find that they had traveled back in time.']
        await bot.get_channel(bot.mee6_channel).send(random.choice(sentences), delete_after=0.1)
        await asyncio.sleep(60)

@bot.command(aliases=['slotsniper', "slotbotsniper"])
async def slotbot(ctx, param=None):
    await ctx.message.delete()
    bot.slotbot_sniper = False
    if str(param).lower() == 'true' or str(param).lower() == 'on':
        bot.slotbot_sniper = True
    elif str(param).lower() == 'false' or str(param).lower() == 'off':
        bot.slotbot_sniper = False

@bot.command(aliases=['giveawaysniper'])
async def giveaway(ctx, param=None):
    await ctx.message.delete()
    bot.giveaway_sniper = False
    if str(param).lower() == 'true' or str(param).lower() == 'on':
        bot.giveaway_sniper = True
    elif str(param).lower() == 'false' or str(param).lower() == 'off':
        bot.giveaway_sniper = False

@bot.command(aliases=[])
async def msgsniper(ctx, msgsniperlol=None):
    await ctx.message.delete()
    if str(msgsniperlol).lower() == 'true' or str(msgsniperlol).lower() == 'on':
        bot.msgsniper = True
        await ctx.send('Message-Sniper is now **enabled**')
    elif str(msgsniperlol).lower() == 'false' or str(msgsniperlol).lower() == 'off':
        bot.msgsniper = False
        await ctx.send('Message-Sniper is now **disabled**')


@bot.event
async def on_ready():
    print(f'''{Fore.RED}
                          {Fore.LIGHTWHITE_EX}╔╦╗╔═╗╦═╗╔╦╗╦╔╗╔╔═╗╦
                          {Fore.WHITE} ║ ║╣ ╠╦╝║║║║║║║╠═╣║
                          \033[94m ╩ ╚═╝╩╚═╩ ╩╩╝╚╝╩ ╩╩═╝

               {Fore.RED}Terminal Selfbot v{SELFBOT.__version__} | {Fore.RED}Logged in as: {bot.user.name}#{bot.user.discriminator}

                        Nitro Sniper | {Fore.GREEN}Enabled
                        {Fore.RED}Message Sniper | {Fore.GREEN}Enabled
                        {Fore.RED}Slotbot Sniper | {Fore.GREEN}Enabled
                        {Fore.RED}Giveaway Sniper | {Fore.GREEN}Enabled
                        {Fore.RED}Privnote Sniper | {Fore.GREEN}Enabled
                        {Fore.RED}Mention Logger | {Fore.GREEN}Enabled


    ''' + Fore.RESET)

#Compact Help Commands

compact_enabled = False

@bot.command()
async def compact(ctx,choice):
    global compact_enabled
    await ctx.message.delete()
    if choice == 'on':
      await ctx.send(f"Compact mode is now enabled run `({bot.command_prefix}chelp)` to access compact mode.")
      compact_enabled = True

    elif choice == 'off':
      await ctx.send("Compact mode is now disabled.")
      compact_enabled = False


@bot.group(invoke_without_command=True)
async def chelp(ctx):
   if compact_enabled:
    await ctx.message.delete()
    embed = discord.Embed(color=0x36393E, timestamp=ctx.message.created_at)
    embed.set_author(name="")
    embed.set_thumbnail(url="")
    embed.add_field(name="TERMINAL SELFBOT - HELP MENU", value="```Help - Shows this message\nHelp General - Shows all general commands\nHelp Account - Shows all account commands\nHelp Text - Shows all text commands\nHelp Misc - Shows all miscellaneous commands\nHelp Image - Shows all image manipulation commands\nHelp Nsfw - Shows all nsfw commands\nHelp Malicious - Shows all malicious commands\nHelp Nuke - Shows all nuke commands\nHelp Mod - Shows all moderation commands\nHelp Server - Shows all server-builder commands\nHelp Config - Shows all config commands\n\n   ---------- Credits ; Shows Credits ----------\n---------------------------------------------------\nNitro Sniper: Enabled --- Giveaway Sniper: Enabled\nPrivnote Sniper: Enabled --- Slotbot Sniper: Enabled\nMessage Logger: Enabled --- Mention Logger: Enabled```", inline=False)
    embed.set_image(url="")
    await ctx.send(embed=embed)
   else:
    await ctx.message.delete()
    await ctx.send("Compact mode isn't enabled")

@chelp.command(invoke_without_command=True)
async def general(ctx):
   if compact_enabled:
    await ctx.message.delete()
    embed = discord.Embed(color=0x36393E, timestamp=ctx.message.created_at)
    embed.set_author(name="")
    embed.set_thumbnail(url="")
    embed.add_field(name="TERMINAL SELFBOT - GENERAL COMMANDS", value="```help {category} - returns all commands of that category\nuptime - returns how long the selfbot has been running\nping - returns the bots latency\npingweb {url} pings a website to see if its up\nav {user} - returns the users pfp\ngeoip {ip} - provides info about the ip\nwhois {user} - returns info about the users account\ntokeninfo {token} - returns info about the token\ncopyserver - makes a copy of the server\nserverinfo - gets information about the server\nserverpfp - returns the server icon\nserverbanner - returns the server banner\nclearcls - clears the console\nshutdown - shutsdown the selfbot```", inline=False)
    embed.set_image(url="")
    await ctx.send(embed=embed)
   else:
    await ctx.message.delete()
    await ctx.send("Compact mode isn't enabled")

@chelp.command(invoke_without_command=True)
async def account(ctx):
   if compact_enabled:
    await ctx.message.delete()
    embed = discord.Embed(color=0x36393E, timestamp=ctx.message.created_at)
    embed.set_author(name="")
    embed.set_thumbnail(url="")
    embed.add_field(name="TERMINAL SELFBOT - ACCOUNT COMMANDS", value="```ghost - makes your name and pfp invisible\npfpsteal {user} - steals the users pfp\nsetpfp {link} - sets the image-link as your pfp\nhypesquad {hypesquad} - changes your current hypesquad\nbump - bumps the server every 7200 seconds\ncyclenick {text} - cycles through your nickname\nstopcyclenick - stops cycling your nickname\nstream {status} - sets your streaming status\nplaying {status} - sets your playing status\nlistening {status} - sets your listening status\nwatching {status} - sets your watching status\nstopactivity - resets your status activity\nsetname {name} - changes your username\njoin {inv-code} - joins the specified server\nallservers - displays all your servers in the console\nleavegc - leaves the current groupchat\nadminservers - lists every server you have perms in\nfirstmsg - returns the first msg```", inline=False)
    embed.set_image(url="")
    await ctx.send(embed=embed)
   else:
    await ctx.message.delete()
    await ctx.send("Compact mode isn't enabled")


@chelp.command(invoke_without_command=True)
async def text(ctx):
   if compact_enabled:
    await ctx.message.delete()
    embed = discord.Embed(color=0x36393E, timestamp=ctx.message.created_at)
    embed.set_author(name="")
    embed.set_thumbnail(url="")
    embed.add_field(name="TERMINAL SELFBOT - TEXT COMMANDS", value="```snipe - snipes the last deleted msg\neditsnipe - sniped the last edited msg\nflood - floods the chat with a blank msg\n1337speak {msg} - talk like a hacker\nminesweeper - play a game of minesweeper\nreverse {msg} - sends the msg but reversed\nshrug - returns ¯\_(ツ)_/¯\nlenny - returns ( ͡° ͜ʖ ͡°)\nfliptable - returns (╯°□°）╯︵ ┻━┻\nunflip - returns (╯°□°）╯︵ ┻━┻\nbold {msg} - bolds the msg\ncensor {msg} - censors the msg\nitalicize {msg} - italicizes the msg\nstrike {msg} - strikes through the msg\nquote {msg} - quotes the msg\ncode {msg} - applies code formatting to the msg\npurge {amount} purges your messages\nascii {msg} - creates an ascii art\nquery {text} - queries your msg into google\nghostping {amt} {msg} - ghostpings the mentioned user\nshorten {url} - shortens your link using tinyurl\nwizz - sends a prank msg about wizzing\nslots - play the slots machine\ndel {msg} - sends a ghost msg\ntts {msg} sends a tts msg\nabc - cycles the alphabet\n9/11 - sends a 9/11 attack\nmassreact {emoji} - massreact messages```", inline=False)
    embed.set_image(url="")
    await ctx.send(embed=embed)
   else:
    await ctx.message.delete()
    await ctx.send("Compact mode isn't enabled")

@chelp.command(invoke_without_command=True)
async def misc(ctx):
   if compact_enabled:
    await ctx.message.delete()
    embed = discord.Embed(color=0x36393E, timestamp=ctx.message.created_at)
    embed.set_author(name="")
    embed.set_thumbnail(url="")
    embed.add_field(name="TERMINAL SELFBOT - MISCELLANEOUS COMMANDS", value="```copycat {user} - copies the specified user\nstopcopycat - stops copycatting\nanticatfish {user} - reverse google search users pfp\nhexcolor {hex-code} - returns the hex-codes color\ndick {user} - returns the users dicksize\nbitcoin - shows the current bitcoin exchange rate\nhastebin {msg} - posts your message to hastebin\nrolecolor {role} - returns the roles color\nnitro - generates a random nitro code\nnitrogen - redirects you to a nitrogen\ntopic - sends a conversation starter\nwyr - sends a would you rather\ngif {query} sends a gif based on the query\nimage {query} sends an image based on the query\ncat - returns a random cat pic\ndog - returns a random dog pic\nfox - returns a random fox pic```", inline=False)
    embed.set_image(url="")
    await ctx.send(embed=embed)
   else:
    await ctx.message.delete()
    await ctx.send("Compact mode isn't enabled")

@chelp.command(invoke_without_command=True)
async def image(ctx):
   if compact_enabled:
    await ctx.message.delete()
    embed = discord.Embed(color=0x36393E, timestamp=ctx.message.created_at)
    embed.set_author(name="")
    embed.set_thumbnail(url="")
    embed.add_field(name="TERMINAL SELFBOT - IMAGE COMMANDS", value="```magik {user} - distorts the specified user\nfry {user} - deep-fry the specified user\nblur {user} - blurs the specified user\npixelate {user} - pixelates the specified user\nblurpify {user} - blurpifies the spiecified user\ninvert {user} - inverts the specified user\ngay {user} - makes the specified user gay\ncommunist {user} - makes the specified user a communist\nsnow {user} - adds a snow filter to the specified user\nsupreme {message} - makes a supreme logo\ndarksupreme {message} makes a darksupreme logo\nfax {text} makes a fax meme\npornhub {logo-word 1} {logo-word 2} - makes a ph logo\nphcomment {user} {message} - makes a fake ph comment\ntweet {user} {message} makes a fake tweet```", inline=False)
    embed.set_image(url="")
    await ctx.send(embed=embed)
   else:
    await ctx.message.delete()
    await ctx.send("Compact mode isn't enabled")

@chelp.command(invoke_without_command=True)
async def nsfw(ctx):
   if compact_enabled:
    await ctx.message.delete()
    embed = discord.Embed(color=0x36393E, timestamp=ctx.message.created_at)
    embed.set_author(name="")
    embed.set_thumbnail(url="")
    embed.add_field(name="TERMINAL SELFBOT - NSFW COMMANDS", value="```hentai - shows hentai\nboobs - shows boobs\nass - shows ass\nblowjob - shows a blowjob\nwaifu - returns waifu pics```", inline=False)
    embed.set_image(url="")
    await ctx.send(embed=embed)
   else:
    await ctx.message.delete()
    await ctx.send("Compact mode isn't enabled")

@chelp.command(invoke_without_command=True)
async def malicious(ctx):
   if compact_enabled:
    await ctx.message.delete()
    embed = discord.Embed(color=0x36393E, timestamp=ctx.message.created_at)
    embed.set_author(name="")
    embed.set_thumbnail(url="")
    embed.add_field(name="TERMINAL SELFBOT - MALICIOUS COMMANDS", value="```dmall {msg} - messages every user in your friendlist\nsdmall {msg} - messages every user in the server\nspam {amount} {msg} - spams your message\ndisable {token} - disables the given token\ndwebhook {url} - deletes the given webhook\ngmailbomb - spam someones gmail {check console}\nhtoken - get half of someones token {check console}\nspotify - free spotify account method\naccounts - free acounts method\nfreenitro - free nitro method\ncheapboost - cheap server-boost method```", inline=False)
    embed.set_image(url="")
    await ctx.send(embed=embed)
   else:
    await ctx.message.delete()
    await ctx.send("Compact mode isn't enabled")

@chelp.command(invoke_without_command=True)
async def nuke(ctx):
   if compact_enabled:
    await ctx.message.delete()
    embed = discord.Embed(color=0x36393E, timestamp=ctx.message.created_at)
    embed.set_author(name="")
    embed.set_thumbnail(url="")
    embed.add_field(name="TERMINAL SELFBOT - NUKE COMMANDS", value="```destroy - destroys the server\nmassban - bans all members in the server\nchannels - deletes all channels and spams them\nroles - spams roles in the server```", inline=False)
    embed.set_image(url="")
    await ctx.send(embed=embed)
   else:
    await ctx.message.delete()
    await ctx.send("Compact mode isn't enabled")

@chelp.command(invoke_without_command=True)
async def mod(ctx):
   if compact_enabled:
    await ctx.message.delete()
    embed = discord.Embed(color=0x36393E, timestamp=ctx.message.created_at)
    embed.set_author(name="")
    embed.set_thumbnail(url="")
    embed.add_field(name="TERMINAL SELFBOT - MODERATION COMMANDS", value="```ban {user} - bans the specified user\nkick {user} - kicks the specified user\nmassunban - unbans everyone in the server\nrainbowrole {role} - makes the role a rainbow\nclear {amount} - clears a certain amount of messages```", inline=False)
    embed.set_image(url="")
    await ctx.send(embed=embed)
   else:
    await ctx.message.delete()
    await ctx.send("Compact mode isn't enabled")

@chelp.command(invoke_without_command=True)
async def server(ctx):
   if compact_enabled:
    await ctx.message.delete()
    embed = discord.Embed(color=0x36393E, timestamp=ctx.message.created_at)
    embed.set_author(name="")
    embed.set_thumbnail(url="")
    embed.add_field(name="TERMINAL SELFBOT - SERVER-BUILDER COMMANDS", value="```buildtemplate1 - builds a server for you to use\nbuildtemplate2 - builds a server for you to use\nbuildtemplate3 - builds a server for you to use\nbuildtemplate4 - builds a server for you to use\nbuildtemplate5 - builds a server for you to use\nbuildtemplate6 - builds a server for you to use\nbuildtemplate7 - builds a server for you to use\nbuildtemplate8 - builds a server for you to use\nbuildtemplate9 - builds a server for you to use\nbuildtemplate10 - builds a server for you to use```", inline=False)
    embed.set_image(url="")
    await ctx.send(embed=embed)
   else:
    await ctx.message.delete()
    await ctx.send("Compact mode isn't enabled")

@chelp.command(invoke_without_command=True)
async def config(ctx):
   if compact_enabled:
    await ctx.message.delete()
    embed = discord.Embed(color=0x36393E, timestamp=ctx.message.created_at)
    embed.set_author(name="")
    embed.set_thumbnail(url="")
    embed.add_field(name="TERMINAL SELFBOT - CONFIG COMMANDS", value=f"```msgsniper (on/off) - snipes messages ({bot.msgsniper})\nslotbot (on/off) - snipes slotbots ({bot.slotbot_sniper})\nmee6 (on/off) - farm mee6 levels ({bot.mee6}) (<#{bot.mee6_channel}>)\nprefix (prefix) - changes the bots prefix ({bot.command_prefix})\ncompact (on/off) - toggles compact mode ({compact_enabled}) ({bot.command_prefix}chelp)\nsafemode (on/off) - toggles safemode ({safemode_enabled}) ({bot.command_prefix}shelp)```", inline=False)
    embed.set_image(url="")
    await ctx.send(embed=embed)
   else:
    await ctx.message.delete()
    await ctx.send("Compact mode isn't enabled")


@bot.command(invoke_without_command=True)
async def ccredits(ctx):
   if compact_enabled:
    await ctx.message.delete()
    embed = discord.Embed(color=0x36393E, timestamp=ctx.message.created_at)
    embed.set_author(name="")
    embed.set_thumbnail(url="")
    embed.add_field(name="TERMINAL SELFBOT - CREDITS", value="```Yum - Creator\nZyph - Creator\nAced - General Support\nAlucard - General Support\nExeter - General Support\nGgbitch - General Support```", inline=False)
    embed.set_image(url="")
    await ctx.send(embed=embed)
   else:
    await ctx.message.delete()
    await ctx.send("Compact mode isn't enabled")

#Safe Mode Help Commands

safemode_enabled = False

@bot.command()
async def safemode(ctx,choice):
    global safemode_enabled
    await ctx.message.delete()
    if choice == 'on':
      await ctx.send(f"Safemode mode is now enabled run `({bot.command_prefix}shelp)` to access safemode.")
      safemode_enabled = True

    elif choice == 'off':
      await ctx.send("Safemode is now disabled.")
      safemode_enabled = False

@bot.group(invoke_without_command=True)
async def shelp(ctx):
  await ctx.message.delete()
  if safemode_enabled:
    await ctx.send("""
***----------> TERMINAL SELFBOT - HELP MENU***
```yaml
Help - Shows this message
Help General - Shows all general commands
Help Account - Shows all account commands
Help Text - Shows all text commands
Help Misc - Shows all miscellaneous commands
Help Image - Shows all image manipulation commands
Help Nsfw - Shows all nsfw commands
Help Malicious - Shows all malicious commands
Help Nuke - Shows all nuke commands
Help Mod - Shows all moderation commands
Help Server - Shows all server-builder commands
Help Config - Shows all config commands

   ------ Credits ; Shows Credits ------
-------------------------------------------------------
Nitro Sniper: Enabled --- Giveaway Sniper: Enabled
Privnote Sniper: Enabled --- Slotbot Sniper: Enabled
Message Logger: Enabled --- Mention Logger: Enabled
```
""")
  else:
    await ctx.send("Safemode isn't enabled")

@shelp.command(invoke_without_command=True)
async def general(ctx):
  await ctx.message.delete()
  if safemode_enabled:
    await ctx.send("""
    ***----------> TERMINAL SELFBOT - GENERAL COMMANDS***
```yaml
help {category} - returns all commands of that category
uptime - returns how long the selfbot has been running
ping - returns the bots latency
pingweb {url} pings a website to see if its up
av {user} - returns the users pfp
geoip {ip} - provides info about the ip
whois {user} - returns info about the users account
tokeninfo {token} - returns info about the token
copyserver - makes a copy of the server
serverinfo - gets information about the server
serverpfp - returns the server icon
serverbanner - returns the server banner
clearcls - clears the console
shutdown - shutsdown the selfbot```
""")
  else:
    await ctx.send("Safemode isn't enabled")

@shelp.command(invoke_without_command=True)
async def account(ctx):
  await ctx.message.delete()
  if safemode_enabled:
    await ctx.send("""
    ***----------> TERMINAL SELFBOT - ACCOUNT COMMANDS***
```yaml
ghost - makes your name and pfp invisible
pfpsteal {user} - steals the users pfp
setpfp {link} - sets the image-link as your pfp
hypesquad {hypesquad} - changes your current hypesquad
bump - bumps the server every 7200 seconds
cyclenick {text} - cycles through your nickname
stopcyclenick - stops cycling your nickname
stream {status} - sets your streaming status
playing {status} - sets your playing status
listening {status} - sets your listening status
watching {status} - sets your watching status
stopactivity - resets your status activity
setname {name} - changes your username
join {inv-code} - joins the specified server
allservers - displays all your servers in the console
leavegc - leaves the current groupchat
adminservers - lists every server you have perms in
firstmsg - returns the first msg```
""")
  else:
    await ctx.send("Safemode isn't enabled")

@shelp.command(invoke_without_command=True)
async def text(ctx):
  await ctx.message.delete()
  if safemode_enabled:
    await ctx.send("""
***----------> TERMINAL SELFBOT - TEXT COMMANDS***
```yaml
snipe - snipes the last deleted msg
editsnipe - sniped the last edited msg
flood - floods the chat with a blank msg
1337speak {msg} - talk like a hacker
minesweeper - play a game of minesweeper
reverse {msg} - sends the msg but reversed
shrug - returns ¯\_(ツ)_/¯
lenny - returns ( ͡° ͜ʖ ͡°)
fliptable - returns (╯°□°）╯︵ ┻━┻
unflip - returns (╯°□°）╯︵ ┻━┻
bold {msg} - bolds the msg
censor {msg} - censors the msg
italicize {msg} - italicizes the msg
strike {msg} - strikes through the msg
quote {msg} - quotes the msg
code {msg} - applies code formatting to the msg
purge {amount} purges your messages
ascii {msg} - creates an ascii art
query {text} - queries your msg into google
ghostping {amt} {msg} - ghostpings the mentioned user
shorten {url} - shortens your link using tinyurl
wizz - sends a prank msg about wizzing
slots - play the slots machine
del {msg} - sends a ghost msg
tts {msg} sends a tts msg
abc - cycles the alphabet
9/11 - sends a 9/11 attack
massreact {emoji} - massreact messages
```
""")
  else:
    await ctx.send("Safemode isn't enabled")


@shelp.command(invoke_without_command=True)
async def misc(ctx):
  await ctx.message.delete()
  if safemode_enabled:
    await ctx.send("""
***----------> TERMINAL SELFBOT - MISCELLANEOUS COMMANDS***
```yaml
copycat {user} - copies the specified user
stopcopycat - stops copycatting
anticatfish {user} - reverse google search users pfp
hexcolor {hex-code} - returns the hex-codes color
dick {user} - returns the users dicksize
bitcoin - shows the current bitcoin exchange rate
hastebin {msg} - posts your message to hastebin
rolecolor {role} - returns the roles color
nitro - generates a random nitro code
nitrogen - redirects you to a nitrogen
topic - sends a conversation starter
wyr - sends a would you rather
gif {query} sends a gif based on the query
image {query} sends an image based on the query
cat - returns a random cat pic
dog - returns a random dog pic
fox - returns a random fox pic
```
""")
  else:
    await ctx.send("Safemode isn't enabled")

@shelp.command(invoke_without_command=True)
async def image(ctx):
  await ctx.message.delete()
  if safemode_enabled:
    await ctx.send("""
    ***----------> TERMINAL SELFBOT - IMAGE COMMANDS***
```yaml
magik {user} - distorts the specified user
fry {user} - deep-fry the specified user
blur {user} - blurs the specified user
pixelate {user} - pixelates the specified user
blurpify {user} - blurpifies the spiecified user
invert {user} - inverts the specified user
gay {user} - makes the specified user gay
communist {user} - makes the specified user a communist
snow {user} - adds a snow filter to the specified user
supreme {message} - makes a supreme logo
darksupreme {message} makes a darksupreme logo
fax {text} makes a fax meme
pornhub {logo-word 1} {logo-word 2} - makes a ph logo
phcomment {user} {message} - makes a fake ph comment
tweet {user} {message} makes a fake tweet```
""")
  else:
    await ctx.send("Safemode isn't enabled")

@shelp.command(invoke_without_command=True)
async def nsfw(ctx):
  await ctx.message.delete()
  if safemode_enabled:
    await ctx.send("""
    ***----------> TERMINAL SELFBOT - NSFW COMMANDS***
```yaml
hentai - shows hentai
boobs - shows boobs
ass - shows ass
blowjob - shows a blowjob
waifu - returns waifu pics
```
""")
  else:
    await ctx.send("Safemode isn't enabled")

@shelp.command(invoke_without_command=True)
async def malicious(ctx):
  await ctx.message.delete()
  if safemode_enabled:
    await ctx.send("""
    ***----------> TERMINAL SELFBOT - MALICIOUS COMMANDS***
```yaml
dmall {msg} - messages every user in your friendlist
sdmall {msg} - messages every user in the server
spam {amount} {msg} - spams your message
disable {token} - disables the given token
dwebhook {url} - deletes the given webhook
gmailbomb - spam someones gmail {check console}
htoken - get half of someones token {check console}
spotify - free spotify account method
accounts - free acounts method
freenitro - free nitro method
cheapboost - cheap server-boost method
```
""")
  else:
    await ctx.send("Safemode isn't enabled")

@shelp.command(invoke_without_command=True)
async def nuke(ctx):
  await ctx.message.delete()
  if safemode_enabled:
    await ctx.send("""
    ***----------> TERMINAL SELFBOT - NUKE COMMANDS***
```yaml
destroy - destroys the server
massban - bans all members in the server
channels - deletes all channels and spams them
roles - spams roles in the server```
""")
  else:
    await ctx.send("Safemode isn't enabled")

@shelp.command(invoke_without_command=True)
async def mod(ctx):
  await ctx.message.delete()
  if safemode_enabled:
    await ctx.send("""
    ***----------> TERMINAL SELFBOT - MODERATION COMMANDS***
```yaml
ban {user} - bans the specified user
kick {user} - kicks the specified user
massunban - unbans everyone in the server
rainbowrole {role} - makes the role a rainbow
clear {amount} - clears a certain amount of messages```
""")
  else:
    await ctx.send("Safemode isn't enabled")

@shelp.command(invoke_without_command=True)
async def server(ctx):
  await ctx.message.delete()
  if safemode_enabled:
    await ctx.send("""
    ***----------> TERMINAL SELFBOT - SERVER-BUILDER COMMANDS***
```yaml
buildtemplate1 - builds a server for you to use
buildtemplate2 - builds a server for you to use
buildtemplate3 - builds a server for you to use
buildtemplate4 - builds a server for you to use
buildtemplate5 - builds a server for you to use
buildtemplate6 - builds a server for you to use
buildtemplate7 - builds a server for you to use
buildtemplate8 - builds a server for you to use
buildtemplate9 - builds a server for you to use
buildtemplate10 - builds a server for you to use
```
""")
  else:
    await ctx.send("Safemode isn't enabled")


@shelp.command(invoke_without_command=True)
async def config(ctx):
  await ctx.message.delete()
  if safemode_enabled:
    await ctx.send(f"""
    ***----------> TERMINAL SELFBOT - CONFIG COMMANDS***
```yaml
msgsniper (on/off) - snipes messages ({bot.msgsniper})
slotbot (on/off) - snipes slotbots ({bot.slotbot_sniper})
giveaway (on/off) - snipes giveaways ({bot.giveaway_sniper})
mee6 (on/off) - farms mee6 levels ({bot.mee6}) (<#{bot.mee6_channel})
prefix (prefix) - changes the bots prefix ({bot.command_prefix})
compact (on/off) - toggles compact mode ({compact_enabled}) ({bot.command_prefix}chelp)
safemode (on/off) - toggles safemode ({safemode_enabled}) ({bot.command_prefix}shelp)
```
""")
  else:
    await ctx.send("Safemode isn't enabled")

@bot.command(invoke_without_command=True)
async def scredits(ctx):
  await ctx.message.delete()
  if safemode_enabled:
    await ctx.send(f"""
        ***----------> TERMINAL SELFBOT - CREDITS***
```yaml
Yum - Creator
Zyph - Creator
Aced - General Support
Alucard - General Support
Exeter - General Support
Ggbitch - General Support
```
""")
  else:
    await ctx.send("Safemode isn't enabled")

#Help commands
@bot.group(invoke_without_command=True)
async def help(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name="𝙏𝙀𝙍𝙈𝙄𝙉𝘼𝙇 𝙎𝙀𝙇𝙁𝘽𝙊𝙏 | 𝙋𝙍𝙀𝙁𝙄𝙓: " + str(bot.command_prefix), icon_                     url=bot.user.avatar_url)
        embed.set_thumbnail(url=bot.user.avatar_url)
        embed.set_image(url="")
        embed.add_field(name=" :comet: `GENERAL`", value="Shows all general commands", inline=True)
        embed.add_field(name=" :comet: `ACCOUNT`", value="Shows all account commands", inline=True)
        embed.add_field(name=" :comet: `TEXT`", value="Shows all text commands", inline=True)
        embed.add_field(name=" :comet: `MISC`", value="Shows all miscellaneous commands", inline=True)
        embed.add_field(name=" :comet: `IMAGE`", value="Shows all image manipulation commands", inline=True)
        embed.add_field(name=" :comet: `NSFW`", value="Shows all nsfw commands", inline=True)
        embed.add_field(name=" :comet: `MALICIOUS`", value="Shows all malicious commands", inline=True)
        embed.add_field(name=" :comet: `NUKE`", value="Shows all nuke commands", inline=True)
        embed.add_field(name=" :comet: `MOD`", value="Shows all mod commands", inline=True)
        embed.add_field(name=" :comet: `SERVER`", value="Shows all server-builder commands", inline=True)
        embed.add_field(name=" :comet: `CONFIG`", value="Shows all config commands", inline=True)
        embed.add_field(name=" :comet: `CREDITS`", value="Shows the selfbot credits", inline=True)
        embed.set_image(url="https://cdn.discordapp.com/attachments/772834827115167804/778657485917388809/tumblr_oi5rpmTpmV1u6hk5ko1_400.gif")
        await ctx.send(embed=embed)


@help.command()
async def general(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name=" 🌠 𝙂𝙀𝙉𝙀𝙍𝘼𝙇 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎")
        embed.add_field(name="`help {category}`", value="- returns all commands of that category")
        embed.add_field(name="`uptime`", value="- return how long the selfbot has been running")
        embed.add_field(name="`ping`", value="- returns the bot's latency")
        embed.add_field(name="`pingweb {url}`", value="- pings a website to see if it's up")
        embed.add_field(name="`av {user}`", value="- returns the users pfp")
        embed.add_field(name="`geoip {ip}`", value="- provides info about the ip")
        embed.add_field(name="`whois {user}`", value="- returns the user's account info")
        embed.add_field(name="`tokeninfo {token}`", value="- returns information about the token")
        embed.add_field(name="`copyserver`", value="- makes a copy of the server")
        embed.add_field(name="`serverinfo`", value="- gets information about the server")
        embed.add_field(name="`serverpfp`", value="- returns the server icon")
        embed.add_field(name="`banner`", value="- returns the server banner")
        embed.add_field(name="`clearcls`", value="- clears the console")
        embed.add_field(name="`shutdown`", value="- shutsdown the selfbot")
        embed.set_image(url="")
        await ctx.send(embed=embed)


@help.command()
async def account(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name=" 🌠 𝘼𝘾𝘾𝙊𝙐𝙉𝙏 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎")
        embed.add_field(name="`ghost`", value="- makes your name and pfp invisible")
        embed.add_field(name="`pfpsteal {user}`", value="- steals the users pfp")
        embed.add_field(name="`setpfp {link}`", value="- sets the image-link as your pfp")
        embed.add_field(name="`hypesquad {hypesquad}`", value="- changes your current hypesquad")
        embed.add_field(name="`bump`", value="- bumps server that it is ran in automatically every 7200 seconds")
        embed.add_field(name="`cyclenick {text}`", value="- cycles through your nickname letter by letter")
        embed.add_field(name="`stopcyclenick`", value="- stops cycling your nickname")
        embed.add_field(name="`stream {status}`", value="- sets your streaming status")
        embed.add_field(name="`playing {status}`", value="- sets your playing status")
        embed.add_field(name="`listening {status}`", value="- sets your listening status")
        embed.add_field(name="`watching {status}`", value="- sets your watching status")
        embed.add_field(name="`stopactivity`", value="- resets your status-activity")
        embed.add_field(name="`setname {name}`", value="- sets your username to whatever is specified.")
        embed.add_field(name="`join {inv-code}`", value="- joins the specified server")
        embed.add_field(name="`allservers`", value="- displays every server you're in inside of the console")
        embed.add_field(name="`leavegc`", value="- leaves the current groupchat")
        embed.add_field(name="`adminservers`", value="- lists all servers you have perms in")
        embed.set_image(url="")
        await ctx.send(embed=embed)

@help.command()
async def config(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name=" 🌠 𝘾𝙊𝙉𝙁𝙄𝙂 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎")
        embed.add_field(name="`msgsniper {on/off}`", value=f"- snipes messages ({bot.msgsniper})")
        embed.add_field(name="`slotbot {on/off}`", value=f"- snipes slotbots ({bot.slotbot_sniper})")
        embed.add_field(name="`giveaway {on/off}`", value=f"- snipes giveaways ({bot.giveaway_sniper})")
        embed.add_field(name="`mee6 {on/off}`", value=f"- auto sends messages\n in the specified channel ({bot.mee6}) (<#{bot.mee6_channel}>)")
        embed.add_field(name="`prefix {prefix}`", value=f"- changes the bots prefix ({bot.command_prefix})")
        embed.add_field(name="`compact {on/off}`", value=f"- enables/disables compact mode ({compact_enabled}) ({bot.command_prefix}chelp)")
        embed.add_field(name="`safemode {on/off}`", value=f"- enables/disables safemode ({safemode_enabled}) ({bot.command_prefix}shelp)")
        embed.set_image(url="")
        await ctx.send(embed=embed)


@help.command()
async def image(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name=" 🌠 𝙄𝙈𝘼𝙂𝙀 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎")
        embed.add_field(name="`magik {user}`", value="- distorts the specified user")
        embed.add_field(name="`fry {user}`", value="- deep-fry the specified user")
        embed.add_field(name="`blur {user}`", value="- blurs the specified user")
        embed.add_field(name="`pixelate {user}`", value="- pixelates the specified user")
        embed.add_field(name="`blurpify {user}`", value="- blurpifies the specified user")
        embed.add_field(name="`invert {user}`", value="- inverts the specified user")
        embed.add_field(name="`gay {user}`", value="- makes the specified user gay")
        embed.add_field(name="`communist {user}`", value="- makes the specified user a communist")
        embed.add_field(name="`snow {user}`", value="- adds a snow filter to the specified user")
        embed.add_field(name="`supreme {message}`", value="- makes a *Supreme* logo")
        embed.add_field(name="`darksupreme {message}`", value="- makes a *Dark Supreme* logo")
        embed.add_field(name="`fax {text}`", value="- makes a fax meme")
        embed.add_field(name="`pornhub {logo-word 1} {logo-word 2}`", value="- makes a PornHub logo")
        embed.add_field(name="`phcomment {user} {message}`", value="- makes a fake PornHub comment")
        embed.add_field(name="`tweet {user} {message}`", value="- makes a fake tweet")
        embed.set_image(url="")
        await ctx.send(embed=embed)

@help.command()
async def nuke(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name=" 🌠 𝙉𝙐𝙆𝙀 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎")
        embed.add_field(name="`destroy`", value="- destroys the server")
        embed.add_field(name="`massban`", value="- bans all members in the server")
        embed.add_field(name="`channels`", value="- deletes all chanels and spams them")
        embed.add_field(name="`roles`", value="- spams roles in the server")
        embed.set_image(url="")
        await ctx.send(embed=embed)

@help.command()
async def raid(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name=" 🌠 𝙍𝘼𝙄𝘿 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎 - COMING SOON")
        embed.add_field(name="`join {invite}`", value="- Makes your tokens join the server")
        embed.add_field(name="`leave`", value="- Makes your tokens leave the server")
        embed.add_field(name="`friend {user-id}`", value="- Makes your tokens friend the user")
        embed.add_field(name="`check`", value="- Checks if your tokens are valid")
        embed.add_field(name="`spam {msg}`", value="- Spams the server with your tokens")
        embed.add_field(name="`fspam {msg}`", value="- Spams the server but faster")
        embed.add_field(name="`dmspam {user-id} {msg}`", value="- Spams the user with your tokens")
        embed.add_field(name="`gspam {msg}`", value="- Ghost spams the server (msg instantly deletes)")
        embed.add_field(name="`rspam {msg}`", value="- Spams all roles in the server")
        embed.add_field(name="`typing`", value="- Makes your tokens have a typing status in the server")
        embed.set_image(url="")
        await ctx.send(embed=embed)


@help.command()
async def misc(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name=" 🌠 𝙈𝙄𝙎𝘾𝙀𝙇𝙇𝘼𝙉𝙀𝙊𝙐𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎")
        embed.add_field(name="`copycat {user}`", value="- copies the specified user")
        embed.add_field(name="`stopcopycat`", value="- stops copycatting")
        embed.add_field(name="`anticatfish {user}`", value="- reverse google searches the users pfp")
        embed.add_field(name="`hexcolor {hex-code}`", value="- returns the hex-codes color")
        embed.add_field(name="`dick {user}`", value="- returns the users dicksize")
        embed.add_field(name="`bitcoin`", value="- shows the current bitcoin exchange rate")
        embed.add_field(name="`hastebin {msg}`", value="- posts your message to hastebin")
        embed.add_field(name="`rolecolor {role}`", value="- returns the roles color")
        embed.add_field(name="`nitro`", value="- generates a random nitro code")
        embed.add_field(name="`nitrogen`", value="- redirects you to a nitrogen")
        embed.add_field(name="`topic`", value="- sends a conversation starter")
        embed.add_field(name="`wyr`", value="- sends a would you rather")
        embed.add_field(name="`gif {query}`", value="- sends a gif based on the query")
        embed.add_field(name="`image {query}`", value="- sends an image based on the query")
        embed.add_field(name="`cat`", value="- returns a random cat pic")
        embed.add_field(name="`dog`", value="- returns a random dog pic")
        embed.add_field(name="`fox`", value="- returns a random fox pic")
        embed.set_image(url="")
        await ctx.send(embed=embed)

@help.command()
async def nsfw(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name=" 🌠 𝙉𝙎𝙁𝙒 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎")
        embed.add_field(name="`hentai`", value="- shows hentai")
        embed.add_field(name="`boobs`", value="- shows boobs")
        embed.add_field(name="`ass`", value="- shows ass")
        embed.add_field(name="`blowjob`", value="- shows a blowjob")
        embed.add_field(name="`waifu`", value="- returns waifu pics")
        embed.set_image(url="")
        await ctx.send(embed=embed)

@help.command()
async def malicious(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name=" 🌠 𝙈𝘼𝙇𝙄𝘾𝙄𝙊𝙐𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎")
        embed.add_field(name="`dmall {msg}`", value="- messages every user in your friend-list")
        embed.add_field(name="`sdmall {msg}`", value="- messages every user in the server")
        embed.add_field(name="`spam {amount} {msg}`", value="- spams your message in a certain amount")
        embed.add_field(name="`disable {token}`", value="- disables the given token")
        embed.add_field(name="`dwebhook {url}`", value="- deletes the given webhook")
        embed.add_field(name="`gmailbomb`", value="- spam someones email {check console}")
        embed.add_field(name="`htoken`", value="- get half of someones token from userid {check console}")
        embed.add_field(name="`spotify`", value="- free spotify account method")
        embed.add_field(name="`accounts`", value="- free accounts method")
        embed.add_field(name="`freenitro`", value="- free nitro method")
        embed.add_field(name="`cheapboost`", value="- free cheap server-boost method")
        embed.set_image(url="")
        await ctx.send(embed=embed)


@help.command()
async def text(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name=" 🌠 𝙏𝙀𝙓𝙏 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎")
        embed.add_field(name="`snipe`", value="- snipes the last deleted message")
        embed.add_field(name="`editsnipe`", value="- snipes the last edited message")
        embed.add_field(name="`flood`", value="- floods the chat with a large blank message")
        embed.add_field(name="`1337speak {msg}`", value="- talk like a hacker")
        embed.add_field(name="`minesweeper`", value="- play a game of minesweeper")
        embed.add_field(name="`reverse {msg}`", value="- sends the message but reversed")
        embed.add_field(name="`shrug`", value="- returns ¯\_(ツ)_/¯")
        embed.add_field(name="`lenny`", value="- returns ( ͡° ͜ʖ ͡°)")
        embed.add_field(name="`fliptable`", value="- returns (╯°□°）╯︵ ┻━┻")
        embed.add_field(name="`unflip`", value="- returns (╯°□°）╯︵ ┻━┻")
        embed.add_field(name="`bold {msg}`", value="- bolds the message")
        embed.add_field(name="`censor {msg}`", value="- censors the message")
        embed.add_field(name="`italicize {msg}`", value="- italicizes the message")
        embed.add_field(name="`strike {msg}`", value="- strikes through the message")
        embed.add_field(name="`quote {msg}`", value="- quotes the message")
        embed.add_field(name="`code {msg}`", value="- applies code formatting to the message")
        embed.add_field(name="`purge {amount}`", value="- purges the amount of messages")
        embed.add_field(name="`ascii {msg}`", value="- creates an ASCII art of your message")
        embed.add_field(name="`query {text}`", value="- queries your message into google")
        embed.add_field(name="`ghostping {amount} {mention}`", value="- ghostpings the mentioned user an amount of times")
        embed.add_field(name="`shorten {url}`", value="- Shortens ur link using tinyurl")
        embed.add_field(name="`firstmsg`", value="- get the first message of the channel or dm")
        embed.add_field(name="`wizz`", value="- sends a prank message about wizzing")
        embed.add_field(name="`slots`", value="- play the slots machine")
        embed.add_field(name="`del {msg}`", value="- sends a message then deletes it")
        embed.add_field(name="`tts {msg}`", value="- sends your message as a tts")
        embed.add_field(name="`abc`", value="- cycles through the alphabet")
        embed.add_field(name="`9/11`", value="- sends a 9/11 attack")
        embed.add_field(name="`massreact {emoji}`", value="- massreact with custom emojis")
        embed.set_image(url="")
        await ctx.send(embed=embed)

@help.command()
async def server(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name=" 🌠 𝙎𝙀𝙍𝙑𝙀𝙍 𝘽𝙐𝙄𝙇𝘿𝙀𝙍 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎")
        embed.add_field(name="`buildtemplate1`", value="- builds a server for you to use")
        embed.add_field(name="`buildtemplate2`", value="- builds a server for you to use")
        embed.add_field(name="`buildtemplate3`", value="- builds a server for you to use")
        embed.add_field(name="`buildtemplate4`", value="- builds a server for you to use")
        embed.add_field(name="`buildtemplate5`", value="- builds a server for you to use")
        embed.add_field(name="`buildtemplate6`", value="- builds a server for you to use")
        embed.add_field(name="`buildtemplate7`", value="- builds a server for you to use")
        embed.add_field(name="`buildtemplate8`", value="- builds a server for you to use")
        embed.add_field(name="`buildtemplate9`", value="- builds a server for you to use")
        embed.add_field(name="`buildtemplate10`", value="- builds a server for you to use")

        embed.set_image(url="")
        await ctx.send(embed=embed)

@bot.command()
async def credits(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name=" 🌠 𝘾𝙍𝙀𝘿𝙄𝙏𝙎")
        embed.add_field(name="`YUM`", value="Creator")
        embed.add_field(name="`ZYPH`", value="Creator")
        embed.add_field(name="`ACED`", value="- General Support")
        embed.add_field(name="`ALUCARD`", value="- General Support")
        embed.add_field(name="`EXETER`", value="- General Support")
        embed.add_field(name="`GGBITCH`", value="- General-Support")
        await ctx.send(embed=embed)

@help.command()
async def mod(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name=" 🌠 𝙈𝙊𝘿𝙀𝙍𝘼𝙏𝙄𝙊𝙉 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎")
        embed.add_field(name="`ban {user}`", value="bans the specified user")
        embed.add_field(name="`kick {user}`", value="kicks the specified user")
        embed.add_field(name="`massunban`", value="- unbans everyone in the server")
        embed.add_field(name="`rainbowrole {role}`", value="- makes the role a rainbow role")
        embed.add_field(name="`clear {amount}`", value="- clears a certain amount of messages")
        await ctx.send(embed=embed)

#Message Logger
@bot.event
async def on_message_delete(message):
    if message.author.id == bot.user.id:
        return
    if bot.msgsniper:
        if isinstance(message.channel, discord.DMChannel) or isinstance(message.channel, discord.GroupChannel):
            attachments = message.attachments
            if len(attachments) == 0:
                message_content = "`" + str(discord.utils.escape_markdown(str(message.author))) + "`: " + str(
                    message.content).replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
                await message.channel.send(message_content)
            else:
                links = ""
                for attachment in attachments:
                    links += attachment.proxy_url + "\n"
                message_content = "`" + str(
                    discord.utils.escape_markdown(str(message.author))) + "`: " + discord.utils.escape_mentions(
                    message.content) + "\n\n**Attachments:**\n" + links
                await message.channel.send(message_content)
    if len(bot.sniped_message_dict) > 1000:
        bot.sniped_message_dict.clear()
    attachments = message.attachments
    if len(attachments) == 0:
        channel_id = message.channel.id
        message_content = "`" + str(discord.utils.escape_markdown(str(message.author))) + "`: " + str(
            message.content).replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
        bot.sniped_message_dict.update({channel_id: message_content})
    else:
        links = ""
        for attachment in attachments:
            links += attachment.proxy_url + "\n"
        channel_id = message.channel.id
        message_content = "`" + str(
            discord.utils.escape_markdown(str(message.author))) + "`: " + discord.utils.escape_mentions(
            message.content) + "\n\n**Attachments:**\n" + links
        bot.sniped_message_dict.update({channel_id: message_content})


#Edit Logger
@bot.event
async def on_message_edit(before, after):
    if before.author.id == bot.user.id:
        return
    if bot.msgsniper:
        if before.content is after.content:
            return
        if isinstance(before.channel, discord.DMChannel) or isinstance(before.channel, discord.GroupChannel):
            attachments = before.attachments
            if len(attachments) == 0:
                message_content = "`" + str(
                    discord.utils.escape_markdown(str(before.author))) + "`: \n**BEFORE**\n" + str(
                    before.content).replace("@everyone", "@\u200beveryone").replace("@here",
                                                                                    "@\u200bhere") + "\n**AFTER**\n" + str(
                    after.content).replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
                await before.channel.send(message_content)
            else:
                links = ""
                for attachment in attachments:
                    links += attachment.proxy_url + "\n"
                message_content = "`" + str(
                    discord.utils.escape_markdown(str(before.author))) + "`: " + discord.utils.escape_mentions(
                    before.content) + "\n\n**Attachments:**\n" + links
                await before.channel.send(message_content)
    if len(bot.sniped_edited_message_dict) > 1000:
        bot.sniped_edited_message_dict.clear()
    attachments = before.attachments
    if len(attachments) == 0:
        channel_id = before.channel.id
        message_content = "`" + str(discord.utils.escape_markdown(str(before.author))) + "`: \n**BEFORE**\n" + str(
            before.content).replace("@everyone", "@\u200beveryone").replace("@here",
                                                                            "@\u200bhere") + "\n**AFTER**\n" + str(
            after.content).replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
        bot.sniped_edited_message_dict.update({channel_id: message_content})
    else:
        links = ""
        for attachment in attachments:
            links += attachment.proxy_url + "\n"
        channel_id = before.channel.id
        message_content = "`" + str(
            discord.utils.escape_markdown(str(before.author))) + "`: " + discord.utils.escape_mentions(
            before.content) + "\n\n**Attachments:**\n" + links
        bot.sniped_edited_message_dict.update({channel_id: message_content})

#Mention logger
@bot.listen('on_message')
async def ifmentioned(message):
    if message_logger:
        if message.author == bot.user:
            return
        if bot.user.mention in message.content:
            print(f"{Fore.WHITE}╔══════════════════════════{Fore.WHITE}════════════════════════{Fore.RESET}")
            print(Fore.WHITE + "║ [Mentioned] " + Fore.RESET + Fore.CYAN + f"You were mentioned by {message.author}." + Fore.RESET)
            print(Fore.WHITE + "║ [Mentioned] " + Fore.RESET + Fore.YELLOW + f"Server: {message.guild}" + Fore.RESET)
            print(Fore.WHITE + "║ [Mentioned] " + Fore.RESET + Fore.YELLOW + f"Channel: {message.channel}")
            print(Fore.WHITE + "║ [Mentioned] " + Fore.RESET + Fore.YELLOW + f"Message Content: {message.content}".replace(f"<@{bot.user.id}>" or f"<@!{bot.user.id}>", "") + Fore.RESET)
            print(f"{Fore.WHITE}╚══════════════════════════{Fore.WHITE}════════════════════════" + Fore.RESET)
    else:
        pass


#General commands
@bot.command()
async def ping(ctx):
    await ctx.message.delete()
    before = time.monotonic()
    message = await ctx.send("Pinging...")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"`{int(ping)} ms`")

@bot.command()
async def clearcls(ctx):
    await ctx.message.delete()
    os.system("cls")
    await on_ready()

@bot.command()
async def uptime(ctx):
    await ctx.message.delete()
    now = datetime.datetime.utcnow()  # Timestamp of when uptime function is run
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if days:
        time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
    else:
        time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."
    uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)
    await ctx.send(uptime_stamp)

@bot.command()
async def prefix(ctx, prefix):
    await ctx.message.delete()
    bot.command_prefix = str(prefix)

@bot.command()
async def pingweb(ctx, website=None):
    await ctx.message.delete()
    if website is None:
        pass
    else:
        try:
            r = requests.get(website).status_code
        except Exception as e:
            print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}" + Fore.RESET)
        if r == 404:
            await ctx.send(f'Website is down ({r})', delete_after=3)
        else:
            await ctx.send(f'Website is operational ({r})', delete_after=3)

@bot.command(aliases=['pfp', 'avatar'])
async def av(ctx, *, user: discord.User = None):
    await ctx.message.delete()
    format = "gif"
    user = user or ctx.author
    if user.is_avatar_animated() != True:
        format = "png"
    avatar = user.avatar_url_as(format=format if format != "gif" else None)
    async with aiohttp.ClientSession() as session:
        async with session.get(str(avatar)) as resp:
            image = await resp.read()
    with io.BytesIO(image) as file:
        await ctx.send(file=discord.File(file, f"Avatar.{format}"))

@bot.command(aliases=['geolocate', 'iptogeo', 'iptolocation', 'ip2geo', 'ip'])
async def geoip(ctx, *, ipaddr: str = '1.3.3.7'):
    await ctx.message.delete()
    r = requests.get(f'http://extreme-ip-lookup.com/json/{ipaddr}')
    geo = r.json()
    embed = discord.Embed()
    fields = [
        {'name': 'IP', 'value': geo['query']},
        {'name': 'Type', 'value': geo['ipType']},
        {'name': 'Country', 'value': geo['country']},
        {'name': 'City', 'value': geo['city']},
        {'name': 'Continent', 'value': geo['continent']},
        {'name': 'Country', 'value': geo['country']},
        {'name': 'Hostname', 'value': geo['ipName']},
        {'name': 'ISP', 'value': geo['isp']},
        {'name': 'Latitute', 'value': geo['lat']},
        {'name': 'Longitude', 'value': geo['lon']},
        {'name': 'Org', 'value': geo['org']},
        {'name': 'Region', 'value': geo['region']},
    ]
    for field in fields:
        if field['value']:
            embed.add_field(name=field['name'], value=field['value'], inline=True)
    return await ctx.send(embed=embed)

@bot.command()
async def whois(ctx, member: discord.Member = None):
  await ctx.message.delete()
  member = ctx.author if not member else member
  roles = [role for role in member.roles]

  embed = discord.Embed()
  embed.set_author(name=f"User Info - {member}")
  embed.set_thumbnail(url=member.avatar_url)
  embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
  embed.add_field(name="User ID", value=member.id)
  embed.add_field(name="Nickname", value=member.display_name)
  embed.add_field(name="Creation Date", value=member.created_at.strftime("%a, %#d %B, %Y, %I:%M %p UTC"))
  embed.add_field(name="Guild Join Date", value=member.joined_at.strftime("%a, %#d %B, %Y, %I:%M %p UTC"))
  embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
  embed.add_field(name="Highest Role", value=member.top_role.mention)
  embed.add_field(name="Bot:", value=member.bot)
  await ctx.send(embed=embed)

@bot.command(aliases=['tokinfo', 'tdox'])
async def tokeninfo(ctx, _token):
    await ctx.message.delete()
    headers = {
        'Authorization': _token,
        'Content-Type': 'application/json'
    }
    try:
        res = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers)
        res = res.json()
        user_id = res['id']
        locale = res['locale']
        avatar_id = res['avatar']
        language = languages.get(locale)
        creation_date = datetime.datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime(
            '%d-%m-%Y %H:%M:%S UTC')
    except KeyError:
        headers = {
            'Authorization': "Bot " + _token,
            'Content-Type': 'application/json'
        }
        try:
            res = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers)
            res = res.json()
            user_id = res['id']
            locale = res['locale']
            avatar_id = res['avatar']
            language = languages.get(locale)
            creation_date = datetime.datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime(
                '%d-%m-%Y %H:%M:%S UTC')
            em = discord.Embed(
                description=f"Name: `{res['username']}#{res['discriminator']} ` **BOT**\nID: `{res['id']}`\nEmail: `{res['email']}`\nCreation Date: `{creation_date}`")
            fields = [
                {'name': 'Flags', 'value': res['flags']},
                {'name': 'Local language', 'value': res['locale'] + f"{language}"},
                {'name': 'Verified', 'value': res['verified']},
            ]
            for field in fields:
                if field['value']:
                    em.add_field(name=field['name'], value=field['value'], inline=False)
                    em.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}")
            return await ctx.send(embed=em)
        except KeyError:
            await ctx.send("Invalid token")
    em = discord.Embed(
        description=f"Name: `{res['username']}#{res['discriminator']}`\nID: `{res['id']}`\nEmail: `{res['email']}`\nCreation Date: `{creation_date}`")
    nitro_type = "None"
    if "premium_type" in res:
        if res['premium_type'] == 2:
            nitro_type = "Nitro Premium"
        elif res['premium_type'] == 1:
            nitro_type = "Nitro Classic"
    fields = [
        {'name': 'Phone', 'value': res['phone']},
        {'name': 'Flags', 'value': res['flags']},
        {'name': 'Local language', 'value': res['locale'] + f"{language}"},
        {'name': 'MFA', 'value': res['mfa_enabled']},
        {'name': 'Verified', 'value': res['verified']},
        {'name': 'Nitro', 'value': nitro_type},
    ]
    for field in fields:
        if field['value']:
            em.add_field(name=field['name'], value=field['value'], inline=False)
            em.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}")
    return await ctx.send(embed=em)

@bot.command(aliases=["copyguild", "copyserver"])
async def copy(ctx):  # b'\xfc'
    await ctx.message.delete()
    await bot.create_guild(f'Copy -{ctx.guild.name}')
    await asyncio.sleep(4)
    for g in bot.guilds:
        if f'Copy -{ctx.guild.name}' in g.name:
            for c in g.channels:
                await c.delete()
            for cate in ctx.guild.categories:
                x = await g.create_category(f"{cate.name}")
                for chann in cate.channels:
                    if isinstance(chann, discord.VoiceChannel):
                        await x.create_voice_channel(f"{chann}")
                    if isinstance(chann, discord.TextChannel):
                        await x.create_text_channel(f"{chann}")
    try:
        await g.edit(icon=ctx.guild.icon_url)
    except:
        pass

@bot.command(aliases=["rainbowrole"])
async def rainbow(ctx, *, role):
    await ctx.message.delete()
    role = discord.utils.get(ctx.guild.roles, name=role)
    await ctx.send("Type `Stop` to stop.")

    def check_reply(m):
        return m.content in ["Stop"] and m.author == ctx.author

    async def rainbow_role():
        while True:
            await role.edit(role=role, colour=random.randrange(0x1000000))

    rainbow_role_task = bot.loop.create_task(rainbow_role())
    await bot.wait_for("message", check=check_reply)
    rainbow_role_task.cancel()
    await ctx.send("`Stopped the rainbow-role.`")

@bot.command(aliases=["guildinfo"])
async def serverinfo(ctx):
    guild = ctx.guild
    await ctx.message.delete()
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(title=f"{ctx.guild.name}",
                          description=f" {len(guild.members)} Members\n {len(guild.roles)} Roles\n {len(guild.text_channels)} Text-Channels\n {len(guild.voice_channels)} Voice-Channels\n {len(guild.categories)} Categories",
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{guild.created_at.strftime(date_format)}")
    embed.add_field(name="Server Owner", value=f"{guild.owner}")
    embed.add_field(name="Server Region", value=f"{guild.region}")
    embed.add_field(name="Server ID", value=f"{guild.id}")
    embed.set_thumbnail(url=f"{guild.icon_url}")
    await ctx.send(embed=embed)

@bot.command(aliases=['guildpfp', 'serverpfp', 'servericon'])
async def guildicon(ctx):
    await ctx.message.delete()
    em = discord.Embed(title=ctx.guild.name)
    em.set_image(url=ctx.guild.icon_url)
    await ctx.send(embed=em)

@bot.command(aliases=['serverbanner'])
async def banner(ctx):
    await ctx.message.delete()
    em = discord.Embed(title=ctx.guild.name)
    em.set_image(url=ctx.guild.banner_url)
    await ctx.send(embed=em)

@bot.command(aliases=["logout"])
async def shutdown(ctx):
    await ctx.message.delete()
    await bot.logout()

#Account commands
@bot.command()
async def ghost(ctx):
    await ctx.message.delete()
    if config.get('password') == 'password-here':
        print(f"{Fore.RED}[ERROR] {Fore.YELLOW}You didnt put your password in the config.json file" + Fore.RESET)
    else:
        password = config.get('password')
        with open('Images/Avatars/Transparent.png', 'rb') as f:
            try:
                await bot.user.edit(password=password, username="ٴٴٴٴ", avatar=f.read())
            except discord.HTTPException as e:
                print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}" + Fore.RESET)

@bot.command()
async def join(tokens, invlink):
    try:
      userdata = req.get("https://discord.com/api/users/@me", headers={"authorization": token}).json()
      req.post(f"https://discordapp.com/api/invites/{invlink}", headers={"authorization": token})
      print(f"{Color.WHITE}{userdata['username']}#{userdata['discriminator']}{Color.GREEN} has joined {Color.WHITE}{invlink}")
      return
    except:
      pass

@bot.command(aliases=['pfpget', 'stealpfp'])
async def pfpsteal(ctx, user: discord.User):
    await ctx.message.delete()
    if password == 'password-here':
        print(f"{Fore.RED}[ERROR] {Fore.YELLOW}You didnt put your password in the config.json file" + Fore.RESET)
    else:
        with open('Images/Avatars/Stolen/Stolen.png', 'wb') as f:
            r = requests.get(user.avatar_url, stream=True)
            for block in r.iter_content(1024):
                if not block:
                    break
                f.write(block)
        try:
            Image.open('Images/Avatars/Stolen/Stolen.png').convert('RGB')
            with open('Images/Avatars/Stolen/Stolen.png', 'rb') as f:
                await bot.user.edit(password=password, avatar=f.read())
        except discord.HTTPException as e:
            print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}" + Fore.RESET)


@bot.command(name='set-pfp', aliases=['setpfp', 'pfpset,"changepfp'])
async def _set_pfp(ctx, *, url):
    await ctx.message.delete()
    if password == 'password-here':
        print(f"{Fore.RED}[ERROR] {Fore.YELLOW}You didnt put your password in the config.json file" + Fore.RESET)
    else:
        with open('Images/Avatars/PFP-1.png', 'wb') as f:
            r = requests.get(url, stream=True)
            for block in r.iter_content(1024):
                if not block:
                    break
                f.write(block)
    try:
        Image.open('Images/Avatars/PFP-1.png').convert('RGB')
        with open('Images/Avatars/PFP-1.png', 'rb') as f:
            await bot.user.edit(password=password, avatar=f.read())
    except discord.HTTPException as e:
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}" + Fore.RESET)


@bot.command(aliases=['changehypesquad'])
async def hypesquad(ctx, house):
    await ctx.message.delete()
    request = requests.Session()
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'
    }
    if house == "bravery":
        payload = {'house_id': 1}
    elif house == "brilliance":
        payload = {'house_id': 2}
    elif house == "balance":
        payload = {'house_id': 3}
    elif house == "random":
        houses = [1, 2, 3]
        payload = {'house_id': random.choice(houses)}
    try:
        request.post('https://discordapp.com/api/v6/hypesquad/online', headers=headers, json=payload, timeout=10)
    except Exception as e:
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}" + Fore.RESET)


@bot.command(name='group-leaver',
                aliase=['leaveallgroups', 'leavegroup', 'leavegroups', "groupleave", "groupleaver"])
async def _group_leaver(ctx):
    await ctx.message.delete()
    for channel in bot.private_channels:
        if isinstance(channel, discord.GroupChannel):
            await channel.leave()

@bot.command(pass_context=True, aliases=["cyclename", "autoname", "autonick", "cycle"])
async def cyclenick(ctx, *, text):
    await ctx.message.delete()
    global cycling
    cycling = True
    while cycling:
        name = ""
        for letter in text:
            name = name + letter
            await ctx.message.author.edit(nick=name)


@bot.command(aliases=["stopcyclename", "cyclestop", "stopautoname", "stopautonick", "stopcycle"])
async def stopcyclenick(ctx):
    await ctx.message.delete()
    global cycling
    cycling = False


@bot.command()
async def stream(ctx, *, message):
    await ctx.message.delete()
    stream = discord.Streaming(
        name=message,
        url=stream_url,
    )
    await bot.change_presence(activity=stream)

@bot.command(alises=["game"])
async def playing(ctx, *, message):
    await ctx.message.delete()
    game = discord.Game(
        name=message
    )
    await bot.change_presence(activity=game)


@bot.command(aliases=["listen"])
async def listening(ctx, *, message):
    await ctx.message.delete()
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=message,
        ))


@bot.command(aliases=["watch"])
async def watching(ctx, *, message):
    await ctx.message.delete()
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=message
        ))


@bot.command(aliases=["stopstreaming", "stopstatus", "stoplistening", "stopplaying", "stopwatching"])
async def stopactivity(ctx):
    await ctx.message.delete()
    await bot.change_presence(activity=None, status=discord.Status.dnd)



@bot.command()
async def adminservers(ctx):
    await ctx.message.delete()
    admins = []
    bots = []
    kicks = []
    bans = []
    for guild in bot.guilds:
        if guild.me.guild_permissions.administrator:
            admins.append(discord.utils.escape_markdown(guild.name))
        if guild.me.guild_permissions.manage_guild and not guild.me.guild_permissions.administrator:
            bots.append(discord.utils.escape_markdown(guild.name))
        if guild.me.guild_permissions.ban_members and not guild.me.guild_permissions.administrator:
            bans.append(discord.utils.escape_markdown(guild.name))
        if guild.me.guild_permissions.kick_members and not guild.me.guild_permissions.administrator:
            kicks.append(discord.utils.escape_markdown(guild.name))
    adminPermServers = f"**Servers with Admin ({len(admins)}):**\n{admins}"
    botPermServers = f"\n**Servers with BOT_ADD Permission ({len(bots)}):**\n{bots}"
    banPermServers = f"\n**Servers with Ban Permission ({len(bans)}):**\n{bans}"
    kickPermServers = f"\n**Servers with Kick Permission ({len(kicks)}:**\n{kicks}"
    await ctx.send(adminPermServers + botPermServers + banPermServers + kickPermServers)


@bot.command()
async def bump(ctx):
    await ctx.message.delete()
    await ctx.send("Starting..", delete_after=3)
    while True:
        try:
            await ctx.send('!d bump')
            await asyncio.sleep(7200)
        except Exception as e:
            print(f"Couldn't bump. Did the channel get nuked or deleted? Error: {e}")

@bot.command(aliases=["gcleave"])
async def leavegc(ctx):
    await ctx.message.delete()
    if isinstance(ctx.message.channel, discord.GroupChannel):
        await ctx.message.channel.leave()

@bot.command()
async def query(ctx, *, message):
    await ctx.message.delete()
    embed = discord.Embed(title="**Search Query**", color=0xff2b41, description=searchq(link=message))
    await ctx.send(embed=embed, delete_after=25)

@bot.command(aliases=['allguilds'])
async def allservers(ctx):
    await ctx.message.delete()
    async for guild in bot.fetch_guilds():
        print(guild)
    await asyncio.sleep(25)
    splash()

@bot.command()
async def setname(ctx, *, message):
    await ctx.message.delete()
    await bot.user.edit(username=message, password=password)

@bot.command()
async def ghostping(ctx, amount: int, arg):
    await ctx.message.delete()
    for i in range(int(amount / 2)):
        await ctx.send(arg, delete_after=0.001)
        await ctx.send(arg, delete_after=0.001)
        await ctx.send(arg, delete_after=0.001)
        await asyncio.sleep(15)

@bot.command()
async def shorten(ctx, *, link): # b'\xfc'
    await ctx.message.delete()
    r = requests.get(f'http://tinyurl.com/api-create.php?url={link}').text
    em = discord.Embed()
    em.add_field(name='Shortened link', value=r, inline=False )
    await ctx.send(embed=em)

@bot.command(name='first-message', aliases=['firstmsg', 'fm', 'firstmessage'])
async def firstmsg(ctx, channel: discord.TextChannel = None): # b'\xfc'
    await ctx.message.delete()
    if channel is None:
        channel = ctx.channel
    first_message = (await channel.history(limit=1, oldest_first=True).flatten())[0]
    embed = discord.Embed(description=first_message.content)
    embed.add_field(name="First Message", value=f"[Jump]({first_message.jump_url})")
    await ctx.send(embed=embed)


#Image commands
@bot.command(aliases=["distort"])
async def magik(ctx, user: discord.Member = None):
    await ctx.message.delete()
    endpoint = "https://nekobot.xyz/api/imagegen?type=magik&intensity=3&image="
    if user is None:
        avatar = str(ctx.author.avatar_url_as(format="png"))
        endpoint += avatar
        r = requests.get(endpoint)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(res['message'])) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_magik.png"))
        except:
            await ctx.send(res['message'])
    else:
        avatar = str(user.avatar_url_as(format="png"))
        endpoint += avatar
        r = requests.get(endpoint)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(res['message'])) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_magik.png"))
        except:
            await ctx.send(res['message'])



@bot.command(aliases=["deepfry"])
async def fry(ctx, user: discord.Member = None):
    await ctx.message.delete()
    endpoint = "https://nekobot.xyz/api/imagegen?type=deepfry&image="
    if user is None:
        avatar = str(ctx.author.avatar_url_as(format="png"))
        endpoint += avatar
        r = requests.get(endpoint)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(res['message'])) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_fry.png"))
        except:
            await ctx.send(res['message'])
    else:
        avatar = str(user.avatar_url_as(format="png"))
        endpoint += avatar
        r = requests.get(endpoint)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(res['message'])) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_fry.png"))
        except:
            await ctx.send(res['message'])


@bot.command()
async def blur(ctx, user: discord.Member = None):
    await ctx.message.delete()
    endpoint = "https://api.alexflipnote.dev/filter/blur?image="
    if user is None:
        avatar = str(ctx.author.avatar_url_as(format="png"))
        endpoint += avatar
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_blur.png"))
        except:
            await ctx.send(endpoint)
    else:
        avatar = str(user.avatar_url_as(format="png"))
        endpoint += avatar
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_blur.png"))
        except:
            await ctx.send(endpoint)

@bot.command(aliases=["pixel"])
async def pixelate(ctx, user: discord.Member = None):
    await ctx.message.delete()
    endpoint = "https://api.alexflipnote.dev/filter/pixelate?image="
    if user is None:
        avatar = str(ctx.author.avatar_url_as(format="png"))
        endpoint += avatar
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_blur.png"))
        except:
            await ctx.send(endpoint)
    else:
        avatar = str(user.avatar_url_as(format="png"))
        endpoint += avatar
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_blur.png"))
        except:
            await ctx.send(endpoint)


@bot.command(aliases=["blurp"])
async def blurpify(ctx, user: discord.Member = None):
    await ctx.message.delete()
    endpoint = "https://nekobot.xyz/api/imagegen?type=blurpify&image="
    if user is None:
        avatar = str(ctx.author.avatar_url_as(format="png"))
        endpoint += avatar
        r = requests.get(endpoint)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(res['message'])) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_blurpify.png"))
        except:
            await ctx.send(res['message'])
    else:
        avatar = str(user.avatar_url_as(format="png"))
        endpoint += avatar
        r = requests.get(endpoint)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(res['message'])) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_blurpify.png"))
        except:
            await ctx.send(res['message'])

@bot.command()
async def invert(ctx, user: discord.Member = None):
    await ctx.message.delete()
    endpoint = "https://api.alexflipnote.dev/filter/invert?image="
    if user is None:
        avatar = str(ctx.author.avatar_url_as(format="png"))
        endpoint += avatar
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_invert.png"))
        except:
            await ctx.send(endpoint)
    else:
        avatar = str(user.avatar_url_as(format="png"))
        endpoint += avatar
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_invert.png"))
        except:
            await ctx.send(endpoint)

@bot.command()
async def gay(ctx, user: discord.Member = None):
    await ctx.message.delete()
    endpoint = "https://api.alexflipnote.dev/filter/gay?image="
    if user is None:
        avatar = str(ctx.author.avatar_url_as(format="png"))
        endpoint += avatar
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_invert.png"))
        except:
            await ctx.send(endpoint)
    else:
        avatar = str(user.avatar_url_as(format="png"))
        endpoint += avatar
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_invert.png"))
        except:
            await ctx.send(endpoint)


@bot.command()
async def communist(ctx, user: discord.Member = None):
    await ctx.message.delete()
    endpoint = "https://api.alexflipnote.dev/filter/communist?image="
    if user is None:
        avatar = str(ctx.author.avatar_url_as(format="png"))
        endpoint += avatar
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_invert.png"))
        except:
            await ctx.send(endpoint)
    else:
        avatar = str(user.avatar_url_as(format="png"))
        endpoint += avatar
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_invert.png"))
        except:
            await ctx.send(endpoint)


@bot.command()
async def snow(ctx, user: discord.Member = None):
    await ctx.message.delete()
    endpoint = "https://api.alexflipnote.dev/filter/snow?image="
    if user is None:
        avatar = str(ctx.author.avatar_url_as(format="png"))
        endpoint += avatar
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_invert.png"))
        except:
            await ctx.send(endpoint)
    else:
        avatar = str(user.avatar_url_as(format="png"))
        endpoint += avatar
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"bot_invert.png"))
        except:
            await ctx.send(endpoint)


@bot.command()
async def supreme(ctx, *, args=None):
    await ctx.message.delete()
    if args is None:
        await ctx.send("missing parameters")
        return
    endpoint = "https://api.alexflipnote.dev/supreme?text=" + args.replace(" ", "%20")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"bot_supreme.png"))
    except:
        await ctx.send(endpoint)


@bot.command()
async def darksupreme(ctx, *, args=None):
    await ctx.message.delete()
    if args is None:
        await ctx.send("missing parameters")
        return
    endpoint = "https://api.alexflipnote.dev/supreme?text=" + args.replace(" ", "%20") + "&dark=true"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"bot_dark_supreme.png"))
    except:
        await ctx.send(endpoint)


@bot.command(aliases=["facts"])
async def fax(ctx, *, args=None):
    await ctx.message.delete()
    if args is None:
        await ctx.send("missing parameters")
        return
    endpoint = "https://api.alexflipnote.dev/facts?text=" + args.replace(" ", "%20")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"bot_facts.png"))
    except:
        await ctx.send(endpoint)


@bot.command(aliases=["pornhublogo", "phlogo"])
async def pornhub(ctx, word1=None, word2=None):
    await ctx.message.delete()
    if word1 is None or word2 is None:
        await ctx.send("missing parameters")
        return
    endpoint = "https://api.alexflipnote.dev/pornhub?text={text-1}&text2={text-2}".replace("{text-1}", word1).replace(
        "{text-2}", word2)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"bot_pornhub_logo.png"))
    except:
        await ctx.send(endpoint)


@bot.command(aliases=["pornhubcomment", 'phc'])
async def phcomment(ctx, user: str = None, *, args=None):
    await ctx.message.delete()
    if user is None or args is None:
        await ctx.send("missing parameters")
        return
    endpoint = "https://nekobot.xyz/api/imagegen?type=phcomment&text=" + args + "&username=" + user + "&image=" + str(
        ctx.author.avatar_url_as(format="png"))
    r = requests.get(endpoint)
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res["message"]) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"bot_pornhub_comment.png"))
    except:
        await ctx.send(res["message"])


@bot.command()
async def tweet(ctx, username: str = None, *, message: str = None):
    await ctx.message.delete()
    if username is None or message is None:
        await ctx.send("missing parameters")
        return
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={message}") as r:
            res = await r.json()
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(res['message'])) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"bot_tweet.png"))
            except:
                await ctx.send(res['message'])

#Misc commands
@bot.command(aliases=["stopcopycatuser", "stopcopyuser", "stopcopy"])
async def stopcopycat(ctx):
    await ctx.message.delete()
    if bot.user is None:
        await ctx.send("You weren't copying anyone to begin with")
        return
    await ctx.send("Stopped copying " + str(bot.copycat))
    bot.copycat = None

@bot.command(aliases=["copycatuser", "copyuser"])
async def copycat(ctx, user: discord.User):
    await ctx.message.delete()
    bot.copycat = user
    await ctx.send("Now copying " + str(bot.copycat))

@bot.command()
async def massreact(ctx, emote):
    await ctx.message.delete()
    messages = await ctx.message.channel.history(limit=40).flatten()
    for message in messages:
        await message.add_reaction(emote)

@bot.command(aliases=["reversesearch", "anticatfish", "catfish"])
async def revav(ctx, user: discord.Member = None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    try:
        em = discord.Embed(description=f"https://images.google.com/searchbyimage?image_url={user.avatar_url}")
        await ctx.send(embed=em)
    except Exception as e:
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}" + Fore.RESET)

@bot.command(name='get-color', aliases=['color', 'colour', 'sc', "hexcolor", "rgb"])
async def _get_color(ctx, *, color: discord.Colour):
    await ctx.message.delete()
    file = io.BytesIO()
    Image.new('RGB', (200, 90), color.to_rgb()).save(file, format='PNG')
    file.seek(0)
    em = discord.Embed(color=color, title=f'{str(color)}')
    em.set_image(url='attachment://color.png')
    await ctx.send(file=discord.File(file, 'color.png'), embed=em)

@bot.command(aliases=['dong', 'penis'])
async def dick(ctx, *, user: discord.Member = None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    size = random.randint(1, 15)
    dong = ""
    for _i in range(0, size):
        dong += "="
    await ctx.send(f"{user}'s Dick size\n8{dong}D")

@bot.command(aliases=['bitcoin'])
async def btc(ctx):
    await ctx.message.delete()
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR')
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    em = discord.Embed(description=f'USD: `{str(usd)}$`\nEUR: `{str(eur)}€`')
    em.set_author(name='Bitcoin', icon_url='https://cdn.pixabay.com/photo/2013/12/08/12/12/bitcoin-225079_960_720.png')
    await ctx.send(embed=em)

@bot.command()
async def hastebin(ctx, *, message):
    await ctx.message.delete()
    r = requests.post("https://hastebin.com/documents", data=message).json()
    await ctx.send(f"<https://hastebin.com/{r['key']}>")


@bot.command(name='rolecolor')
async def _role_hexcode(ctx, *, role: discord.Role):
    await ctx.message.delete()
    await ctx.send(f"{role.name} : {role.color}")

@bot.command()
async def nitro(ctx):
    await ctx.message.delete()
    await ctx.send(Nitro())

@bot.command()
async def nitrogen(ctx):
    await ctx.message.delete()
    url = 'https://outrageous-maze-music.glitch.me/'
    r = requests.get(url)
    if r.status_code == 200:
        webbrowser.open(url)
    else:
        print('Page is currently under maintenance, our team will announce when the page is back online')

@bot.command()
async def topic(ctx):
    await ctx.message.delete()
    r = requests.get('https://www.conversationstarters.com/generator.php').content
    soup = bs4(r, 'html.parser')
    topic = soup.find(id="random").text
    await ctx.send(topic)

@bot.command(aliases=['wouldyourather', 'would-you-rather', 'wyrq'])
async def wyr(ctx):
    await ctx.message.delete()
    r = requests.get('https://www.conversationstarters.com/wyrqlist.php').text
    soup = bs4(r, 'html.parser')
    qa = soup.find(id='qa').text
    qb = soup.find(id='qb').text
    message = await ctx.send(f"{qa}\nor\n{qb}")
    await message.add_reaction("🅰")
    await message.add_reaction("🅱")

@bot.command(aliases=["giphy", "tenor", "searchgif"])
async def gif(ctx, query=None):
    await ctx.message.delete()
    if query is None:
        r = requests.get("https://api.giphy.com/v1/gifs/random?api_key=ldQeNHnpL3WcCxJE1uO8HTk17ICn8i34&tag=&rating=R")
        res = r.json()
        await ctx.send(res['data']['url'])

@bot.command(aliases=["img", "searchimg", "searchimage", "imagesearch", "imgsearch"])
async def image(ctx, *, args):
    await ctx.message.delete()
    url = 'https://unsplash.com/search/photos/' + args.replace(" ", "%20")
    page = requests.get(url)
    soup = bs4(page.text, 'html.parser')
    image_tags = soup.findAll('img')
    if str(image_tags[2]['src']).find("https://trkn.us/pixel/imp/c="):
        link = image_tags[2]['src']
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(f"Search result for: **{args}**", file=discord.File(file, f"terminal_anal.png"))
        except:
            await ctx.send(f'' + link + f"\nSearch result for: **{args}** ")
    else:
        await ctx.send("Nothing found for **" + args + "**")

@bot.command()
async def cat(ctx):
    await ctx.message.delete()
    r = requests.get("https://api.thecatapi.com/v1/images/search").json()
    link = str(r[0]["url"])
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"terminal_cat.png"))
    except:
        await ctx.send(link)

@bot.command()
async def dog(ctx):
    await ctx.message.delete()
    r = requests.get("https://dog.ceo/api/breeds/image/random").json()
    link = str(r['message'])
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"terminal_dog.png"))
    except:
        await ctx.send(link)

@bot.command()
async def fox(ctx):
    await ctx.message.delete()
    r = requests.get('https://randomfox.ca/floof/').json()
    link = str(r["image"])
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"terminal_fox.png"))
    except:
        await ctx.send(link)

#Nuke commands
@bot.command()
async def destroy(ctx): # b'\xfc'
    await ctx.message.delete()
    for channel in list(ctx.guild.channels):
        try:
            await channel.delete()
        except:
            pass
    for user in list(ctx.guild.members):
        try:
            await user.ban()
        except:
            pass
    for role in list(ctx.guild.roles):
        try:
            await role.delete()
        except:
            pass
    for emoji in list(ctx.guild.emojis):
        try:
            await emoji.delete()
        except:
            pass
    try:
        await ctx.guild.edit(
            name=RandString(),
        )
    except:
        pass
    for _i in range(25):
        await ctx.guild.create_text_channel(name="TERMINAL SELFBOT")
        await ctx.guild.create_voice_channel(name="TERMINAL SELFBOT")
        await ctx.guild.create_category(name="TERMINAL SELFBOT")

@bot.command(pass_context=True)
async def massban(ctx):
    guild = ctx.message.guild
    for member in list(ctx.message.guild.members):
        try:
            await guild.ban(member)
            print("User " + member.name + " has been banned")
        except:
            pass
    print("Succesfully banned all members.")

@bot.command(pass_context=True)
async def channels(ctx):
    await ctx.message.delete()

    for channel in ctx.guild.channels:
            await channel.delete()
    for i in range(1, 25):
              await ctx.guild.create_text_channel(name=f'TERMINAL SELFBOT ON TOP {i}')
              await ctx.guild.create_voice_channel(name=f'TERMINAL SELFBOT ON TOP {i}')
              await ctx.guild.create_category(name=f'TERMINAL SELFBOT ON TOP {i}')

@bot.command()
async def massunban(ctx): # b'\xfc'
    await ctx.message.delete()
    banlist = await ctx.guild.bans()
    for users in banlist:
        try:
            await ctx.guild.unban(user=users.user)
        except:
            pass

@bot.command()
async def roles(ctx): # b'\xfc'
    await ctx.message.delete()
    for _i in range(100):
        try:
            await ctx.guild.create_role(name="NUKED")
        except:
            return


#Malicious Commands
@bot.command()
async def dmall(ctx, *, message):
  for user in bot.user.friends:
        try:
            await asyncio.sleep(1)
            await user.send(message)
        except:
            pass

@bot.command()
async def spotify(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name=" 🌠 𝙎𝙋𝙊𝙏𝙄𝙁�      �� 𝙈𝙀𝙏𝙃𝙊𝘿")
        embed.add_field(name="𝙈𝙀𝙏𝙃𝙊𝘿", value="https://github.com/TEERMIIINAAL/spotify/blob/mai      n/README.md")
        embed.set_image(url="")
        await ctx.send(embed=embed)

@bot.command()
async def accounts(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name=" 🌠 𝘼𝘾𝘾𝙊𝙐𝙉𝙏 𝙈𝙀𝙏𝙃𝙊𝘿")
        embed.add_field(name="𝙈𝙀𝙏𝙃𝙊𝘿", value="https://leak.sx")
        embed.set_image(url="")
        await ctx.send(embed=embed)

@bot.command()
async def freenitro(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name=" 🌠 𝙉𝙄𝙏𝙍𝙊 𝙈𝙀𝙏𝙃𝙊𝘿")
        embed.add_field(name="𝙈𝙀𝙏𝙃𝙊𝘿", value="https://github.com/TEERMIIINAAL/Nitro-Method/blo      b/main/README.md")
        embed.set_image(url="")
        await ctx.send(embed=embed)

@bot.command()
async def cheapboost(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
        embed.set_author(name=" 🌠 𝘾𝙃𝙀𝘼𝙋 𝘽𝙊𝙊𝙎𝙏 𝙈𝙀𝙏𝙃𝙊𝘿")
        embed.add_field(name="𝙈𝙀𝙏𝙃𝙊𝘿", value="https://github.com/TEERMIIINAAL/Cheap-Server-Boo      st/blob/main/README.md")
        embed.set_image(url="")
        await ctx.send(embed=embed)

@bot.command()
async def sdmall(ctx, *, message):
    await ctx.message.delete()
    for user in list(ctx.guild.members):
        try:
            await asyncio.sleep(1)
            await user.send(message)
        except:
            pass

@bot.command()
async def spam(ctx, amount: int, *, message): # b'\xfc'
    await ctx.message.delete()
    for _i in range(amount):
        await ctx.send(message)

@bot.command()
async def htoken(ctx, member : discord.Member=None):
    await ctx.message.delete()
    embed = discord.Embed(title=f"{member}", color=0xff2b41, timestamp=datetime.datetime.utcfromtimestamp(time.time()))
    embed.add_field(name='**User\'s Half Token:**', value=f"{base64.b64encode(bytes(str(member.id), 'utf-8')).decode() + '..........'}", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def disable(ctx, _token):
    await ctx.message.delete()
    r = requests.patch('https://discordapp.com/api/v6/users/@me', headers={'Authorization': _token}, json={'date_of_birth': '2017-7-16'})
    if r.status_code == 400:
       await ctx.send(f"`Account disabled.`")
       print(f'[{Fore.RED}+{Fore.RESET}] Account disabled [SUCCESSFUL]')
    else:
       await ctx.send(f"`Invalid Token`")
       print(f'[{Fore.RED}-{Fore.RESET}] Invalid Token [UNSUCCESSFUL]')

@bot.command()
async def dwebhook(ctx, *, link: str):
    await ctx.message.delete()
    try:
        requests.delete(link)
        await ctx.send("Webhook has been deleted".format(link))
    except Exception as e:
        await ctx.send("Webhook doesnt exist".format(link))

@bot.command()
async def GmailBomb(ctx): # b'\xfc'
    await ctx.message.delete()
    GmailBomber()

#Nsfw Commands
@bot.command()
async def hentai(ctx):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/Random_hentai_gif")
    res = r.json()
    em = discord.Embed()
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@bot.command()
async def boobs(ctx):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/boobs")
    res = r.json()
    em = discord.Embed()
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@bot.command()
async def ass(ctx):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/anal")
    res = r.json()
    em = discord.Embed()
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@bot.command()
async def blowjob(ctx):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/blowjob")
    res = r.json()
    em = discord.Embed()
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@bot.command()
async def waifu(ctx):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/waifu")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"waifu.gif"))
    except:
        em = discord.Embed()
        em.set_image(url=res['url'])
        await ctx.send(embed=em)


#Text commands
@bot.command()
async def snipe(ctx):
    await ctx.message.delete()
    currentChannel = ctx.channel.id
    if currentChannel in bot.sniped_message_dict:
        await ctx.send(bot.sniped_message_dict[currentChannel])
    else:
        await ctx.send("No message to snipe!")

@bot.command(aliases=["esnipe"])
async def editsnipe(ctx):
    await ctx.message.delete()
    currentChannel = ctx.channel.id
    if currentChannel in bot.sniped_edited_message_dict:
        await ctx.send(bot.sniped_edited_message_dict[currentChannel])
    else:
        await ctx.send("No message to snipe!")

@bot.command()
async def flood(ctx):
    await ctx.message.delete()
    await ctx.send('ﾠﾠ' + '\n' * 400 + 'ﾠﾠ')

@bot.command(name='1337speak', aliases=['leetspeak'])
async def _1337_speak(ctx, *, text):
    await ctx.message.delete()
    text = text.replace('a', '4').replace('A', '4').replace('e', '3') \
        .replace('E', '3').replace('i', '!').replace('I', '!') \
        .replace('o', '0').replace('O', '0').replace('u', '|_|').replace('U', '|_|')
    await ctx.send(f'{text}')

@bot.command()
async def minesweeper(ctx, size: int = 5):
    await ctx.message.delete()
    size = max(min(size, 8), 2)
    bombs = [[random.randint(0, size - 1), random.randint(0, size - 1)] for x in range(int(size - 1))]
    is_on_board = lambda x, y: 0 <= x < size and 0 <= y < size
    has_bomb = lambda x, y: [i for i in bombs if i[0] == x and i[1] == y]
    message = "**Click to play**:\n"
    for y in range(size):
        for x in range(size):
            tile = "||{}||".format(chr(11036))
            if has_bomb(x, y):
                tile = "||{}||".format(chr(128163))
            else:
                count = 0
                for xmod, ymod in m_offets:
                    if is_on_board(x + xmod, y + ymod) and has_bomb(x + xmod, y + ymod):
                        count += 1
                if count != 0:
                    tile = "||{}||".format(m_numbers[count - 1])
            message += tile
        message += "\n"
    await ctx.send(message)

@bot.command()
async def reverse(ctx, *, message):
    await ctx.message.delete()
    message = message[::-1]
    await ctx.send(message)


@bot.command()
async def shrug(ctx):
    await ctx.message.delete()
    shrug = r'¯\_(ツ)_/¯'
    await ctx.send(shrug)


@bot.command()
async def lenny(ctx):
    await ctx.message.delete()
    lenny = '( ͡° ͜ʖ ͡°)'
    await ctx.send(lenny)


@bot.command(aliases=["fliptable"])
async def tableflip(ctx):
    await ctx.message.delete()
    tableflip = '(╯°□°）╯︵ ┻━┻'
    await ctx.send(tableflip)


@bot.command()
async def unflip(ctx):
    await ctx.message.delete()
    unflip = '┬─┬ ノ( ゜-゜ノ)'
    await ctx.send(unflip)


@bot.command()
async def bold(ctx, *, message):
    await ctx.message.delete()
    await ctx.send('**' + message + '**')


@bot.command()
async def censor(ctx, *, message):
    await ctx.message.delete()
    await ctx.send('||' + message + '||')

@bot.event
async def on_connect():
    Clear()


@bot.command()
async def underline(ctx, *, message):
    await ctx.message.delete()
    await ctx.send('__' + message + '__')


@bot.command()
async def italicize(ctx, *, message):
    await ctx.message.delete()
    await ctx.send('*' + message + '*')


@bot.command()
async def strike(ctx, *, message):
    await ctx.message.delete()
    await ctx.send('~~' + message + '~~')


@bot.command()
async def quote(ctx, *, message):
    await ctx.message.delete()
    await ctx.send('> ' + message)


@bot.command()
async def code(ctx, *, message):
    await ctx.message.delete()
    await ctx.send('`' + message + "`")

@bot.command()
async def purge(ctx, amount: int):
    await ctx.message.delete()
    async for message in ctx.message.channel.history(limit=amount).filter(lambda m: m.author == bot.user).map(
            lambda m: m):
        try:
            await message.delete()
        except:
            pass

@bot.command()
async def empty(ctx):
    await ctx.message.delete()
    await ctx.send(chr(173))

@bot.command(aliases=["fancy"])
async def ascii(ctx, *, text):
    await ctx.message.delete()
    r = requests.get(f'http://artii.herokuapp.com/make?text={urllib.parse.quote_plus(text)}').text
    if len('```' + r + '```') > 2000:
        return
    await ctx.send(f"```{r}```")

@bot.command()
async def wizz(ctx):
    await ctx.message.delete()
    if isinstance(ctx.message.channel, discord.TextChannel):
        print("hi")
        initial = random.randrange(0, 60)
        message = await ctx.send(f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n`Deleting {len(ctx.guild.roles)} Roles...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n`Deleting {len(ctx.guild.roles)} Roles...\nDeleting {len(ctx.guild.text_channels)} Text Channels...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n`Deleting {len(ctx.guild.roles)} Roles...\nDeleting {len(ctx.guild.text_channels)} Text Channels...\nDeleting {len(ctx.guild.voice_channels)} Voice Channels...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n`Deleting {len(ctx.guild.roles)} Roles...\nDeleting {len(ctx.guild.text_channels)} Text Channels...\nDeleting {len(ctx.guild.voice_channels)} Voice Channels...\nDeleting {len(ctx.guild.categories)} Categories...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n`Deleting {len(ctx.guild.roles)} Roles...\nDeleting {len(ctx.guild.text_channels)} Text Channels...\nDeleting {len(ctx.guild.voice_channels)} Voice Channels...\nDeleting {len(ctx.guild.categories)} Categories...\nDeleting Webhooks...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n`Deleting {len(ctx.guild.roles)} Roles...\nDeleting {len(ctx.guild.text_channels)} Text Channels...\nDeleting {len(ctx.guild.voice_channels)} Voice Channels...\nDeleting {len(ctx.guild.categories)} Categories...\nDeleting Webhooks...\nDeleting Emojis`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n`Deleting {len(ctx.guild.roles)} Roles...\nDeleting {len(ctx.guild.text_channels)} Text Channels...\nDeleting {len(ctx.guild.voice_channels)} Voice Channels...\nDeleting {len(ctx.guild.categories)} Categories...\nDeleting Webhooks...\nDeleting Emojis\nInitiating Ban Wave...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n`Deleting {len(ctx.guild.roles)} Roles...\nDeleting {len(ctx.guild.text_channels)} Text Channels...\nDeleting {len(ctx.guild.voice_channels)} Voice Channels...\nDeleting {len(ctx.guild.categories)} Categories...\nDeleting Webhooks...\nDeleting Emojis\nInitiating Ban Wave...\nInitiating Mass-DM`")
    elif isinstance(ctx.message.channel, discord.DMChannel):
        initial = random.randrange(1, 60)
        message = await ctx.send(
            f"`Wizzing {ctx.message.channel.recipient.name}, will take {initial} seconds to complete`\n")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.recipient.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.recipient.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\nCaching {random.randrange(0, 1000)} Messages...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.recipient.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\nCaching {random.randrange(0, 1000)} Messages...\nDeleting {random.randrange(0, 1000)} Pinned Messages...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.recipient.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\nCaching {random.randrange(0, 1000)} Messages...\nDeleting {random.randrange(0, 1000)} Pinned Messages...\n`")
    elif isinstance(ctx.message.channel, discord.GroupChannel):
        initial = random.randrange(1, 60)
        message = await ctx.send(f"`Wizzing {ctx.message.channel.name}, will take {initial} seconds to complete`\n")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\nCaching {random.randrange(0, 1000)} Messages...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\nCaching {random.randrange(0, 1000)} Messages...\nDeleting {random.randrange(0, 1000)} Pinned Messages...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\nCaching {random.randrange(0, 1000)} Messages...\nDeleting {random.randrange(0, 1000)} Pinned Messages...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\nCaching {random.randrange(0, 1000)} Messages...\nDeleting {random.randrange(0, 1000)} Pinned Messages...\nKicking {len(ctx.message.channel.recipients)} Users...`")


@bot.command(aliases=['slots', 'bet', "slotmachine"])
async def slot(ctx):
    await ctx.message.delete()
    emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
    a = random.choice(emojis)
    b = random.choice(emojis)
    c = random.choice(emojis)
    slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"
    if a == b == c:
        await ctx.send(embed=discord.Embed.from_dict(
            {"title": "Slot machine", "description": f"{slotmachine} All matchings, you won!"}))
    elif (a == b) or (a == c) or (b == c):
        await ctx.send(embed=discord.Embed.from_dict(
            {"title": "Slot machine", "description": f"{slotmachine} 2 in a row, you won!"}))
    else:
        await ctx.send(embed=discord.Embed.from_dict(
            {"title": "Slot machine", "description": f"{slotmachine} No match, you lost"}))

@bot.command()
async def abc(ctx):
    await ctx.message.delete()
    ABC = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z']
    message = await ctx.send(ABC[0])
    await asyncio.sleep(2)
    for _next in ABC[1:]:
        await message.edit(content=_next)
        await asyncio.sleep(2)

@bot.command(aliases=["jerkoff", "ejaculate", "orgasm"])
async def cum(ctx):
    await ctx.message.delete()
    message = await ctx.send('''
            :ok_hand:            :smile:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8=:punch:=D
             :trumpet:      :eggplant:''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :smiley:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8==:punch:D
             :trumpet:      :eggplant:
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :grimacing:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8=:punch:=D
             :trumpet:      :eggplant:
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :persevere:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8==:punch:D
             :trumpet:      :eggplant:
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :confounded:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8=:punch:=D
             :trumpet:      :eggplant:
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :tired_face:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8==:punch:D
             :trumpet:      :eggplant:
             ''')
    await asyncio.sleep(0.5)
    await message.edit(contnet='''
                       :ok_hand:            :weary:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8=:punch:= D:sweat_drops:
             :trumpet:      :eggplant:
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :dizzy_face:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8==:punch:D :sweat_drops:
             :trumpet:      :eggplant:                 :sweat_drops:
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :drooling_face:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8==:punch:D :sweat_drops:
             :trumpet:      :eggplant:                 :sweat_drops:
     ''')

@bot.command(aliases=["del", "quickdel"])
async def quickdelete(ctx, *, args):
    await ctx.message.delete()
    await ctx.send(args, delete_after=1)

@bot.command(aliases=["9/11", "911", "terrorist"])
async def nine_eleven(ctx):
    await ctx.message.delete()
    invis = ""  # char(173)
    message = await ctx.send(f'''
{invis}:man_wearing_turban::airplane:    :office:
''')
    await asyncio.sleep(0.5)
    await message.edit(content=f'''
{invis} :man_wearing_turban::airplane:   :office:
''')
    await asyncio.sleep(0.5)
    await message.edit(content=f'''
{invis}  :man_wearing_turban::airplane:  :office:
''')
    await asyncio.sleep(0.5)
    await message.edit(content=f'''
{invis}   :man_wearing_turban::airplane: :office:
''')
    await asyncio.sleep(0.5)
    await message.edit(content=f'''
{invis}    :man_wearing_turban::airplane::office:
''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
        :boom::boom::boom:
        ''')

@bot.command()
async def tts(ctx, *, message):
    await ctx.message.delete()
    buff = await do_tts(message)
    await ctx.send(file=discord.File(buff, f"{message}.wav"))

#server builder
@bot.command()
async def buildtemplate1(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=0xff2b41)
    embed.set_author(name="💉 Server builder has been opened, look at your browser 💉", icon_url="https://cdn.freebiesupply.com/logos/large/2x/panda-7-logo-png-transparent.png")
    await ctx.send(embed=embed)
    await os.system('start https://discord.new/NxSj7Z5jhV83')

@bot.command()
async def buildtemplate2(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=0xff2b41)
    embed.set_author(name="💉 Server builder has been opened, look at your browser 💉", icon_url="https://cdn.freebiesupply.com/logos/large/2x/panda-7-logo-png-transparent.png")
    await ctx.send(embed=embed)
    await os.system('start https://discord.com/template/WRp8JrT37kkc')

@bot.command()
async def buildtemplate3(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=0xff2b41)
    embed.set_author(name="💉 Server builder has been opened, look at your browser 💉", icon_url="https://cdn.freebiesupply.com/logos/large/2x/panda-7-logo-png-transparent.png")
    await ctx.send(embed=embed)
    await os.system('start https://discord.com/template/Wx8CkEV6b7BN')

@bot.command()
async def buildtemplate4(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=0xff2b41)
    embed.set_author(name="💉 Server builder has been opened, look at your browser 💉", icon_url="https://cdn.freebiesupply.com/logos/large/2x/panda-7-logo-png-transparent.png")
    await ctx.send(embed=embed)
    await os.system('start https://discord.com/template/8Pq7aTucMTd6')

@bot.command()
async def buildtemplate5(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=0xff2b41)
    embed.set_author(name="💉 Server builder has been opened, look at your browser 💉", icon_url="https://cdn.freebiesupply.com/logos/large/2x/panda-7-logo-png-transparent.png")
    await ctx.send(embed=embed)
    await os.system('start https://discord.com/template/XpqYx5asn3UT')

@bot.command()
async def buildtemplate6(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=0xff2b41)
    embed.set_author(name="💉 Server builder has been opened, look at your browser 💉", icon_url="https://cdn.freebiesupply.com/logos/large/2x/panda-7-logo-png-transparent.png")
    await ctx.send(embed=embed)
    await os.system('start https://discord.com/template/3Mv9YjYySCQW')

@bot.command()
async def buildtemplate7(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=0xff2b41)
    embed.set_author(name="💉 Server builder has been opened, look at your browser 💉", icon_url="https://cdn.freebiesupply.com/logos/large/2x/panda-7-logo-png-transparent.png")
    await ctx.send(embed=embed)
    await os.system('start https://discord.com/template/PzyTmafcuzDJ')

@bot.command()
async def buildtemplate8(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=0xff2b41)
    embed.set_author(name="💉 Server builder has been opened, look at your browser 💉", icon_url="https://cdn.freebiesupply.com/logos/large/2x/panda-7-logo-png-transparent.png")
    await ctx.send(embed=embed)
    await os.system('start https://discord.com/template/n7cKgN6VkH6w')

@bot.command()
async def buildtemplate9(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=0xff2b41)
    embed.set_author(name="💉 Server builder has been opened, look at your browser 💉", icon_url="https://cdn.freebiesupply.com/logos/large/2x/panda-7-logo-png-transparent.png")
    await ctx.send(embed=embed)
    await os.system('start https://discord.com/template/zcPYVPy4uq4S')

@bot.command()
async def buildtemplate10(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=0xff2b41)
    embed.set_author(name="💉 Server builder has been opened, look at your browser 💉", icon_url="https://cdn.freebiesupply.com/logos/large/2x/panda-7-logo-png-transparent.png")
    await ctx.send(embed=embed)
    await os.system('start https://discord.com/template/AzhSzjMR3pkk')

#moderation commands

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member = None):
  if member is None:
     await ctx.send(f"{ctx.author.mention} You must mention a user to do that!")
  else:
   embed = discord.Embed(color=(0xff2b41), timestamp=ctx.message.created_at)
  embed.description = f"{member.mention} has been banned by {bot.user.name}"
  await member.ban()
  await ctx.send(embed=embed)

@ban.error
async def ban_error(ctx, error):
  if isinstance(error, (commands.BadArgument)):
    embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
    embed.title=("ERROR")
    embed.description=f"User was not found ping the right person!"
    await ctx.send(embed=embed)
  else:
    raise error


@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member = None):
  if member is None:
     await ctx.send(f"{ctx.author.mention} You must mention a user to do that!")
  else:
   embed = discord.Embed(color=(0xff2b41), timestamp=ctx.message.created_at)
  embed.description = f"{member.mention} has been kicked by {bot.user.name}"
  await member.kick()
  await ctx.send(embed=embed)

@kick.error
async def kick_error(ctx, error):
  if isinstance(error, (commands.BadArgument)):
    embed = discord.Embed(color=0xff2b41, timestamp=ctx.message.created_at)
    embed.title=("ERROR")
    embed.description=f"User was not found ping the right person!"
    await ctx.send(embed=embed)
  else:
    raise error

@bot.command(pass_context=True)
async def clear(ctx, limit:int):
  await ctx.channel.purge(limit=limit)
  await ctx.send('Cleared by {}'.format(ctx.author.mention))
  await asyncio.sleep(3)
  await ctx.message.delete()



#Bot Token runner
bot.run(token, bot=False)