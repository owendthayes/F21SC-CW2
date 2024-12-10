import json #for managing files https://docs.python.org/3/library/json.html
from tkinter import *  #for creating a gui https://docs.python.org/3/library/tkinter.html
import graphviz.dot
import pandas as pd #for data manipulation and managing big data https://pandas.pydata.org/
import pycountry #allows the ability to get country codes https://pypi.org/project/pycountry/
from pycountry_convert import country_alpha2_to_continent_code, convert_continent_code_to_continent_name #allows the ability to get country codes https://pypi.org/project/pycountry/
import matplotlib #for creating graphs https://matplotlib.org/
from matplotlib.figure import Figure #for creating graphs https://matplotlib.org/
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #for creating graphs https://matplotlib.org/
import graphviz
# TO DO LIST
# - LINK UP FUNCTIONALITY BUTTONS FOR REQ 5 AND 6
# - COMMAND LINE TESTING (CHECK SPEC)
# 
# - VIDEO
# - REPORT
#
# - COMMENT CODE
# - CHECK SPEC AGAIN FOR ANYTHING MISSING
# - doesnt close when u click x


##GUI FOR CHOOSING INPUT FILE
def gui_load_file():
    root = Tk()
    
    root.title("F20SC-CW2 Data Analysis Tracker")
    
    app_width = 700
    app_height = 300

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    
    root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    root.configure(bg="MediumPurple1")  

    ##grid for managing placement of widgets
    root.columnconfigure(0, weight = 1)
    root.columnconfigure(1, weight = 1)
    root.columnconfigure(2, weight = 1)

    root.rowconfigure(0, weight = 1)
    root.rowconfigure(1, weight = 1)
    root.rowconfigure(2, weight = 1)   

    ##elements of main page
    lbl_load_file = Label(root, font = ("Arial", 14, 'bold') ,fg= "white", bg="MediumPurple1", height = 1, width = 30, text="Please enter the file path")
    lbl_load_file.grid(row=0, column=1, sticky = 's')

    txt_filePath = Text(root, font = ("Arial", 14) ,fg= "black", height = 1, width = 30   )
    txt_filePath.grid(row=1, column=1,)

    btn_choose_file = Button(root, text = "Load file", font = ("Arial", 14) ,fg= "black", bg="lavender",command=lambda: clicked_load_file(txt_filePath.get(1.0, 'end-1c'), root))
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

        print("File loaded Successfully")

    except FileNotFoundError:
        print(f"File not found: {FILE_NAME}")
        lbl_error_msg = Label(root, font = ("Arial", 14) ,fg= "red", bg = "white", text="File can't be found, check you have entered the file path correctly.")
        lbl_error_msg.grid(row=2, column=1, sticky = 'n')

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        lbl_error_msg = Label(root, font = ("Arial", 14) ,fg= "red",bg = "white", text="Invalid JSON data. Please check your file and try again.")
        lbl_error_msg.grid(row=2, column=1, sticky = 'n')

    except OSError as e:
        print(f"OS Error: {e}")
        lbl_error_msg = Label(root, font = ("Arial", 14) ,fg= "red" ,bg = "white", text="An unknown error has occured.")
        lbl_error_msg.grid(row=2, column=1, sticky = 'nw')

    else:
        root.withdraw()
        gui_main()
        
