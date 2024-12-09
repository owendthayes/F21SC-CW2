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
# - LINK UP FUNCTIONALITY BUTTONS
# - COMMAND LINE TESTING (CHECK SPEC)
# 
# - VIDEO
# - REPORT
# - COMMENT CODE
# - CHECK SPEC AGAIN FOR ANYTHING MISSING



##GUI FOR CHOOSING INPUT FILE
def gui_load_file():
    root = Tk()
    
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

    btn_choose_file = Button(root, text = "Load file", font = ("Arial", 14) ,fg= "black", command=lambda: clicked_load_file(txt_filePath.get(1.0, 'end-1c'), root))
    btn_choose_file.grid(row=1, column=2, sticky = 'w')

    root.mainloop()

##FUNCTION FOR LOADING FILE FROM INPUTTED FILE PATH
def clicked_load_file(filePath, root):
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
    root = Tk()
    ##decide a document to do operations

    states = {"country": False, "continent": False, "views_verbose": False, "views_short": False, "reader": False}

    root.title("F20SC-CW2 Data Analysis Tracker")
    root.geometry('900x600')

    ##grid for managing placement of widgets
    root.columnconfigure(0, weight = 1)
    root.columnconfigure(1, weight = 1, uniform = 'column')
    root.columnconfigure(2, weight = 1)
    root.columnconfigure(3, weight = 1)
    root.columnconfigure(4, weight = 1)
    
    root.rowconfigure(0, weight = 1)
    root.rowconfigure(1, weight = 1)
    root.rowconfigure(2, weight = 1)  

        
    #HIDES AND SHOWS BUTTONS ALLOWING FOR GRID TO BE CREATED AVOIDING FORMATTING ISSUES
    def button_hide():
        btn_view_document_continent.grid_remove()
        btn_view_document_country.grid_remove()
        btn_views_by_browser_verbose.grid_remove()
        btn_views_by_browser_short.grid_remove()
        btn_reader_profile.grid_remove()
        btn_back_to_load.grid_remove()
        btn_back_to_main.grid()

    def button_show():
        btn_choose_doc.grid()
        txt_doc.grid()

    
    #Helper method to flip the value of the associated key in the states dictionary
    def toggle_flag(flag):
        states[flag] = True

    #THESE NEED TESTED, PROBABLY NOT WORKING?
    def back_to_main():
        txt_doc.delete(1.0, END)

        for widget in root.grid_slaves():
           widget.grid_remove()

        btn_view_document_continent.grid()
        btn_view_document_country.grid()
        btn_views_by_browser_verbose.grid()
        btn_views_by_browser_short.grid()
        btn_reader_profile.grid()
        btn_back_to_load.grid()

        for x in states:
            states[x] = False

    def back_to_load(root):
        root.withdraw() 
        gui_load_file() 

    ##BUTTONS TO BE USED FOR STUFF
    btn_view_document_country = Button(root, text = "Search visitors\nby country", font = ("Arial", 14), height =5,fg= "red", command=lambda: (button_hide(), button_show(), toggle_flag("country"))) 
    btn_view_document_country.grid(row=2, column=0)
    
    btn_view_document_continent = Button(root, text = "Search document\nvisitors by\ncontinent", font = ("Arial", 14), height =5 ,fg= "red", command=lambda: (button_hide(), button_show(), toggle_flag("continent")))
    btn_view_document_continent.grid(row=2,column=1)

    btn_views_by_browser_verbose = Button(root, text = "Search document\nviews by browser\n(long)", font = ("Arial", 14), height =5 ,fg= "red", command=lambda:(button_hide(), create_bar_chart((views_by_browser_verbose(), "", "Views by Browser (Verbose)", "Browser", "Freq"), root)))
    btn_views_by_browser_verbose.grid(row=2, column=2)

    btn_views_by_browser_short = Button(root, text = "Search document\nviews by browser\n(short)", font = ("Arial", 14), height =5 ,fg= "red", command=lambda: (button_hide(), create_bar_chart((views_by_browser_short(), "", "Views by Browser (Short)", "Browser", "Freq"), root)))
    btn_views_by_browser_short.grid(row=2, column=3)                                                                                                            

    btn_reader_profile = Button(root, text = "Top Viewers", font = ("Arial", 14) ,fg= "red", height =5, command=lambda: (button_hide(), toggle_flag("reader")))
    btn_reader_profile.grid(row=2, column=4)   

    txt_doc = Text(root, font = ("Arial", 14) ,fg= "black", height = 1, width = 20)
    txt_doc.grid(row=0, column=0, sticky = 'nw', columnspan=5)
    txt_doc.grid_remove()

    #he is the fixer, he fixes things
    def the_fixer():
        if (states.get("country") == True):
            freq = search_country(txt_doc.get(1.0, END).strip())
            print(freq)
            title = "Document viewed per country"
            x = "country"
            y = "freq"

        elif (states.get("continent") == True):
            freq = search_continent(txt_doc.get(1.0, END).strip())
            title = "Document viewed per continent"
            x = "continent"
            y = "freq"

        elif (states.get("views_verbose") == True):
            freq = views_by_browser_verbose()
            title = "Views by Browser (Verbose)"
            x = "browser"
            y = "views"
            create_bar_chart((freq, '', title, x, y), root)

        elif (states.get("views_short") == True):
            freq = views_by_browser_short()
            title = "Views by browser (Short)"
            x = "browser"
            y = "views"
            create_bar_chart((freq, "", title, x, y), root)

        elif (states.get("reader") == True):
            freq = reader_profile(txt_doc.get(1.0, END).strip())
            title = "Top Viewers"
            x = "User"
            y = "Time spent"

        else:
            print("WARNING: SOMETHING HAS GONE HORRIBLY WRONG")

        return freq ,txt_doc.get(1.0, END).strip() ,title, x, y
    
    btn_choose_doc = Button(root, text = "choose document", font = ("Arial", 14) ,fg= "red", command=lambda:create_bar_chart(the_fixer(), root), padx=20)
    btn_choose_doc.grid(row=0, column=1, columnspan=5, sticky='n')
    btn_choose_doc.grid_remove()

    btn_back_to_main = Button(root, text = "back", font = ("Arial", 14) ,fg= "red", command=lambda:back_to_main(), width=10, height=1)
    btn_back_to_main.grid(row=2, column=0, sticky='sw', columnspan=5)
    btn_back_to_main.grid_remove()

    btn_back_to_load = Button(root, text = "back to file selection", font = ("Arial", 14) ,fg= "red", command=lambda:back_to_load(root), width=10, height=1)
    btn_back_to_load.grid(row=2, column=0, sticky='sw')

    ##Creating bar charts
    def create_bar_chart(parameters, root):
        freq, searched, title, x, y = parameters
        fig = Figure(figsize=(root.winfo_screenwidth(),7), dpi= 80)
        ax = fig.add_subplot(111)

        ax.bar(freq.index, freq.values, color='skyblue')
        ax.set_title(f"{title}: {searched}")
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.tick_params(axis='x', rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=1, column=2)
        
    root.mainloop()





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
#helper functions
def users_from_doc(documentID):
    #get list of users that have read the given document
    users_viewed = []
    for obj in data:
        if obj.get("env_doc_id") is documentID:
            users_viewed.append(obj.get("visitor_uuid"))
    return users_viewed
            
def docs_from_users(visitorID):
    #get list of documents that user has read
    documents_viewed = []
    for obj in data:
        if obj.get("visitor_uuid") is visitorID:
            documents_viewed.append(obj.get("env_doc_id"))
    return documents_viewed

#actual function
#what the fuck is a parameter sorting fucktion sakjdpakisdjmdsgsdaf
def also_like(documentID, visitorID, key):
    #get list of "Liked documents"
    users = users_from_doc(documentID)

    liked_docs = []
    
    all_read_docs = []
    for user in users:
        all_read_docs.append(docs_from_users(user))
    
    # doc_counts = Counter(all_read_docs)  # Count the occurrences of each document
    # sorted_docs = sorted(doc_counts.items(), key=lambda x: x[1], reverse=True)  # Sort by count in descending order
    
    # Optional: Extract only the document IDs, ignoring the counts
    # sorted_doc_ids = [doc for doc, count in sorted_docs]

    return liked_docs
    
    

def sorting_function():
    print("kys")


gui_load_file()
