from bs4 import BeautifulSoup
import urllib.request
import fileinput

f = open("links.txt", "r")
f1 = f.readlines()
f2 = open("lyrics.txt", "w+")

def get_lyrics():
    for x in f1:
        page = urllib.request.urlopen(x).read()
        soup = BeautifulSoup(page, 'html.parser')
        lyrics = str(soup)
        top_text = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        bottom_text = '<!-- MxM banner -->'
        lyrics = lyrics.split(top_text)[1]
        lyrics = lyrics.split(bottom_text)[0]
        lyrics = lyrics.replace('<br>','').replace('</br>','').replace('</div>','').replace('<br/>','').strip()
        f2.write(lyrics)

get_lyrics()
f.close()
f2.close()