def gui_main():
    root = Tk()
    #also_likes_graph("130705172251-3a2a725b2bbd5aa3f2af810acf0aeabb","745409913574d4c6")
    #also_like( "140206010823-b14c9d966be950314215c17923a04af7", "745409913574d4c6")
    
    states = {"country": False, "continent": False}

    root.title("F20SC-CW2 Data Analysis Tracker")

    app_width = 1200
    app_height = 700

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    
    root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

    root.configure(bg="MediumPurple1")

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
        btn_also_likes.grid_remove()
        btn_back_to_load.grid_remove()
        btn_back_to_main.grid()

    #Shows buttons to allow for user input
    def button_show():
        btn_choose_doc.grid()
        txt_doc.grid(row=0, column=0,sticky='nw')
 
    
    #Helper method to flip the value of the associated key in the states dictionary
    def toggle_flag(flag):
        states[flag] = True

    #naviagtes user back to main page allowing them to select a different button 
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
        btn_also_likes.grid()

        for x in states:
            states[x] = False

    #navigates user back to initial page allowing for them to select a different file
    def back_to_load(root):
        root.withdraw() 
        gui_load_file() 

    def prep_also_likes():
        button_hide()
        
        lbl_doc_id = Label(root, font = ("Arial", 14) ,fg= "white" ,bg = "MediumPurple1", text="Document ID:")
        lbl_doc_id.grid(row=0, column=0, sticky='se')
        txt_doc.grid(row=0, column=2, sticky = 'sw')

        lbl_user_id = Label(root, font = ("Arial", 14) ,fg= "white" ,bg = "MediumPurple1", text="User ID:")
        lbl_user_id.grid(row=1, column=0, sticky='e')
        txt_userID.grid(row=1, column=2, sticky = 'w')

        btn_also_likes_go.grid()

    ##BUTTONS TO BE USED FOR STUFF
    #allows user to search for a certain document
    btn_view_document_country = Button(root, bg = "lavender", text = "Search visitors\nby country", font = ("Arial", 14), width = 15, height =6,fg= "black", command=lambda: (button_hide(), button_show(), toggle_flag("country"))) 
    btn_view_document_country.grid(row=0, column=0)
    
    #allows user to search for a certain document
    btn_view_document_continent = Button(root, bg = "lavender", text = "Search document\nvisitors by\ncontinent", font = ("Arial", 14), width = 15, height =6 ,fg= "black", command=lambda: (button_hide(), button_show(), toggle_flag("continent")))
    btn_view_document_continent.grid(row=0,column=2)

    #Generates graph displaying what browsers have been used to view documents in the file (verbose)
    btn_views_by_browser_verbose = Button(root, bg = "lavender", text = "Search document\nviews by browser\n(long)", font = ("Arial", 14), width = 15,  height =6 ,fg= "black", command=lambda:(button_hide(), create_bar_chart((views_by_browser_verbose(), "", "Views by Browser (Verbose)", "Browser", "Freq"), root)))
    btn_views_by_browser_verbose.grid(row=0, column=4)

    #Generates graph displaying what browsers have been used to view documents in the file (short)
    btn_views_by_browser_short = Button(root, bg = "lavender",text = "Search document\nviews by browser\n(short)", font = ("Arial", 14), width = 15, height =6 ,fg= "black", command=lambda: (button_hide(), create_bar_chart((views_by_browser_short(), "", "Views by Browser (Short)", "Browser", "Freq"), root)))
    btn_views_by_browser_short.grid(row=1, column=0)                                                                                                            

    #Generates graph displaying the top 10 Users (ranked by most time spent reading ('event_readtime'))
    btn_reader_profile = Button(root, bg="lavender", text = "Top Viewers", font = ("Arial", 14) ,fg= "black", height =6, width = 15, command=lambda: (button_hide(), create_bar_chart((reader_profile(), "", "Top Readers", "UUID", "Time spent"), root)))
    btn_reader_profile.grid(row=1, column=2)   

    #Generates graph displaying the top 10 Users (ranked by most time spent reading ('event_readtime'))
    btn_also_likes = Button(root, bg="lavender", text = "Also likes", font = ("Arial", 14) ,fg= "black", height =6, width = 15, command=lambda: prep_also_likes())
    btn_also_likes.grid(row=1, column=4) 

    btn_also_likes_go = Button(root, bg = "lavender", text = "Go", font = ("Arial", 14), width = 10, height =2,fg= "black", command=lambda: also_like(txt_doc.get(1.0, END).strip(), txt_userID.get(1.0, END).strip()))
    btn_also_likes_go.grid(row=2, column=2, sticky = 'nw')                                                                                 #also_like(txt_doc text, txt_userID text)
    btn_also_likes_go.grid_remove()

    txt_userID = Text(root, font = ("Arial", 14), width = 20, height = 1, fg = "black")
    txt_userID.grid(row=0,column=0)
    txt_userID.grid_remove()

    #text box allowing for user input
    txt_doc = Text(root, font = ("Arial", 14) ,fg= "black", height = 1, width = 20, bg = "lavender")
    txt_doc.grid(row=0, column=0, sticky = 'nw', columnspan=5)
    txt_doc.grid_remove()

    #he is the fixer, he fixes things
    def the_fixer():
        #goes through states dictionary checking which flag has been changed if any
        if (states.get("country") == True): #search for country has been selected
            #fills out relevent data to then be passed on
            freq = search_country(txt_doc.get(1.0, END).strip()) #calls search country method
            title = "Document viewed per country"
            x = "country"
            y = "freq"
        elif (states.get("continent") == True):#search continent has been selected
            #fills out relevent data to then be passed on
            freq = search_continent(txt_doc.get(1.0, END).strip())#calls search continent method
            title = "Document viewed per continent"
            x = "continent"
            y = "freq"
        else:
            print("WARNING: SOMETHING HAS GONE HORRIBLY WRONG")

        #returns a touple of all relevent information to then generate the chart
        return freq ,txt_doc.get(1.0, END).strip() ,title, x, y
    
    #once this button is pressed it will check which flag has been raised and generate the appropriate graph
    btn_choose_doc = Button(root, bg = "lavender", text = "choose document", font = ("Arial", 14) ,fg= "black", command=lambda:create_bar_chart(the_fixer(), root), padx=20)
    btn_choose_doc.grid(row=0, column=1, columnspan=5, sticky='n')
    btn_choose_doc.grid_remove()

    #once pressed directs user back to main page
    btn_back_to_main = Button(root, bg="lavender", text = "back", font = ("Arial", 14) ,fg= "black", command=lambda:back_to_main(), width=10, height=1)
    btn_back_to_main.grid(row=2, column=0, sticky='sw', columnspan=5)
    btn_back_to_main.grid_remove()

    #once pressed directs user back to initial page to select a new file
    btn_back_to_load = Button(root, bg="lavender", text = "back to file selection", font = ("Arial", 14) ,fg= "black", command=lambda:back_to_load(root), width=16, height=1)
    btn_back_to_load.grid(row=2, column=0, sticky='sw')

    ##Creating bar charts
    def create_bar_chart(parameters, root):
        freq, searched, title, x, y = parameters #populates relevent variables using the parameters which is passed in as a 5 piece tuple
        fig = Figure(figsize=(root.winfo_screenwidth(),7), dpi= 80) #configures size of bar chart
        ax = fig.add_subplot(111)

        #fills in all relevent axis and information on bar chart with information passed through parameters
        ax.bar(freq.index, freq.values, color='lavender')
        ax.set_title(f"{title}: {searched}")
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.tick_params(axis='x', rotation=270)

        #Increases bottom margin for graph (prevents x axis title being cut off)
        fig.subplots_adjust(bottom=0.3)

        #dictates position of graph
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=1, column=2, sticky="nsew")
        
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
    #creates list of all user ids and time spent reading found in the list allowing for duplicate entries
    user_time = [(obj.get("visitor_uuid"), obj.get("event_readtime", 0)) for obj in data if "event_readtime" in obj]
    #splits data up
    df = pd.DataFrame(user_time, columns=["User ID", "Read Time"])
    #finds the total time each user has spent reading files (by tallying any duplicates of their uuid)
    agg = df.groupby("User ID")["Read Time"].sum()
    
    #returns users list tallied up with the frequency each user id has been found, will show the top 10 most seen users
    return agg.sort_values(ascending=False).head(10)

