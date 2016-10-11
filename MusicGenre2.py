#! python3

#type out the MusicScraper with the argument of root directory for music folders
# sudo python3 /$HOME/Desktop/MusicGenre.py /Volumes/Padlock/Music_Jenn/"This Is Not A Game"/

#Define the scope of scandir as functions; such as Resurively or only at Root
#sauce: http://stackoverflow.com/questions/33135038/how-do-i-use-os-scandir-to-return-direntry-objects-recursively-on-a-directory
#doc: https://www.python.org/dev/peps/pep-0471/
try:
    from os import scandir
except ImportError:
    from scandir import scandir  # use scandir PyPI module on Python < 3.5

def scanroot(path):
    """Yield DirEntry objects for given directory."""
    for entry in scandir(path):
        if not entry.name.startswith('.') and entry.is_dir():
            yield entry.name

#Create the ScraperList
musicscrape = []

#Run the scanroot function to list all directories in root
if __name__ == '__main__':
    import sys
    for entry in scanroot(sys.argv[1] if len(sys.argv) > 1 else '.'):
        #print(entry)
        musicscrape.append(entry) #Create the working list of artists
    #print(musicscrape)

#sauce: http://www.blog.pythonlibrary.org/2012/06/08/python-101-how-to-submit-a-web-form/
#sauce = http://stackoverflow.com/questions/2935658/beautifulsoup-get-the-contents-of-a-specific-table
#prettify_doc = http://stackoverflow.com/questions/34961559/python-beautifulsoup-prettify-attributeerror
#structure the webform variables
try:
    import urllib.request
    from bs4 import BeautifulSoup
    #import re
    #import json
except ImportError:
    print('Its all fucked')
    print('Youre missing urllib')
    print('Do you have python3?')
    print('Its all fucked')
    print("execute: sudo easy_install pip3")
    print("then execute: pip3 install beautifulsoup4")

def requestcraft(artist_q_url):
    """submit a query to musicbrainz.com"""
    musicbrainz = 'http://musicbrainz.org'
    with urllib.request.urlopen(artist_q_url) as response:
        soup = BeautifulSoup(response.read(), 'html.parser')
        tbl_score = soup.tbody.tr.find_all("td", limit=2)
        for i in (tbl_score): #for each iterable line in ResultSet Object
            if i.find_all('a'): # search for an 'a' tag
                #print(i.a['href']) # print tag 'a', attribute 'href'
                href_orig = i.a['href']
                i.a['href'] = musicbrainz + href_orig
                #print(i.a['href'])
                with open("table.html", "ab") as f:
                    f.write(("Score: ").encode('utf-8'))
                    f.write(tbl_score[0].prettify(formatter="html").encode('utf-8'))
                    f.write(("Artist: ").encode('utf-8'))
                    f.write(i.prettify(formatter="html").encode('utf-8'))
                    f.write(("Original Artist: " + artist).encode('utf-8'))
                    f.close
                with urllib.request.urlopen(i.a['href']) as wo_fat:
                    budosoup = BeautifulSoup(wo_fat.read(), 'html.parser')
                    genre = budosoup.find(id="sidebar-tags")
                    #print(genre.prettify())
                    for t in genre:
                        for string in t:
                            text = str(string)
                            print(text)
                    with open("table.html", "ab") as f:
                        #f.write(("Tag: ").encode('utf-8'))
                        f.write(genre.prettify(formatter="html").encode('utf-8'))
                        f.close

if __name__ == '__main__':
    import sys
    #print(musicscrape)
    #musicscrape = ['Atlas','Truckfighters']
    for artist in musicscrape:
        artist_clean = artist.replace(" ", "+")
        try:
            print("Researching Artist:", artist)
            artist_q_url = 'http://musicbrainz.org/search?query=' + artist_clean + '&type=artist&method=indexed'
            requestcraft(artist_q_url)
        except Exception as e:
            print(e)
            continue
