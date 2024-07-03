#!/usr/bin/env python

import os, requests, sys
from bs4 import BeautifulSoup
from PIL import Image
from urllib.request import urlopen
import uuid
import ssl

#change working directory to this folder 
path = os.getcwd()

#img classes
imageClass = r"js-lazy e2e-site-project-module-image"
imageGridClass = r"grid__item-image js-grid__item-image grid__item-image-lazy js-lazy"

#grabs url argument from command-line 
url = sys.argv[1]

#retreive website
while True:
    try:
        response = requests.get(url, verify=False) #disable SSL certificate validation temporarily
    except Exception:        
        print("Invalid site. Enter site:")
        url = input()
    else:
        break

#prompt for directory name, create directory
print("Enter a folder to your files in:")
folderName = input()
path = os.path.join(path, folderName)


try:    
    os.mkdir(path)
except:
    print("Folder already exists. Try again.")
    exit()

os.chdir(path)

#create a folder called HTML to save the HTML file in. We'll go back up a level once its saved
htmlFolder = os.path.join(path, "HTML")
os.mkdir(htmlFolder)
os.chdir(htmlFolder)      
       
with open(folderName.lower().replace(" ","-") + ".html", "wb") as html:
    html.write(response.content)
    
os.chdir(path)

#parse to soup
soup = BeautifulSoup(response.text, "html.parser")

#disable SSL certificate validation temporarily
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def saveImage(link):
    imgFile = Image.open(urlopen(link, context=ctx))
    if ".gif" not in link:
        imgFile.save("img_" + str(uuid.uuid4()) +".png", "PNG")
    else: 
        with open("animated-img_" + str(uuid.uuid4()) +".gif", "wb") as gif:
            gif.write(requests.get(link).content)


#create method that finds image tag and strips to image link
def findImages(soup, tag):
    imageTag = soup.find_all("img", tag)
    #get data-srcset; this creates a list of strings
    for tag in imageTag:
        source = tag.get("data-srcset") #find the image tag with this attribute
        source = source.split()
#        print("Here is the tag: ")
#        print(source)
        source = source[len(source)-2]  #get the second to last item in the string list
        link = source.split(",") #remove the part of the string with the image size, seperated by a comma
        link = link[(len(link)-1)] #get the last item aka the link to the image
        print("Downloading: " + link)
        saveImage(link)
        
#find and download video
def findVideos(soup):
    p = path
    videoFolder = os.path.join(p, "Videos")
    os.mkdir(videoFolder)
    os.chdir(videoFolder)
    videoTag = soup.find_all("iframe")
    for tag in videoTag:
        source = tag.get("src")
        response = requests.get(source)
        #we need to parse the source link
        #find video tag, with type = 'video/mp4'
        videoSoup = BeautifulSoup(response.text, "html.parser")
        videoLink = videoSoup.find("video")
        
        print(videoLink)
        


#findImages(soup, imageClass) #for stand alone imamages
#findImages(soup, imageGridClass) #for images in a grid format
findVideos(soup)
print("Finished downloading.")

