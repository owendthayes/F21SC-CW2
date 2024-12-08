import json
from tkinter import * 
import pandas as pd
import re
import pycountry
from pycountry_convert import country_alpha2_to_continent_code, convert_continent_code_to_continent_name
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

##LOADING IN FILE AS A REUSABLE FUNCTION
# def loadFile(fileName):
#     FILE_NAME = fileName
#     print(FILE_NAME)
#     #reading in data
#     with open(FILE_NAME, 'r') as file:
#         lines = [line.strip() for line in file if line.strip()]
#     fixed_json = "[\n" + ",\n".join(lines) + "\n]"
#     with open('fixed_file.json', 'w') as file:
#         file.write(fixed_json)
#     with open('fixed_file.json', 'r') as file:
#         data = json.load(file)

root = Tk()

##GUI STUFF
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
    lbl_load_file = Label(root, font = ("Arial", 14) ,fg= "red", height = 1, width = 30, text="enter file path")
    lbl_load_file.grid(row=0, column=1, sticky = 's')

    txt_filePath = Text(root, font = ("Arial", 14) ,fg= "red", height = 1, width = 30)
    txt_filePath.grid(row=1, column=1,)

    btn_choose_file = Button(root, text = "Load file", font = ("Arial", 14) ,fg= "red", command=lambda: clicked_load_file(txt_filePath.get(1.0, 'end-1c')))
    
    btn_choose_file.grid(row=1, column=2, sticky = 'w')

    root.mainloop()

def clicked_load_file(filePath):
    ##try to load file
    FILE_NAME =  "\\" + filePath.strip()
    print("Processing file: {FILE_NAME}")

    try:     
        #reading in data
        with open(FILE_NAME, 'r') as file:
            ##lines = [line.strip() for line in file if line.strip()]
            data = json.load(file)
            print(data)
            return data

        # fixed_json = "[\n" + ",\n".join(lines) + "\n]"
        # with open('fixed_file.json', 'w') as file:
        #     file.write(fixed_json)
        # with open('fixed_file.json', 'r') as file:
        #     data = json.load(file)
        # print("File loaded successfully!")

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



    

##bar_chart_frame = Frame(root)
    # bar_chart_frame.pack(fill="x", expand=True)

    # ##BUTTONS TO BE USED FOR STUFF
    # bottom_frame = Frame(root) #creates frame area for the bottom row (used as button area)
    # bottom_frame.pack(side="bottom", fill="x") #fills from the bottom left

    # top_frame = Frame(root)
    # top_frame.pack(side =  "top", fill = "x")

    # top_frame = Frame(root) #creates frame area for the top row (used as text area)
    # top_frame.pack(side="top", fill="x") #fills from the top left

    # def clicked_search_doc_country():
    #     create_bar_chart(search_country("140228202800-6ef39a241f35301a9a42cd0ed21e5fb0"), "140228202800-6ef39a241f35301a9a42cd0ed21e5fb0", "Visitor frequency from each country for document","Country", "Frequency")

    # btn_view_document_country = Button(bottom_frame, text = "Hit me", font = ("Arial", 14) ,fg= "red", command=clicked_search_doc_country)
    # btn_view_document_country.pack(side = "left")
    
    # def clicked_search_doc_continent():
    #     create_bar_chart(search_continent("140228202800-6ef39a241f35301a9a42cd0ed21e5fb0"), "140228202800-6ef39a241f35301a9a42cd0ed21e5fb0", "Visitor frequency from each continent for document","Country", "Frequency")

    # btn_view_document_continent = Button(bottom_frame, text = "Hit me", font = ("Arial", 14) ,fg= "red", command=clicked_search_doc_continent)
    #     btn_view_document_continent.pack(side = "left")

    #     btn3 = Button(bottom_frame, text = "Hit me", font = ("Arial", 14) ,fg= "red", command=clicked_search_doc_country)
    #     btn3.pack(side = "left")

    #     btn4 = Button(bottom_frame, text = "Hit me", font = ("Arial", 14) ,fg= "red", command=clicked_search_doc_country)
    #     btn4.pack(side = "left")

    #     btn5 = Button(bottom_frame, text = "Hit me", font = ("Arial", 14) ,fg= "red", command=clicked_search_doc_country)
    #     btn5.pack(side = "left")

    
    # ##CHOOSING INPUT FILE
    # txtLoadFile = Text(top_frame, font = ("Arial", 14), fg = "blue", height = 1.4, width = 30)
    # txtLoadFile.pack(side = "left", anchor = "nw")

    # ##btnLoadFile = Button(top_frame, text = "select file", font = ("Arial", 14) ,fg= "blue", command=load_input_file)
    # ##btnLoadFile.pack(side = "left", anchor = "nw")

    # root.mainloop()

