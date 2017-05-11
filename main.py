from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3

import json
import requests


links = []


driver = webdriver.Chrome() # Intended for Chrome browser.

driver.get("https://www.youtube.com/user/caseyneistat/videos") # Load a specific web page in the current browser window.

buttonXpath = '//*[@id="browse-items-primary"]/li[2]/button' # xPath string variable.

loginButtonElement = driver.find_element_by_xpath(buttonXpath) # Finds first matching element, takes xPath as parameter.

driver.execute_script("window.scrollTo(0,1080)") # Scroll downward to display and be able to access necessary element.

loginButtonElement.click()

WebDriverWait(driver, 5)

page = requests.get("https://www.youtube.com/user/caseyneistat/videos") # Create a reponse object with all our data.

soup = BeautifulSoup(page.content, 'html.parser') # Parse the HTML data.

html = list(soup.children)[2] # Naivagate the soup with lots of indexing.

body = list(html.children)[2]

bodyContainer = list(body.children)[3]

pageContainer = list(bodyContainer.children)[4]

page = list(pageContainer.children)[0]

container = list(page.children)[4]

containerOutter = list(container.children)[1]

colContainer = list(containerOutter.children)[3]

containerInner = list(colContainer.children)[1]

primaryCol = list(containerInner.children)[1]

ytCard = list(primaryCol.children)[1]

primaryColContent = list(ytCard.children)[1]

uiList = list(primaryColContent.children)[1]

contentGrid = list(uiList.children)[5]

gridItem = list(contentGrid.children)[1]

numberOfVideos = 31 # This is an artbitary numbers which represents the number of thumbnails parsed.


for i in range(1, numberOfVideos):
    # With the way the HTML is structured, alternating containers used for white-space must be accounting for when retreiving the right tags.
    if i % 2 != 0:
        video = list(gridItem.children)[i]

        vvCheck = list(video.children)[1]

        dismissable = list(vvCheck.children)[1]

        thumbNail = list(dismissable.children)[1]

        href = list(thumbNail.children)[1]

        spanOutter = list(href.children)[0]

        spanMiddle = list(spanOutter.children)[1]

        spanInner = list(spanMiddle.children)[1]

        img = list(spanInner.children)[1]

        link = list(img.children)[1]['src']

        links.append(link)


# Address URL string that directs to the video thumbnail image.
thumbnailLink = links[14]

visual_recognition = VisualRecognitionV3('2016-05-20', api_key='d20eab949ea4ff544ff3ffe27cd6858a5ee25e52')

dictOutput = visual_recognition.classify(images_url=thumbnailLink)

# Display the characteristics of the image contents.
for r in dictOutput["images"]:
    for i in range(0, len(r["classifiers"][0]["classes"])):
        print(r["classifiers"][0]["classes"][i]["class"])

