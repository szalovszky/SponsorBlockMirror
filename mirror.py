### Import required libraries ###
import requests
import os
from datetime import datetime
import time

### Variables ###
dataPath = "./mirror"

instance = "https://sponsor.ajay.app"
databasePath = "/database.json"

### Create directory structure ###
if not os.path.exists(dataPath):
    print("Creating data directory: " + dataPath)
    os.mkdir(dataPath)

### Action ###
# Request up-to-date database URLs
response = requests.get(instance + databasePath)
failed = False
links = list()
if(response.status_code == 200):
    # If successfully connected, parse it as a JSON and save the link values to a variable
    links = response.json()['links']
else:
    # Connection failed for some reason.
    failed = True
    print("Request failed.")
response.close()
# If it didn't fail, download the database
if not failed:
    for link in links:
        start = time.time()
        # Download each parsed data file.
        url = instance + link['url']
        print("Began downloading: " + url)
        dataFile = requests.get(url)
        end = time.time()
        timeElapsed = "%.2f" % (end - start)
        if dataFile.status_code == 200:
            print("Finished downloading in " + str(timeElapsed) + " seconds.\nWriting to file: " + dataPath + "/" + os.path.split(url)[1])
            with open(dataPath + "/" + os.path.split(url)[1], "w", encoding="utf-8") as outputFile:
                outputFile.write(dataFile.text)
            print("File written.")
        else:
            print("Request failed in " + str(timeElapsed) + " seconds for " + url)
        response.close()