##MR DONNELLY, WE PROBABLY GONNA HAVE TO DO LOADFILE(FILENAME) WHEN WE RUN SHIT? MAYBE PASS IN AS A PARAMETER FOR EACH FUNCTION? IDK THIS IS SO CONFUSING
    # i reckon if we have a bit of the GUI that opens before the functionality
    # user inputs the file path of the file they wanna use then they can continue with the graphs and shit
    # then they can go back and do a different file if they want.
    # ill try add it but if it works you'll never see this message hehe


##ngl idk if this is needed, we might just need to do it in command line? im not rly sure
    # def load_input_file():
    #     try:
    #         FILE_NAME = "\\" + txtLoadFile.get("1.0", END)
    #         print(FILE_NAME)
    #         #reading in data
    #         with open(FILE_NAME, 'r') as file:
    #             lines = [line.strip() for line in file if line.strip()]
    #         fixed_json = "[\n" + ",\n".join(lines) + "\n]"
    #         with open('fixed_file.json', 'w') as file:
    #             file.write(fixed_json)
    #         with open('fixed_file.json', 'r') as file:
    #             data = json.load(file)
    #     except Exception as e:
    #         print(repr(e))


def create_bar_chart(freq, searched, title, x, y):
    loadFile("test.json")
    fig = Figure(figsize=(10,10), dpi= 100)
    ax = fig.add_subplot(111)

    ax.bar(freq.index, freq.values, color='skyblue')
    ax.set_title(f"{title}: {searched}")
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.tick_params(axis='x', rotation=45)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side="top", fill="both", expand=True)
    canvas.draw()


## REQ 2
def search_country(document):# "subject_doc_id"
    loadFile("test.json")
    #creates list of all countries which have viewed the document
    countries = [obj.get("visitor_country") for obj in data if (obj.get("subject_doc_id") == document)] 
    print(pd.Series(countries).value_counts()) #DEBUGGING
    return pd.Series(countries).value_counts() #returns a tallied up version of the list showing the country and frequency of visitors

def search_continent(document):
    loadFile("test.json")
    #creates list of all countries which have viewed the document
    countries = [obj.get("visitor_country") for obj in data if (obj.get("subject_doc_id") == document)]
    #creates list of all continents included in the list of user countries
    continents = [convert_continent_code_to_continent_name(country_alpha2_to_continent_code(country)) for country in countries]
    print(pd.Series(continents).value_counts()) #DEBUGGING
    return pd.Series(continents).value_counts() #returns a tallied up version of the list showing the continents and frequency of visitors

##REQ 3 A e.g. entire useragent string
def views_by_browser_verbose():
    loadFile("test.json")
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
    loadFile("test.json")
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
    loadFile("test.json")
    #creates list of all user ids found in the list allowing for duplicate entries
    users = [user.get("visitor_uuid") for user in data] 
    print(pd.Series(users).value_counts().head(10)) #DEBUGGING
    #returns users list tallied up with the frequency each user id has been found, will show the top 10 most seen users
    return pd.Series(users).value_counts().head(10)

##REQ 5
def users_from_doc(document):
    loadFile("test.json")
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
    loadFile("test.json")
    ##get list of documents that user has read
    documents = []


#search_continent("140228202800-6ef39a241f35301a9a42cd0ed21e5fb0")
#views_by_browser()
#reader_profile()

gui_load_file()
