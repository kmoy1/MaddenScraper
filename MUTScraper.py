from bs4 import BeautifulSoup as bs
import requests
import re
import os
import csv   

player_URL = "https://www.muthead.com/21/players/"
# MUT_page = requests.get(base_URL)
# soup = bs(MUT_page.content, 'html.parser')

def scrapeInfo(ID):
    """Return (name, OVR, program, XBOX market price) given madden card ID."""
    URL = player_URL + str(ID) + "/"
    player_page = requests.get(URL)
    soup = bs(player_page.content, 'html.parser')
    mp = soup.find('span', class_='mut-player-price__price').contents[0] #Get market price.
    info_str = soup.find('title').contents[0]
    pattern = r'\s+(\w+\s\w+)\s-\s+21\s-\s+(\d+)\s\w+\s([\w\s]+)'
    name, ovr, program = re.findall(pattern, info_str)[0]
    program = program.rstrip()
    ovr = int(re.findall(r'\d+', ovr)[0])
    if 'K' in mp:
        mp = int(mp.replace('K', '')) * 1000
    return name, ovr, program, mp

def scrapeSets(ID):
    """Scrape valid sets given madden 21 card ID."""
    pass

def playersCSV():
    """Populate players CSV: (Name, OVR, Program, Market Price (XBOX), Position"""
    output = open('MUT21Players.csv', mode='w', newline='')
    output_writer = csv.writer(output)
    output_writer.writerow(['Name', 'OVR',  'Program', 'Market Price', 'Position'])

    URL = "https://www.muthead.com/21/players/?page="

    for i in range(1, 100):
        page_i = URL + str(i)
        player_page = requests.get(page_i)
        soup = bs(player_page.content, 'html.parser')
        pattern = r"\s+(\d+)\s+(\S+(?: \S+)*)\s+(\w+)[^\w]+(\S+(?: \S+)*)[^\w]+(\w+)"
        for tag in soup.find_all('li', class_="player-listing__item"):
            # print(tag.text)
            ovr, name, pos, program, mp = re.findall(pattern, tag.text)[0]
            # if name == 'Jalen Ramsey':
            #     print(tag.text)
            ovr = int(ovr)
            if 'K' in mp:
                mp = int(mp.replace('K', '')) * 1000
            else:
                try:
                    mp = int(mp)
                except:
                    mp = 'Unknown'
            output_writer.writerow([name, ovr, program, mp, pos])



playersCSV()
