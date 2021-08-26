import discord
from discord.ext import commands
from bs4 import BeautifulSoup, SoupStrainer
import requests
import random
import re
import time

with open('./token.txt') as txt:
    token = txt.readline()
    
client = commands.Bot(command_prefix='j')

# website doesn't parse requests for a page above 100.
# thus, this function checks if the actual number of pages is > 100
# if it is, then the range is limited to 100, else it is maintained.
def getOfficialRange(noOfPages):
    if noOfPages > 100:
        return 100
    else:
        return noOfPages

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("with Pie")
    await client.change_presence(activity=game)

@client.command()
async def hello(ctx):
    start = time.time()
    await ctx.send("https://youtu.be/lNvBbh5jDcA")
    end = time.time()
    await ctx.send(f'Took {end-start} seconds')

async def attemptSearch(site, name):
    possible = [f'{site}/{name}-members-profile', f'{site}/{name}-profile']
    img_text = []
    attempts = 0
    for link in possible:
        try:
            search = requests.get(link)
            only_p = SoupStrainer('p')
            soup = BeautifulSoup(search.text, 'lxml', parse_only=only_p)
            first = soup.find('p')
            img = first.find('img').get('src')
            text = first.get_text().split('\n')[-1]
            img_text.append(img)
            img_text.append(text)
            return img_text
        except AttributeError:
            attempts += 1
            if attempts == 2:
                return False
            continue

@client.command()
async def prof(ctx, *, arg):
    start = time.time()
    tmp = arg.split(' ')
    name = '-'.join(tmp)
    site = "https://kprofiles.com"

    search = await attemptSearch(site, name)           

    if search == False:
        await ctx.send('없어요 ㅠㅠ')
    else:
        embedMsg = discord.Embed(description=search[1], color=0x2ecc71)
        embedMsg.set_image(url=search[0])
        # await ctx.send(search[0])
        # await ctx.send(search[1])
        await ctx.send(embed=embedMsg)
        end = time.time()
        await ctx.send(f'Took {end - start} seconds')

@client.command()
async def pic(ctx, *, arg):
    site = "https://kpop.asiachan.com"
    searchString = f'{site}/{arg}?s=id' # searches for person sorted by recent
    try:
        search = requests.get(searchString)
        only_pagination = SoupStrainer(class_='pagination')
        soup = BeautifulSoup(search.text, 'lxml', parse_only=only_pagination)

        # goes to pagination class and finds out the maximum number of pages.
        # will be used as the limit for the randomizer.
        tmp = soup.find('p', class_='pagination').get_text(strip=True).split(' ')[3]
        noOfPages = int(re.findall('\d+', tmp)[0])

        # gets a random page number within constraints.
        randomPage = random.randint(0, getOfficialRange(noOfPages))
        search = requests.get(f'{searchString}&p={randomPage}')
        only_a = SoupStrainer('a')
        soup = BeautifulSoup(search.text, 'lxml', parse_only=only_a)
        
        as_ = soup.find_all('a')
        listOfFull = []
        for a in as_:
            tmp = str(a.get('href'))
            if 'full' in tmp:
                listOfFull.append(tmp)
        
        randomLink = random.randint(0, len(listOfFull) - 1)
        link = listOfFull[randomLink]
        await ctx.send(link)
    except:
        await ctx.send("없어요 ㅠㅠ")

client.run(token)
