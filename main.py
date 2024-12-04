import json
from tkinter import * 
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

##GUI STUFF
def gui():
    root = Tk()
    root.title("F20SC-CW2 Data Analysis Tracker")
    root.geometry('700x500')

    lbl = Label(root, text = "test")
    lbl.pack(side = "top")

    def clicked():
        lbl.configure("oh god the pain")

    ##BUTTONS TO BE USED FOR STUFF
    bottom_frame = Frame(root) #creates frame area for the bottom row (used as button area)
    bottom_frame.pack(side="bottom", fill="x") #fills from the bottom left

    btn1 = Button(bottom_frame, text = "Hit me", font = ("Arial", 14) ,fg= "red", command=clicked)
    btn1.pack(side = "left")

    btn2 = Button(bottom_frame, text = "Hit me", font = ("Arial", 14) ,fg= "red", command=clicked)
    btn2.pack(side = "left")

    btn3 = Button(bottom_frame, text = "Hit me", font = ("Arial", 14) ,fg= "red", command=clicked)
    btn3.pack(side = "left")

    btn4 = Button(bottom_frame, text = "Hit me", font = ("Arial", 14) ,fg= "red", command=clicked)
    btn4.pack(side = "left")

    btn5 = Button(bottom_frame, text = "Hit me", font = ("Arial", 14) ,fg= "red", command=clicked)
    btn5.pack(side = "left")
    root.mainloop()



## REQ 2
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

##REQ 3
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

##REQ 4
def reader_profile():
    #creates list of all user ids found in the list allowing for duplicate entries
    users = [user.get("visitor_uuid") for user in data] 
    print(pd.Series(users).value_counts().head(10)) #DEBUGGING
    #returns users list tallied up with the frequency each user id has been found, will show the top 10 most seen users
    return pd.Series(users).value_counts().head(10)


search_country("140228202800-6ef39a241f35301a9a42cd0ed21e5fb0")
views_by_browser()
reader_profile()
gui()