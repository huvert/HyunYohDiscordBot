import os
import discord
import requests
import youtube_dl
from HyuonYohLib import getHyuonYohMessage
from HyuonYohLib import hyunYohify
from discord.ext import commands
import asyncio
from random import randint
import datetime


# Cant upload TOKEN to github. Needs to be stored locally on machine.
# Use .gitignore :)
from TOKEN import TOKEN
PREFIX = '_'
MEME_CH_ID = 1014781327347822633

# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''


bot = commands.Bot(PREFIX, description='Hyun Yoh Bot')


for filename in os.listdir(f"{os.getcwd()}\HuyonYohBot\cogs"):   # ./ --> Current folder
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

msg = ""





# ------------------------------------
# ----------    Commands    ----------
@bot.event
async def on_ready():
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))
    
    '''
    # INITIAL WAIT
    now = datetime.datetime.now()
    today = datetime.date.today()
    then = datetime.datetime(today.year,today.month,today.day,12,00,00)
    wait_time = abs(then-now).total_seconds()
    await asyncio.sleep(wait_time)

    # LOOP FOR DAILY MESSAGE
    while True:
        r = randint(0,100)
        if r < 10:      #Chance for an insult
            msg = requests.get('https://evilinsult.com/generate_insult.php?lang=en').text.upper()
            msg = msg.replace("'","") #Hyon Yoh doesnt use '
            msg = list(msg.split(" "))
            msg = hyunYohify(msg)
        else:           # Chance for todays inspirational quote
            msg = getHyuonYohMessage(type="today")
        channel = bot.get_channel(MEME_CH_ID)
        print(msg)
        await channel.send(msg)
        await asyncio.sleep(60*60*24)
    '''
    

@bot.command()
async def inspirational(ctx):
    '''Returns a random inspirational quote'''
    msg = getHyuonYohMessage(type="random")
    print(msg)
    await ctx.send(msg)


@bot.command()
async def todaysquote(ctx):
    '''Returns todays inspirational quote'''
    msg = getHyuonYohMessage(type="today")
    print(msg)
    await ctx.send(msg)



@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency * 1000)}ms')


@bot.command()
async def clear(ctx, amount=1):
    """Clear 'x' number of messages. ex: _clear 3"""
    await ctx.channel.purge(limit=(amount+1))


@bot.command()
async def insult(ctx):
    """Random insult"""
    res = requests.get('https://evilinsult.com/generate_insult.php?lang=en').text.upper()
    res = res.replace("'","") #Hyon Yoh doesnt use '
    res = list(res.split(" "))
    insult = hyunYohify(res)
    await ctx.send(insult)


@bot.command()
async def nobody(ctx):
    """Returns AI-generated image of a person"""
    res = requests.get('https://thispersondoesnotexist.com/image')
    if res.status_code == 200:
        with open('nobody.png', 'wb') as f:
            f.write(res.content)
        with open('nobody.png', 'rb') as f:
            await ctx.send("HERE YUO HEV IS BUTIFULL PESHON\n", file=discord.File(f))
    else:
        await ctx.send("SOMETHING WONG (((((")


@bot.command()
async def pwbreach(ctx, myPasswordSHA1):
    """Checks for pw-breaches. Input: Your pw in SHA-1 format"""
    res = requests.get(f"https://api.pwnedpasswords.com/range/{myPasswordSHA1[:5]}")
    myPW = myPasswordSHA1[5:]
    mes = "No breaches found! :D"
    print(res.status_code)
    if res.status_code == 200:
        content = res.text.split("\r\n")
        print(content)
        for cnt in content:
            if myPW == cnt[:35]:
                print("[bot] Password has been breached!")
                x = cnt.split(":")
                mes = f"Your password has been found in breached files {x[1]} times!"
    else:
        mes = "SOMETHING WONG ((((("
    await ctx.send(mes)


@bot.command()
async def HELPpwbreach(ctx):
    """Shows more info about function 'pwbreach'"""
    await ctx.send("""***DO NOT TYPE YOUR OWN UNENCRYPTED PASSWORD ON DISCORD!***\n
    function should be used as follows:
    \t \t_pwbreach 'Passowrd in format SHA-1'
    ex:\t_pwbreach FFC0F2952FD99C4B9147D6A101D031DABB9\n
    visit https://www.cleancss.com/sha1-hash-generator/ for SHA-1 convertion""")


bot.run(TOKEN)
