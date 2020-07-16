from bs4 import BeautifulSoup
import re
import urllib.request
import songlist

artist = songs.artist

def give_url(song_title):
    url_lyrics = "https://www.azlyrics.com/lyrics/" + artist + "/" + song_title + ".html"
    return url_lyrics

f = open("songs.txt", "r")
f1 = f.readlines()
f2 = open("links.txt", "w+")

for x in f1:
    song_title = re.sub('[^A-Za-z0-9]+', "", x)
    song_title = song_title.lower()
    url = give_url(song_title)
    f2.write(url+"\n")

f.close()
f2.close()

