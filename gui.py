from tkinter import *
from tkinter import filedialog, ttk
from tkinter import filedialog, ttk
from tkinter.filedialog import askopenfile 
from finance_tools import *
from pandas import DataFrame
import pandas as pd
from pandastable import Table, TableModel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Budget_GUI:
    def __init__(self, master: Tk, name_app: str = "A simple Budget GUI"):
        self.master = master
        self.master.title(name_app)
        self.master.geometry("800x600")
        self.master.resizable(False, False)
        


        ## elements:
        self.folder_path = ""
        self.init_amount = 0
        self.saving_amount = 0
        self.cur_clip_board = "" # copy and paste status of file path
        self.fold_p_box = None
        self.init_amount_box = None
        self.saving_amount_box = None

        self.table=None
        

    def run(self):
        self.home_screen()
        self.master.mainloop()

    def add_home_button(self):
        # create a button object with text "Home" placed at the top right corner
        home_button = Button(self.master, text="Home", command=self.home_screen)
        home_button.place(relx=0.05, rely=0.03, anchor=CENTER)
    
    def add_close_button(self):
        # create a button object with text "Close" placed at the top right corner
        close_button = Button(self.master, text="Close", command=self.master.quit)
        close_button.place(relx=0.95, rely=0.03, anchor=CENTER)

    def home_screen(self, title: str = "Welcome to Budget Tracking", start_txt: str = "Start Budget Monitoring"):
        # clear all buttons and labels
        self.clear_screen()
        # create a button object with text "Start Budget monitoring" with size 20x3 placed at bottom third of the window
        start_button = Button(self.master, text=start_txt, font=("Goudy Type", 12),
        command=self.start_budget_monitoring)
        start_button.place(relx=0.5, rely=0.5, anchor=CENTER)

        # create a button object with text "Close" placed at the top right corner
        close_button = Button(self.master, text="Close", command=self.master.quit)
        close_button.place(relx=0.95, rely=0.03, anchor=CENTER)

        # add a label object with text "Welcom to Budget Tracking" to the window with large Font
        label = Label(self.master, text=title, font=("Goudy Type", 30))
        label.place(relx=0.5, rely=0.3, anchor=CENTER)
    
    def clear_screen(self):
        ## clear all buttons and labels
        for widget in self.master.winfo_children():
            widget.destroy()

    def browse_budget_folder(self):
        # open a file dialog to select a folder and close the dialog
        self.cur_clip_board = filedialog.askdirectory()
        self.fold_p_box.insert(0, self.cur_clip_board)

    def Dashboard(self):
        self.master.geometry("800x900")
        self.clear_screen()
        self.add_close_button()
        self.add_home_button()
        
        # get stats & data
        timeline = Timeline_budget()
        timeline.initate_existing_networth(self.init_amount)
        timeline.add_month_pkg(self.folder_path, self.saving_amount)
        budget_frame = timeline.get_timeline()
        pie_chart = timeline.get_pie_chart()
        stats = timeline.get_stats()
        print(budget_frame)
        print(pie_chart)
        print(stats)

        #convert budget_frame to a tablemodel
        self.convert_to_table(budget_frame)
        #convert pie_chart to a tablemodel
        

        
    
    def show_dataframe(self, df: pd.DataFrame, frame):
        # convert scientific notation to float for every value in dataframe 
        df = df.applymap(lambda x: '{:,.2f}'.format(x) if isinstance(x, float) else x)
        # frame from self.master
        frame = Frame(frame)
        # increase frame size to fit the table without scrollbars
        frame.pack(expand=True, fill='both')
        # create a table
        self.table = Table(frame, dataframe=df)
        self.table.show()



    def confirm_input(self):
        # get the folder path and initial amount from the input boxes
        self.folder_path = self.fold_p_box.get()
        self.init_amount = self.init_amount_box.get()
        self.saving_amount = self.saving_amount_box.get()
        # check if the input is valid
        if self.folder_path == "" or self.init_amount == "" or self.saving_amount == "":
            # show the error message as a red label on the top of self.master
            error_label = Label(self.master, text="Please enter a valid input", fg="red")
            error_label.place(relx=0.5, rely=0.1, anchor=CENTER)
            return
        # check if the folder path is valid
        if not os.path.isdir(self.folder_path):
            error_label = Label(self.master, text="Please enter a valid folder path", fg="red")
            error_label.place(relx=0.5, rely=0.1, anchor=CENTER)
            return
        # check if the initial amount is valid
        try:
            self.init_amount = float(self.init_amount)
        except ValueError:
            error_label = Label(self.master, text="Please enter a valid initial amount", fg="red")
            error_label.place(relx=0.5, rely=0.1, anchor=CENTER)
            return
        # check if the saving amount is valid
        try:
            self.saving_amount = float(self.saving_amount)
        except ValueError:
            error_label = Label(self.master, text="Please enter a valid saving amount", fg="red")
            error_label.place(relx=0.5, rely=0.1, anchor=CENTER)
            return

        # if all the input is valid, start the budget monitoring
        print("folder path: ", self.folder_path)
        print("initial amount: ", self.init_amount)
        print("saving amount: ", self.saving_amount)
        self.Dashboard() 

        

    def start_budget_monitoring(self):
        # clear all buttons and labels
        self.clear_screen()
        self.add_close_button()
        self.add_home_button()


        # setup elements

        label = Label(self.master, text="Enter the file path of the folder")
        label.place(relx=0.5, rely=0.2, anchor=CENTER)
        
        # add a black bordered input box with white background with 2px thick and a placeholder text and activate immediately
        
        self.fold_p_box = Entry(self.master, width=50, borderwidth=2, bg="white")
        self.fold_p_box.focus_set()
        self.fold_p_box.place(relx=0.5, rely=0.25, anchor=CENTER)
        # add button to browse for folder path
        browse_button = Button(self.master, text="▽", command=self.browse_budget_folder)
        browse_button.place(relx=0.82, rely=0.245, anchor=CENTER)
        
        
        label2 = Label(self.master, text="Enter the initial amount you have")
        label2.place(relx=0.5, rely=0.4, anchor=CENTER)

        self.init_amount_box = Entry(self.master, width=50, borderwidth=2, bg="white")
        self.init_amount_box.focus_set()
        self.init_amount_box.place(relx=0.5, rely=0.45, anchor=CENTER)


        label3 = Label(self.master, text="Savings per month")
        label3.place(relx=0.5, rely=0.6, anchor=CENTER)
        self.saving_amount_box = Entry(self.master, width=50, borderwidth=2, bg="white")
        self.saving_amount_box.focus_set()
        self.saving_amount_box.place(relx=0.5, rely=0.65, anchor=CENTER)

        # add a button to confirm the input
        confirm_button = Button(self.master, text="Confirm", command=self.confirm_input)
        confirm_button.place(relx=0.5, rely=0.8, anchor=CENTER)





       

       
       

       


