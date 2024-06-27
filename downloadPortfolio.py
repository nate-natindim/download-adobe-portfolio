import os, requests, sys
from bs4 import BeautifulSoup
from PIL import Image
from urllib.request import urlopen
import uuid

#enter a url and the script will download the images from that site
#change working directory
path = r"C:\Users\nnati\OneDrive\Desktop\Portfolio"
os.chdir(path)
currentFolder = os.getcwd()


#img classes
imageClass = r"js-lazy e2e-site-project-module-image"
imageGridClass = r"grid__item-image js-grid__item-image grid__item-image-lazy js-lazy"

#grabs url argument from command-line 
url = sys.argv[1]

#prompt for directory name, create directory
print("Enter a name for your folder:")
folderName = input()
path = os.path.join(path, folderName)

try:    
    os.mkdir(path)
except:
    print("Folder already exists. Try again.")
    exit()

#get website
while True:
    try:
        response = requests.get(url)
    except:
        print("Invalid site. Enter site:")
        url = input()
    else:
        break
        
#download HTML and save in folder
with open(folderName.lower().replace(" ","-") + ".html", "wb") as html:
    html.write(response.content)
    
print("Success!")
#parse to soup
soup = BeautifulSoup(response.text, "html.parser")

def saveImage(link):
    p = path
    imgFile = Image.open(urlopen(link))
    if ".gif" not in link:
        imgFile.save(p + r"\img_" + str(uuid.uuid4()) +".png", "PNG")
    else: 
        with open(p + r"\animated-img_" + str(uuid.uuid4()) +".gif", "wb") as f:
            f.write(requests.get(link).content)


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
        link = source.split(",") #splits into a list of two
        link = link[(len(link)-1)] #get the last item aka the link to the image
        print("Downloading: " + link)
        saveImage(link)


#print("Images not in a grid:")
findImages(soup, imageClass)
#print("Images in a grid:")
findImages(soup, imageGridClass)   
print("End.")