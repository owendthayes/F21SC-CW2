import json
from tkinter import * 
import pandas as pd
import re
import pycountry
from pycountry_convert import country_alpha2_to_continent_code, convert_continent_code_to_continent_name
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# TO DO LIST
# - REQUIREMENT 5 (ALSO LIKES)
# - REQUIREMENT 6 (ALSO LIKES GRAPH)
# - GET RID OF HARD CODED SHIT
# - COMMAND LINE TESTING (CHECK SPEC)
# - IDK WE GOTTA CHECK THE SPEC MAKE SURE WE GOT IT COVERED
# - VIDEO
# - REPORT
# - COMMENT CODE

root = Tk()

##GUI FOR CHOOSING INPUT FILE
def gui_load_file():
    root.title("F20SC-CW2 Data Analysis Tracker")
    root.geometry('900x600')

    ##grid for managing placement of widgets
    root.columnconfigure(0, weight = 1)
    root.columnconfigure(1, weight = 1)
    root.columnconfigure(2, weight = 1)

    root.rowconfigure(0, weight = 1)
    root.rowconfigure(1, weight = 1)
    root.rowconfigure(2, weight = 1)   

    ##elements of main page
    lbl_load_file = Label(root, font = ("Arial", 14) ,fg= "black", height = 1, width = 30, text="enter file path")
    lbl_load_file.grid(row=0, column=1, sticky = 's')

    txt_filePath = Text(root, font = ("Arial", 14) ,fg= "black", height = 1, width = 30   )
    txt_filePath.grid(row=1, column=1,)

    btn_choose_file = Button(root, text = "Load file", font = ("Arial", 14) ,fg= "black", command=lambda: clicked_load_file(txt_filePath.get(1.0, 'end-1c')))
    btn_choose_file.grid(row=1, column=2, sticky = 'w')

    root.mainloop()

##FUNCTION FOR LOADING FILE FROM INPUTTED FILE PATH
def clicked_load_file(filePath):
    global data    ##this is the parsed json data

    FILE_NAME = filePath.strip()
    print("Processing file: {FILE_NAME}")
    try:     
        #reading in data
        with open(FILE_NAME, 'r') as file:
            unparsed_data = file.read()
        
        json_objects = unparsed_data.strip().split("\n")
        data = [json.loads(obj) for obj in json_objects]

        for obj in data:
            print(obj.get("visitor_uuid"))

        print("File loaded Successfully")

    except FileNotFoundError:
        print(f"File not found: {FILE_NAME}")
        lbl_error_msg = Label(root, font = ("Arial", 14) ,fg= "red", text="File can't be found, check you have entered the file path correctly.")
        lbl_error_msg.grid(row=2, column=1, sticky = 'n')

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        lbl_error_msg = Label(root, font = ("Arial", 14) ,fg= "red", text="Invalid JSON data. Please check your file and try again.")
        lbl_error_msg.grid(row=2, column=1, sticky = 'n')

    except OSError as e:
        print(f"OS Error: {e}")
        lbl_error_msg = Label(root, font = ("Arial", 14) ,fg= "red", text="An unknown error has occured.")
        lbl_error_msg.grid(row=2, column=1, sticky = 'n')

    else:
        root.withdraw()
        gui_main()
        
