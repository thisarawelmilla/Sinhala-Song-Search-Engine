import csv
import urllib.request
import time
from bs4 import BeautifulSoup
import numpy  as np
import pandas as pd
import csv
import requests
from urllib.request import Request, urlopen


def scrape_song_links(src_url):
    page = Request(src_url, headers={'User-Agent': 'Mozilla/5.0'})
    infile=urllib.request.urlopen(page).read()
    soup = BeautifulSoup(infile, 'html.parser', from_encoding="utf-8")
    all_link_list = []
    for link in soup.findAll('h4'):
        for i in link.findAll('a'):
            all_link_list.append(i.get('href'))
    return all_link_list



def scrape_song_details(url, l):
    page = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    infile=urllib.request.urlopen(page).read()
    soup = BeautifulSoup(infile, 'html.parser', from_encoding="utf-8")
    all_link_list = []
    for detail in soup.findAll('span'):
        text = detail.get_text().split(':')
        if text[0] == 'Genre':
            genre = text[1].split(',')
        if text[0] == 'Lyrics':
            composer = text[1]
        if text[0] == 'Music':
            music = text[1]
    singer = soup.find('h6', attrs={'class':'artist-name'}).get_text().strip(' ').split('/')[0]
    print(soup.find('h6', attrs={'class':'artist-name'}).get_text().strip(' ').split('/'))
    if len(soup.find('h6', attrs={'class':'artist-name'}).get_text().strip(' ').split('/'))==2:
        l[soup.find('h6', attrs={'class':'artist-name'}).get_text().strip(' ').split('/')[1]] = singer
    popularity = soup.find('div', attrs={'class':'tptn_counter'}).get_text()
    title = soup.find('span', attrs={'class':'sinTitle'}).get_text()
    cord = soup.find('h3').get_text().split('|')
    key  = cord[0].split(':')[1].strip(' ')
    beat  = cord[1].split(':')[1].strip(' ')
    lyrics_data = soup.findAll('pre')[0].get_text().split('\n')
    n = 0    
    ly_line = False
    lyrics= ''
    formatted_lyrics = ''
    for n in range(len(lyrics_data)):
        i = lyrics_data[n]
        if ly_line:
            m += 1
            if len(i)== 0:
                formatted_lyrics += '\n'
                ly_line = False      
            else:
                if m%2 == 0:
                    lyrics += i
                    formatted_lyrics += i + ('\n')             
        if i.split(' ')[0] == 'VEARSE' or i.split(' ')[0] == 'VERSE' or i.split(' ')[0] == 'CHORUS':
            ly_line = True
            m = 0 
        n+=1

    return [title, singer, genre, composer, music, key, beat, popularity[3:-6], lyrics, formatted_lyrics], l


l={}
page_links = ['https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/']
root_link = 'https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/?_page='
for page_num in range(2, 23):
    page_links.append(root_link + str(page_num))


song_links = []
for page in page_links:
    song_links += scrape_song_links(page)
    time.sleep(1)


n = 1
song_data = []
for link in song_links:
    try:
        song, l = scrape_song_details(link, l)
        print(l)
        song_data.append(song)
        time.sleep(1)
    except :
        print(n, 'error')
    if n%200 == 0:      
        df = pd.DataFrame(song_data, columns=['title', 'singer', 'genre', 'composer', 'music', 'key', 'beat', 'popularity', 'lyrics', 'formatted_lyrics'])
        df.to_csv('scraped_songs' + str(n) +'.csv', encoding = 'utf-8', index=False)
    n+=1


import codecs
with codecs.open('/home/thisara/Documents/sem 7/Data Mining/ir_project_160684E/ar.txt', 'w+', encoding='utf-8') as json_file:
    json_file.write(str(l))
    