##REQ 5
#helper functions
def users_from_doc(documentID):
    #get list of users that have read the given document
    users_viewed = [obj.get("visitor_uuid") for obj in data if obj.get("env_doc_id") == documentID]
    return list(set(users_viewed))
            
def docs_from_users(visitorID):
    #get list of documents that user has read
    documents_viewed = [obj.get("env_doc_id") for obj in data if obj.get("visitor_uuid") == visitorID]
    return documents_viewed

#actual function
#what the fuck is a parameter sorting fucktion sakjdpakisdjmdsgsdaf
def also_like(documentID, visitorID):
    print("DocID: ", documentID)
    print("UserID: ", visitorID)
    
    #get list of "Liked documents"
    if documentID:
        users = users_from_doc(documentID) ##gets list of users who have read a specific document id
        
    if visitorID != "":
        docs = list(set(docs_from_users(visitorID))) ##gets list of documents a specific reader has read

    if documentID and visitorID != "":
        #user -> evry document -> every user- > top 10 docs
        user_docs = []
        for curr in docs: #current document in list of documents
            x = users_from_doc(curr) #finds all users who have viewed this document
            for user in x: #current user who has viewed this doc in the list of users
                if user != visitorID: #not the visitor id
                    user_docs.append(user) #add to list
                    print(user_docs)
            common_users = list(set(user_docs)) #contains all other users which have read a document in common (no duplicates)
        #finds all documents the common_users have read and gets the frequency each document has been viewed
        user_docs_result = [doc for curr_user in common_users for doc in docs_from_users(curr_user)]
        print(pd.Series(user_docs_result).value_counts().head(10)) #COMPLETE
        return pd.Series(user_docs_result).value_counts().head(10) #COMPLETE
    else:
        #we wanna get all the other readers of this document, and then see everything else they have read. then tally the top 10 most common
        read_docs = [doc for curr in users for doc in docs_from_users(curr) if doc != documentID] #WHEN NO VISITOR ID
        print("Series: ", pd.Series(read_docs).value_counts().head(10))
        return pd.Series(read_docs).value_counts().head(10) #COMPLETE

#REQ 6
def also_likes_graph(documentID, userID):
    dot = graphviz.Digraph()

    # 3 - make edges between users and documents they have read!!!

    read_docs = []
    users = users_from_doc(documentID) # all users
    for u in users:
        if u == userID:
            dot.node(u,u[-4:], style='filled', fillcolor='purple', shape='box')
        else:
            dot.node(u, u[-4:], shape='box')    
            
        tempDocs = docs_from_users(u)
        for td in set(tempDocs):
            read_docs.append(td)
            dot.edge(u, td)
        
    # read_docs = set(read_docs)
    print(read_docs)
    for d in read_docs:
        if d == documentID:
            dot.node(d, d[-4:], style='filled', fillcolor='purple')
        else:
            dot.node(d, d[-4:])

    print(read_docs)      

    #iterate through all rel users, get docs they have read
    #make edge between user and doc
    # user list -> find all docs read (use docs_from_users()) -> where user x has read doc y -> make edge
    
    #need userid and docid prefreably in tuple
    #iterate through
    
    # dot.node('A', 'Node A')
    # dot.node('B', 'Node B')

    # dot.edge('A', 'B', 'Edge 1')
    # dot.edge('B', 'A', 'Edge 2')

    dot.render('graph', view=True)

    return

gui_load_file()