def gui_main():
    global root
    root = Tk()

    ##decide a document to do operations

    root.title("F20SC-CW2 Data Analysis Tracker")
    root.geometry('900x600')

    ##grid for managing placement of widgets
    root.columnconfigure(0, weight = 1)
    root.columnconfigure(1, weight = 1)
    root.columnconfigure(2, weight = 1)
    root.columnconfigure(3, weight = 1)
    root.columnconfigure(4, weight = 1)
    
    root.rowconfigure(0, weight = 1)
    root.rowconfigure(1, weight = 1)
    root.rowconfigure(2, weight = 1)  
     
    ##BUTTON FUNCTIONS, NEED CHANGED LATER TO NOT BE HARD CODED
    def clicked_search_doc_country():
        create_bar_chart(search_country("140228202800-6ef39a241f35301a9a42cd0ed21e5fb0"), "140228202800-6ef39a241f35301a9a42cd0ed21e5fb0", "Visitor frequency from each country for document","Country", "Frequency")
 
    def clicked_search_doc_continent():
        create_bar_chart(search_continent("140228202800-6ef39a241f35301a9a42cd0ed21e5fb0"), "140228202800-6ef39a241f35301a9a42cd0ed21e5fb0", "Visitor frequency from each continent for document","Country", "Frequency")

    def clicked_views_by_browser_verbose():
        create_bar_chart(views_by_browser_verbose(""))

    def clicked_views_by_browser_short():
        create_bar_chart(views_by_browser_short(""))

    ##BUTTONS TO BE USED FOR STUFF
    btn_view_document_country = Button(root, text = "Search visitors by country", font = ("Arial", 14) ,fg= "red", command=clicked_search_doc_country)
    btn_view_document_country.grid(row=3, column=0)
    
    btn_view_document_continent = Button(root, text = "Search document visitors by continent", font = ("Arial", 14) ,fg= "red", command=clicked_search_doc_continent)
    btn_view_document_continent.grid(row=3,column=1)

    btn3 = Button(root, text = "Hit me", font = ("Arial", 14) ,fg= "red", command=clicked_views_by_browser_verbose)
    btn3.grid(row=3, column=2)

    btn4 = Button(root, text = "Hit me", font = ("Arial", 14) ,fg= "red", command=clicked_views_by_browser_short)
    btn4.grid(row=3, column=3)

    btn5 = Button(root, text = "Hit me", font = ("Arial", 14) ,fg= "red", command=clicked_search_doc_country)
    btn5.grid(row=3, column=4)   

    root.mainloop()

##CHARTS ARENT DISPLAYING IDK WHY
def create_bar_chart(freq, searched, title, x, y):
    fig = Figure(figsize=(10,10), dpi= 80)
    ax = fig.add_subplot(111)

    ax.bar(freq.index, freq.values, color='skyblue')
    ax.set_title(f"{title}: {searched}")
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.tick_params(axis='x', rotation=45)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=1, column=2)

## REQ 2
def search_country(document):# "subject_doc_id"
    #creates list of all countries which have viewed the document
    countries = [obj.get("visitor_country") for obj in data if (obj.get("subject_doc_id") == document)] 
    return pd.Series(countries).value_counts() #returns a tallied up version of the list showing the country and frequency of visitors

def search_continent(document):
    #creates list of all countries which have viewed the document
    countries = [obj.get("visitor_country") for obj in data if (obj.get("subject_doc_id") == document)]
    #creates list of all continents included in the list of user countries
    continents = [convert_continent_code_to_continent_name(country_alpha2_to_continent_code(country)) for country in countries]
    return pd.Series(continents).value_counts() #returns a tallied up version of the list showing the continents and frequency of visitors

##REQ 3 A e.g. entire useragent string
def views_by_browser_verbose():
    browsers = []

    #populating all browsers into list
    for obj in data:
        browsers.append(obj.get("visitor_useragent"))

    #totalling number of users on each browser
    freq = pd.Series(browsers).value_counts()

    #returning most popular browser
    print(browsers)
    print(freq) #DEBUGGING
    return freq

##REQ 3 B e.g. 'Mozilla'
def views_by_browser_short():
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

##REQ 5
def users_from_doc(document):
    ##get list of users that have read the given document
    ##DONT THINK (DOCUMENT) WILL WORK AS PARAMETER, CHANGE LATER.
    doc = json.load(document)
    readers = []
    for obj in document:    ## this probably will not work, gotta load file
        if obj.get("vistor_uuid") not in readers:
            visitorID = obj.get("visitor_uuid")
            readers.append(visitorID)
    return readers

def docs_from_users(visitorID):
    ##get list of documents that user has read
    documents = []


#search_continent("140228202800-6ef39a241f35301a9a42cd0ed21e5fb0")
#views_by_browser()
#reader_profile()

gui_load_file()