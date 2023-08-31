'''
Created on Nov 19, 2016

@author: Darryl Yan and Jerry Pan
'''
import urllib, re
from bs4 import BeautifulSoup

"""Class that contains a string element, url,
and an integer, canRecycle that describes
a url property

@param url: An image url in string format
@param canRecycle: A binary number, 0 representing recyclable
and 1 representing non-recyclable
"""

class Disposable:
    'Contains image URL and binary classification of recyclable'

    def __init__(self, url, canRecycle):
        self.url, self.canRecycle = url, canRecycle

    def getUrl(self):
        return self.url

    def getRecycle(self):
        return self.canRecycle

"""Returns a URL for a Flickr image
search

@param str: String to be inputted into image search
"""

def getImageSearchUrl(word):
    strList, outputString, outputString = word.split(" "), "https://www.flickr.com/search/?text=", outputString + strList[0]
    for i in range(1, len(strList), 1):  # Concat separator between every word
        outputString += "%20" + strList[i]
    return outputString


"""Returns a list of strings representing image URL's

@param url: String representing the URL of a single image
"""

def urlProcess(url):
    r, soup, result = urllib.urlopen(url).read(), BeautifulSoup(r, "html.parser"), re.findall("img.src='//(.*)';", soup.prettify())
    return result


def main():
    trashList, recycleList = ["plastic bag", "pizza box", "battery", "lightbulb",  # Create lists of recyclables and trash objects
                 "plastic cup", "styrofoam", "napkins", "ceramic",
                 "styrofoam cups", "paper towels", "SOLO cup"], ["plastic bottle", "aluminum can", "cardboard box",
                   "glass bottle", "newspaper", "printer paper",
                   "laundry detergent", "books", "envelope",
                   "corrugated cardboard", "shredded paper",
                   "mirror shards"]
    disposableList, returnList = trashList + recycleList, []                          # Concatenate lists to iterate through all objects
    for object in disposableList:
        """For each object query, generate a Disposable
        object that contains image URL and recycle status
        """
        searchUrl, imageList = getImageSearchUrl(object), urlProcess(searchUrl)
        for imageUrl in imageList:
            canRecycle = 0
            if object in recycleList:
                canRecycle = 1
            newObject = Disposable(imageUrl, canRecycle)
            returnList.append(newObject)

    return returnList
