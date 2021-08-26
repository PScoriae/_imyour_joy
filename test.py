from bs4 import BeautifulSoup, SoupStrainer
import requests
import random
import re

# website doesn't parse requests for a page above 100.
# thus, this function checks if the actual number of pages is > 100
# if it is, then the range is limited to 100, else it is maintained.
def getOfficialRange(noOfPages):
    if noOfPages > 100:
        return 100
    else:
        return noOfPages

# def profile(arg):
#     tmp = arg.split(' ')
#     name = '-'.join(tmp)
#     site = "https://kprofiles.com"
#     searchString = f'{site}/{name}-members-profile'
#     search = requests.get(searchString)
#     only_p = SoupStrainer('p')
#     soup = BeautifulSoup(search.text, 'lxml', parse_only=only_p)
#     first = soup.find('p')
#     img = first.find('img').get('src')
#     text = first.get_text().split('\n')[2]
#     print(img)
#     print(text)

def profile(ctx, *, arg):
    tmp = arg.split(' ')
    name = '-'.join(tmp)
    site = "https://kprofiles.com"
    
    def attemptSearch(site, name):
        possible = [f'{site}/{name}-members-profile', f'{site}/{name}-profile']
        for link in possible:
            try:
                return requests.get(link)
            except:
                return False

    search = attemptSearch(name, site)           

    if search == False:
        await ctx.send('없어요 ㅠㅠ')
    else:
        only_p = SoupStrainer('p')
        soup = BeautifulSoup(search.text, 'lxml', parse_only=only_p)
        first = soup.find('p')
        img = first.find('img').get('src')
        text = first.get_text().split('\n')[-1]
        await ctx.send(img)
        await ctx.send(text)