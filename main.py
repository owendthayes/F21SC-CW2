import json
import tkinter
import pandas as pd
import re
#from pycountry_convert import country_alpha2_to_continent_code, convert_continent_code_to_continent_name


FILE_NAME = 'test.json'

#reading in data
with open(FILE_NAME, 'r') as file:
    data = json.load(file)

def search_country(document):
    # "subject_doc_id"
    countries = [obj.get("visitor_country") for obj in data if (obj.get("subject_doc_id") == document)]
    search_continent(countries)
    print(pd.Series(countries).value_counts()) #DEBUGGING
    return pd.Series(countries).value_counts()

def search_continent(countries):
    return

def views_by_browser():
    browsers = []

    #populating all browsers into list
    for obj in data:
        browserName = obj.get("visitor_useragent").split('/')
        browsers.append(browserName[0])

    #totalling number of users on each browser
    freq = pd.Series(browsers).value_counts()

    #returning most popular browser
    print(freq) #DEBUGGING
    return freq


search_country("140228202800-6ef39a241f35301a9a42cd0ed21e5fb0")
views_by_browser()
