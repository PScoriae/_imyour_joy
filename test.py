from bs4 import BeautifulSoup, SoupStrainer
import requests
import random
import re

def wiki():
    html = requests.get('https://kpop.fandom.com/wiki/IZ*ONE')
    only_mw_parser_output = SoupStrainer('div', class_='mw-parser-output')
    soup = BeautifulSoup(html.text, 'lxml', parse_only=only_mw_parser_output)

    text = soup.find('aside', class_='portable-infobox pi-background pi-border-color pi-theme-artist pi-layout-default')
    info = text.next_sibling.next_sibling
    list = []
    while True:
        if info.name is not None:
            modified = info.get_text()
            list.append(modified)
        else:
            list.append(info)
        info = info.next_sibling
        if info is None:
            break
    
    info = ''.join(list).replace('\n', '')
    print(info)

    img = text.find('a', class_='image image-thumbnail').get('href')
    print(img)

    # data = text.find_all('section', class_='pi-item pi-group pi-border-color pi-collapse pi-collapse-open')
    # for item in data:
    #     if item.find('h2', class_='pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background').get_text():
    #         ab = item.find('h2', class_='pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background').get_text()
    #         print(ab)
    #     elif item.find('caption', class_='pi-header pi-secondary-font pi-secondary-background pi-item-spacing'):
    #         bc = item.find('caption', class_='pi-header pi-secondary-font pi-secondary-background pi-item-spacing')
    #         print(bc)

    # data1 = text.find_all('h2', class_='pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background')
    # print(data1)
wiki()