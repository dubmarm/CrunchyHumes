#! python3

# this music scrapper is an abomination, I know this, but I'm learning
# so deal with it.

# what it's supposed to do, is get a list of directories in a root music folder
# the folders are expected to be titled after artists
# the script then dumps the list of folders/artists into a list
# an iteration is performed on the artist list and urllib queries musicbrainz
# if an artist match is made with musicbrainz, then another iteration is performed
# where the 'tags' are pulled from the artist's musicbrainz profile page
# after the artist tag iteration, the results are written to a file, called table.html
# the table.html will list the artist and the tags associated with the artist

# though ugly, this little scrapper helped me find new artists in a folder
# that held over 600GB of music and 1833 artists.
# thanks for the tunes humes!

# type out the MusicScraper with the argument of root directory for music folders
# sudo python3 /$HOME/Desktop/MusicGenre.py /Volumes/Padlock/MusicRoot/

# for this script you will need:
# Python3
# urllib
# BeautifulSoup

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

#sauce: http://www.blog.pythonlibrary.org/2012/06/08/python-101-how-to-submit-a-web-form/
#sauce = http://stackoverflow.com/questions/2935658/beautifulsoup-get-the-contents-of-a-specific-table
#prettify_doc = http://stackoverflow.com/questions/34961559/python-beautifulsoup-prettify-attributeerror
#structure the webform variables
try:
    import urllib.request
    from bs4 import BeautifulSoup
except ImportError: # i really need to practice exception handling
    print('Its all fucked')
    print('Youre missing urllib') # i'd like to see if python can check for urllib
    print('Do you have python3?') # i'd like to see if python can check it's version
    print("execute: sudo easy_install pip3")
    print("then execute: pip3 install beautifulsoup4") # i'd like to see if python can check for beautifulsoup

def requestcraft(artist_q_url):
    """submit a query to musicbrainz.com"""
    musicbrainz = 'http://musicbrainz.org'
    with urllib.request.urlopen(artist_q_url) as response:
        soup = BeautifulSoup(response.read(), 'html.parser')
        tbl_score = soup.tbody.tr.find_all("td", limit=2)
        for i in (tbl_score): #for each iterable line in ResultSet Object
            if i.find_all('a'): # search for an 'a' tag
                href_orig = i.a['href']
                i.a['href'] = musicbrainz + href_orig
                with urllib.request.urlopen(i.a['href']) as wo_fat:
                    budosoup = BeautifulSoup(wo_fat.read(), 'html.parser')
                    genre = budosoup.find(id="sidebar-tags")

                    """wrap these details up and send off to tickles for I/O"""
                    ftags = genre.prettify(formatter="html")#.encode('utf-8')
                    fscore = tbl_score[0].prettify(formatter="html")#.encode('utf-8')
                    fartist = i.prettify(formatter="html")#.encode('utf-8')
                    ffolder = artist#.encode('utf-8')
                    tickles(fscore, fartist, ffolder, ftags)

def tickles(fscore, fartist, ffolder, ftags):
    try:
        with open("table.html", "a") as f:
            print("Writing " + artist + " to file")
            f.write("Score: ") #("Score: ").encode('utf-8'))
            f.write(fscore)
            f.write("Artist: ")#("Artist: ").encode('utf-8'))
            f.write(fartist) #haha, fart
            f.write("Folder Path: ")#.encode('utf-8')
            f.write('"' + rpath + ffolder + '"')
            #f.write(ffolder)
            f.write(ftags)
            f.close
    except Exception as e:
        print(e)

#Run the scanroot function to list all directories in root
if __name__ == '__main__':
    import sys
    rpath = sys.argv[1]
    if rpath.endswith('/'):
        print(rpath)
    else:
        rpath = (rpath + '/')
        print(rpath)
    musicscrape = [] #Create the ScraperList
    for entry in scanroot(sys.argv[1] if len(sys.argv) > 1 else '.'):
        #print(entry)
        musicscrape.append(entry) #Create the working list of artists
    print(musicscrape)

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
