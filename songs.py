from bs4 import BeautifulSoup
import re
import urllib.request

def artist_name():
    artist = input("Enter the name of the artist: ")
    artist = artist.lower()
    if artist.startswith("the"):
        artist = artist[3:]
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    return artist

artist = artist_name()
url_artist = "https://www.azlyrics.com/" + artist[:1] + "/" + artist + ".html"

page = urllib.request.urlopen(url_artist).read()
soup = BeautifulSoup(page, 'html.parser')
songs = soup.findAll("div", {"class":"listalbum-item"})
f = open("songs.txt", "w+")
for song in songs:
    f.write(song.text+"\n")

f.close()

