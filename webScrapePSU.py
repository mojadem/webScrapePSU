import requests
from bs4 import BeautifulSoup
import json

# url we will be scraping
URL = "https://en.wikipedia.org/wiki/Pennsylvania_State_University"

# getting the html fromm the url
response = requests.get(URL)

# creating a beautiful soup object with the html
soup = BeautifulSoup(response.content, 'html.parser')

# the table we will be scraping
table = soup.find('table', class_='infobox vcard')

# the data of the table will be stored in a dictionary
data = {}

# want to exclude 'sup' tags from our data
tag_exclude = 'sup'

# loop through rows of table
for tr in table.find_all('tr'):
    # will only save data from rows with a header
    if tr.find('th'):
        # looks for excluded tag to remove
        if tr.find(tag_exclude):
            tr.find(tag_exclude).decompose()
        
        # stores text of th
        th_text = tr.find('th').get_text()

        # if there is a list, will store the td in a list
        if tr.find('ul'):
            td_list = []
            for li in tr.find_all('li'):
                td_list.append(li.get_text())
            
            data[th_text] = td_list
        
        # otherwise, will just be text
        else: 
            td_text = tr.find('td').get_text()

            data[th_text] = td_text

        # only scraping until the 'website' column
        if tr.find('th').get_text() == 'Website':
            break

# non al-num characters allowed for cleaning
allowedChars = '();:$,.-/ '

# cleaning out the data
for key in data:
    # will loop over data if it is not a string
    if not isinstance(data[key], str): 
        continue
    
    # stores the data as a string
    text = data[key]
    # the new string we will be building
    newText = ''
    for char in text:
        # will not include chars that are not alnum or not allowed
        if char.isalnum() or char in allowedChars:
            # builds new string character by character
            newText += char
    
    # updates the current data
    data[key] = newText

# writes data to json file
with open('webScrapePSU.json', 'w') as jsonFile:
    json.dump(data, jsonFile)