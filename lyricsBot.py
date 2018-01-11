"""
azLyricsBot v 2.0
Started July 17th, 2017 at 12:04:25 AM


Author: Spencer "Tiberius" Hommel

    The application is going to ask you for an author and song name.
Using the magic of computers, it will return the lyrics (hypothetically 
of course.)
    
    It will work by going to the page under the first letter of the artist, 
then find the name of the artist, then the name of the song.

Update log:
    azLyricsBot v 2.0 --> Monday, July 17th, 2017. 3:23:10 PM.
    + Added the support for the artists beginning with a number
    - Working on a workaround for the Kyle/iSpy case where the first letter
        of songname is not capitalized. 
        
"""

#defining function to output message if the lyrics are not found
def noFind(song, artist):
    print(song.title() + " by " + artist.title() + " could not be found. " +
          "Make sure that the artist and song names are correct.")

#importing BeautifulSoup, used for analyzing the html code
from bs4 import BeautifulSoup as bs

#importing package allowing me to open url 
import urllib.request

#importing sys.exit to execute script when exceptions occur
from sys import exit

#asking the user to input name of artist
artIn = input("Name of artist:    ")
artFormat = artIn.title().split()

#asking user to input name of song
sngIn  = input("Name of song:      ")
sngFormat = sngIn.title()

#if the first word of the artist is "The"
#bring it to the back and add a comma
#ex: The Rolling Stones ---> Rolling Stones, The
if artFormat[0] == "The":
    artOriginal = artIn
    
    #then combine back into string
    temp =  " ".join(artFormat[1:])
    artFormat = temp + ", " + artFormat[0]

#else, just combine back into string
else:
    artFormat = " ".join(artFormat)

#obtaining first letter of the artist's name
firstLetter = artFormat[0][0].lower()

#the base url that all the necessary extensions will be added-on to
urlBase = "http://www.azlyrics.com/"

#try loop to prevent crashes while looking for artist
try:
    #reads the html code at the given url (link to letter page on website)
    if not firstLetter.isnumeric():
        soupLet = bs(urllib.request.urlopen(urlBase + firstLetter + ".html")
                .read(), "lxml")
    else:
    #if the first letter is a number, it goes to the number page 
    #which is ..../19.html
        soupLet = bs(urllib.request.urlopen(urlBase + "19" + ".html")
                .read(), "lxml")
        
    #reads the html code at the given url (link to letter page on website)
    
    #searches the html code for the artist's name formatted as artFormat
    #returns portion of href link associated with the artist's name
    urlAddOnArt = soupLet.find("a", text = artFormat, href = True)["href"]
    
    #adds the url onto the bse URL ready to pass onto next block
    url = urlBase + urlAddOnArt

#if the above fails, points to error finding artist   
except:
    noFind(sngIn, artIn)
    exit("Error finding the artist")

 
#try loop to prevent crashes while looking for song

try:
    #reads the html code at the given url (link to artist's page on website)
    soupArt = bs(urllib.request.urlopen(url).read(), "lxml")
    
    #searches the html code for the song name formatted as sngFormat
    #returns portion of href link associated with the song name
    urlAddOnSng = soupArt.find("a", text = sngFormat, href = True)["href"]
    
    #adds the url onto the bse URL ready to pass onto next block
    #splice the song add-on because of a "../" in front of href link 
    url = urlBase + urlAddOnSng[3:]
    
#if the above fails, points to error finding song   
except:
    noFind(sngIn, artIn)
    exit("Error finding the song")

try:  
    #acceses the html code on the song's page on the website
    soupSong = bs(urllib.request.urlopen(url).read(), "lxml")
    
    #creates a list of <div> class elements (in which the lyrics are in)
    htmlText = str(soupSong.find_all("div", text = False))
    
    #the lyrics are sandwiched inbetween two constant comments in the html
    #in order to extract the lyrics, we find the indeces of each comment
    index1   = htmlText.find("that. -->")
    index2   = htmlText.find("<!-- MxM ")
    
    #splice the string so it's only the text (lyrics) between comments
    lyrics = (htmlText[index1+10:index2-18])
    
    #replacing all the html tags with blank spaces. 
    #thus, only the lyrics are left
    lyrics = lyrics.replace("<br/>", "")
    lyrics = lyrics.replace("<i>", "")
    lyrics = lyrics.replace("</i>", "")
    
    #formatting and printing the final lyrics with artist & song name
    print("\n" * 5)
    print(sngIn.title() + " by " + artIn.title())
    print(lyrics)
    
#if the above fails, points to error finding song      
except:
    noFind(sngIn, artIn)
    exit("Error extracting the lyrics")