import discord
from discord.ext import commands
from bs4 import BeautifulSoup, SoupStrainer
import requests
import random
import re

# gets bot token
with open('token.txt') as txt:
    token = txt.readline()
    
client = commands.Bot(command_prefix='j')

# prints successful login and sets bot status
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("with Pie")
    await client.change_presence(activity=game)

# sends 안녕 song by Joy
@client.command()
async def hello(ctx):
    await ctx.send("https://youtu.be/lNvBbh5jDcA")

# retrieves profile information and picture from kprofiles.com
@client.command()
async def prof(ctx, *, arg):
    tmp = arg.split(' ')
    name = '-'.join(tmp)
    site = "https://kprofiles.com"
    url_tuple = (f'{site}/{name}-members-profile', f'{site}/{name}-profile')

    search = await scrapeProf(url_tuple)           

    if search == False:
        await ctx.send('없어요 ㅠㅠ')
    else:
        embedMsg = discord.Embed(description=search[1], color=0x2ecc71)
        embedMsg.set_image(url=search[0])
        await ctx.send(embed=embedMsg)

# requests and parses HTML for search
async def parseProf(link):
    search = requests.get(link)
    only_p = SoupStrainer('p')
    soup = BeautifulSoup(search.text, 'lxml', parse_only=only_p)  
    return soup

# scrapes img and text from site
async def scrapeProf(url_tuple):
    img_text = []
    attempts = 0
    for link in url_tuple:
        try:
            soup = await parseProf(link)
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

# sends randomly scraped image from kpop.asiachan.com
@client.command()
async def git(ctx):
    await ctx.send('https://github.com/PScoriae/_imyour_joy')

@client.command()
async def pic(ctx, *, arg):
    site = "https://kpop.asiachan.com"
    searchString = f'{site}/{arg}?s=id' # searches for person sorted by recent
    try:
        soup = await parsePicPages(searchString)
        noOfPages = await scrapePicPages(soup)

        # gets a random page number within constraints.
        randomPage = random.randint(0, getOfficialRange(noOfPages))
        soup = await parsePicImages(searchString, randomPage)

        listOfFull = await scrapePicImages(soup)
        randomLink = random.randint(0, len(listOfFull) - 1)
        link = listOfFull[randomLink]
        await ctx.send(link)
    except:
        await ctx.send("없어요 ㅠㅠ")

# requests and parses HTML
async def parsePicPages(searchString):
    search = requests.get(searchString)
    only_pagination = SoupStrainer(class_='pagination')
    soup = BeautifulSoup(search.text, 'lxml', parse_only=only_pagination)
    return soup

# determines number of pages available for search
async def scrapePicPages(soup):
    tmp = soup.find('p', class_='pagination').get_text(strip=True).split(' ')[3]
    noOfPages = int(re.findall('\d+', tmp)[0])
    return noOfPages

# requests and parses HTML for randomly chosen page
async def parsePicImages(searchString, randomPage):
    search = requests.get(f'{searchString}&p={randomPage}')
    only_a = SoupStrainer('a')
    soup = BeautifulSoup(search.text, 'lxml', parse_only=only_a)
    return soup

# returns list of image links on page
async def scrapePicImages(soup):
    as_ = soup.find_all('a')
    listOfFull = []
    for a in as_:
        tmp = str(a.get('href'))
        if 'full' in tmp:
            listOfFull.append(tmp)
    return listOfFull

# website breaks when there are requests for a page above 100.
# thus, this function checks if the actual number of pages is > 100
# if it is, then the range is limited to 100, else it is maintained.
def getOfficialRange(noOfPages):
    if noOfPages > 100:
        return 100
    else:
        return noOfPages

# test command for pinging author of command
@client.command()
async def test(ctx):
    await ctx.send(ctx.author.mention)

client.run(token)
