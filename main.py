import json
import tkinter
import pandas as pd
import re
from pycountry_convert import country_alpha2_to_continent_code, convert_continent_code_to_continent_name


FILE_NAME = 'test.json'

#reading in data
with open(FILE_NAME, 'r') as file:
    lines = [line.strip() for line in file if line.strip()]
fixed_json = "[\n" + ",\n".join(lines) + "\n]"
with open('fixed_file.json', 'w') as file:
    file.write(fixed_json)
with open('fixed_file.json', 'r') as file:
    data = json.load(file)

def search_country(document):# "subject_doc_id"
    #creates list of all countries which have viewed the document
    countries = [obj.get("visitor_country") for obj in data if (obj.get("subject_doc_id") == document)] 
    search_continent(countries) #calls search continent method
    print(pd.Series(countries).value_counts()) #DEBUGGING
    return pd.Series(countries).value_counts() #returns a tallied up version of the list showing the country and frequency of visitors

def search_continent(countries):
    #creates list of all continents included in the list of user countries
    continents = [convert_continent_code_to_continent_name(country_alpha2_to_continent_code(country)) for country in countries]
    print(pd.Series(continents).value_counts()) #DEBUGGING
    return pd.Series(continents).value_counts() #returns a tallied up version of the list showing the continents and frequency of visitors

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

def reader_profile():
    users = [user.get("visitor_uuid") for user in data] 
    print(pd.Series(users).value_counts()) #DEBUGGING
    return pd.Series(users).value_counts()


search_country("140228202800-6ef39a241f35301a9a42cd0ed21e5fb0")
views_by_browser()
reader_profile()