from tracking_services import *
import pandas as pd
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.simpledialog 
import tkinter.messagebox
import tkinter.filedialog
import os


NUM_T_MONTH = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

class FinanceTrackerApp():
    '''
    to do:
    - add a timeline tab
    - add accounts tab
    - show properties of bills such as pie charts of selected categories (eg. by month, by account, etc.), same for incomes
    '''
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Bill Tracker")
        self.master.geometry("600x500")
        self.bill_class = Bill()
        self.income_class = Income()
        self.account_class = BankAccount()

        # create a Notebook widget with two tabs
        self.notebook = ttk.Notebook(self.master)
        self.tab1 = tk.Frame(self.notebook)
        self.tab2 = tk.Frame(self.notebook)
        self.tab3 = tk.Frame(self.notebook)
        self.tab4 = tk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Bills")
        self.notebook.add(self.tab2, text="Incomes")
        self.notebook.add(self.tab3, text="Accounts")
        self.notebook.add(self.tab4, text="Timeline")
        self.notebook.pack(expand=1, fill="both")

        # create widgets for the Bills tab
        self.bill_list_frame = tk.Frame(self.tab1)
        self.bill_list_frame.pack(side="left", fill="y")
        self.bill_list = tk.Listbox(self.bill_list_frame, width=74, height=15)
        self.bill_fields = ["Bill", "Account", "Amount", "Month"]
        self.bill_list.pack()
        self.add_bill_button = tk.Button(self.bill_list_frame, text="Add Bill", command=self.add_bill)
        self.add_bill_button.pack()
        self.edit_bill_button = tk.Button(self.bill_list_frame, text="Edit Bill", command=self.edit_bill)
        self.edit_bill_button.pack()
        self.delete_bill_button = tk.Button(self.bill_list_frame, text="Delete Bill", command=self.delete_bill)
        self.delete_bill_button.pack()
        self.bill_total_label = tk.Label(self.bill_list_frame, text="Total:")
        self.bill_total_label.pack()
        self.bill_total = tk.Label(self.bill_list_frame, text="$0")
        self.bill_total.pack()
    

        # create widgets for the Incomes tab
        self.income_list_frame = tk.Frame(self.tab2)
        self.income_list_frame.pack(side="left", fill="y")
        self.income_list = tk.Listbox(self.income_list_frame, width=74, height=15)
        self.income_fields = ["Income", "Account", "Amount", "Month"]
        self.income_list.pack()
        self.add_income_button = tk.Button(self.income_list_frame, text="Add Income", command=self.add_income)
        self.add_income_button.pack()
        self.edit_income_button = tk.Button(self.income_list_frame, text="Edit Income", command=self.edit_income)
        self.edit_income_button.pack()
        self.delete_income_button = tk.Button(self.income_list_frame, text="Delete Income", command=self.delete_income)
        self.delete_income_button.pack()
        self.income_total_label = tk.Label(self.income_list_frame, text="Total:")
        self.income_total_label.pack()
        self.income_total = tk.Label(self.income_list_frame, text="$0")
        self.income_total.pack()

        # create a menu bar
        self.menu_bar = tk.Menu(self.master)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As...", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.close_app)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.master.config(menu=self.menu_bar)

        # create a context menu for the Bill list
        self.bill_context_menu = tk.Menu(self.bill_list, tearoff=0)
        self.bill_context_menu.add_command(label="Add Bill", command=self.add_bill)
        self.bill_context_menu.add_command(label="Edit Bill", command=self.edit_bill)
        self.bill_context_menu.add_command(label="Delete Bill", command=self.delete_bill)

        # create a context menu for the Income list
        self.income_context_menu = tk.Menu(self.income_list, tearoff=0)
        self.income_context_menu.add_command(label="Add Income", command=self.add_income)
        self.income_context_menu.add_command(label="Edit Income", command=self.edit_income)
        self.income_context_menu.add_command(label="Delete Income", command=self.delete_income)

        # bind the right mouse button to the context menu
        self.bill_list.bind("<Button-3>", self.show_bill_context_menu)
        self.income_list.bind("<Button-3>", self.show_income_context_menu)

        # update the bill and income lists
        self.update_bill_list()
        self.update_income_list()
    
        # saving to file parameters
        self.current_filepath = None

    def add_bill(self):
        # open a dialog to add a new bill
        bill_name = tk.simpledialog.askstring("Add Bill", "Bill Name:")
        if bill_name is not None:
            acc_name = tk.simpledialog.askstring("Add Bill", "Account Name:")
            amount = tk.simpledialog.askfloat("Add Bill", "Amount:")
            month = tk.simpledialog.askinteger("Add Bill", "Month:")
            self.bill_class.add_bill(bill_name, acc_name, amount, month)
            self.update_bill_list()

    def edit_bill(self):
        # get the selected bill
        selected_bill = self.bill_list.curselection()
        if len(selected_bill) == 0:
            tk.messagebox.showwarning("Edit Bill", "No bill selected.")
            return
        bill_name = self.bill_list.get(selected_bill)
        # open a dialog to edit the bill
        new_bill_name = tk.simpledialog.askstring("Edit Bill", "Bill Name:", initialvalue=bill_name)
        if new_bill_name is not None:
            acc_name = tk.simpledialog.askstring("Edit Bill", "Account Name:")
            amount = tk.simpledialog.askfloat("Edit Bill", "Amount:")
            month = tk.simpledialog.askstring("Edit Bill", "Month:")
            self.bill_class.adjust_bill(bill_name, 'Bill Name', new_bill_name)
            self.bill_class.adjust_bill(bill_name, 'Account Name', acc_name)
            self.bill_class.adjust_bill(bill_name, 'Amount', amount)
            self.bill_class.adjust_bill(bill_name, 'Month', month)
            self.update_bill_list()

    def delete_bill(self):
        # get the selected bill
        selected_bill = self.bill_list.curselection()
        if len(selected_bill) == 0:
            tk.messagebox.showwarning("Delete Bill", "No bill selected.")
            return
        bill_name = self.bill_list.get(selected_bill)
        # confirm the deletion
        result = tk.messagebox.askyesno("Delete Bill", f"Are you sure you want to delete {bill_name}?")
        if result:
            self.bill_class.remove_bill(bill_name)
            self.update_bill_list()

    def add_income(self):
        # open a dialog to add a new income
        income_name = tk.simpledialog.askstring("Add Income", "Income Name:")
        if income_name is not None:
            acc_name = tk.simpledialog.askstring("Add Income", "Account Name:")
            amount = tk.simpledialog.askfloat("Add Income", "Amount:")
            month = tk.simpledialog.askstring("Add Income", "Month:")
            self.income_class.add_income(income_name, acc_name, amount, month)
            self.update_income_list()

    def edit_income(self):
        # get the selected income
        selected_income = self.income_list.curselection()
        if len(selected_income) == 0:
            tk.messagebox.showwarning("Edit Income", "No income selected.")
            return
        income_name = self.income_list.get(selected_income)
        # open a dialog to edit the income
        new_income_name = tk.simpledialog.askstring("Edit Income", "Income Name:", initialvalue=income_name)
        if new_income_name is not None:
            acc_name = tk.simpledialog.askstring("Edit Income", "Account Name:")
            amount = tk.simpledialog.askfloat("Edit Income", "Amount:")
            month = tk.simpledialog.askstring("Edit Income", "Month:")
            self.income_class.adjust_income(income_name, 'Income Name', new_income_name)
            self.income_class.adjust_income(income_name, 'Account Name', acc_name)
            self.income_class.adjust_income(income_name, 'Amount', amount)
            self.income_class.adjust_income(income_name, 'Month', month)
            self.update_income_list()

    def delete_income(self):
        # get the selected income
        selected_income = self.income_list.curselection()
        if len(selected_income) == 0:
            tk.messagebox.showwarning("Delete Income", "No income selected.")
            return
        income_name = self.income_list.get(selected_income)
        # confirm the deletion
        result = tk.messagebox.askyesno("Delete Income", f"Are you sure you want to delete {income_name}?")
        if result:
            self.income_class.remove_income(income_name)
            self.update_income_list()
    
    def update_bill_list(self):
        # clear the list and refill it with the updated bill DataFrame
        self.bill_list.delete(0, "end")
        self.bill_list.insert("end",
            f"{self.bill_fields[0].center(30-len(self.bill_fields[0]))}|{self.bill_fields[1].center(30-len(self.bill_fields[1]))}\
                |{self.bill_fields[2].center(30-len(self.bill_fields[2]))}|{self.bill_fields[3].center(30-len(self.bill_fields[3]))}|")
        df = self.bill_class.get_bills()
        for index, row in df.iterrows():
            bill_name = row["Bill Name"]
            acc_name = row["Account Name"]
            amount = "$" + str(row["Amount"])
            month = row["Month"]
            self.bill_list.insert("end",
            f"{bill_name.center(30-len(bill_name))}|{acc_name.center(30-len(acc_name))}\
                |{amount.center(30-len(str(amount)))}|{NUM_T_MONTH[month].center(30-len(NUM_T_MONTH[month]))}|")

        self.bill_total["text"] = "$" + str(self.bill_class.sum_amounts())
    
    def update_income_list(self):
        # clear the list and refill it with the updated income DataFrame
        self.income_list.delete(0, "end")
        self.income_list.insert("end", 
            f"{self.income_fields[0].center(30-len(self.income_fields[0]))}|{self.income_fields[1].center(30-len(self.income_fields[1]))}\
                |{self.income_fields[2].center(30-len(self.income_fields[2]))}|{self.income_fields[3].center(30-len(self.income_fields[3]))}|")
        df = self.income_class.get_incomes()
        for index, row in df.iterrows():
            income_name = row["Income Name"]
            acc_name = row["Account Name"]
            amount = "$" + str(row["Amount"])
            month = row["Month"]
            self.income_list.insert("end", f" {income_name} |    | {acc_name} |    | {amount} |    {NUM_T_MONTH[month]} |")
        self.income_total["text"] = "$" + str(self.income_class.sum_amounts())
    
    def show_bill_context_menu(self, event):
        # show the context menu
        self.bill_context_menu.tk_popup(event.x_root, event.y_root)

    def show_income_context_menu(self, event):
        # show the context menu
        self.income_context_menu.tk_popup(event.x_root, event.y_root)

    def new_file(self):
        # confirm unsaved changes
        if self.bill_class.used or self.income_class.used:
            result = tk.messagebox.askyesnocancel("Unsaved Changes", "There are unsaved changes. Do you want to save them?")
            if result is None:
                return
            elif result:
                self.save_file()
        # clear the bill and income lists
        self.bill_class.clear_bills()
        self.income_class.clear_bills()
        self.update_bill_list()
        self.update_income_list()
        self.bill_class.used = False
        self.income_class.used = False

    def open_file(self):
        # confirm unsaved changes
        if self.bill_class.used or self.income_class.used:
            result = tk.messagebox.askyesnocancel("Unsaved Changes", "There are unsaved changes. Do you want to save them?")
            if result is None:
                return
            elif result:
                self.save_file()
        # open a file dialog to select a file
        filepath = tk.filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if filepath:
            # clear the bill and income lists
            self.bill_class.clear_bills()
            self.income_class.clear_bills()
            # read the file and set the bill and income DataFrames
            df = pd.read_excel(filepath, sheet_name=None)
            self.bill_class._set_bills(df['Bills'])
            self.income_class._set_incomes(df['Incomes'])
            self.update_bill_list()
            self.update_income_list()
            self.bill_class.used = True
            self.income_class.used = True
    
    def save_file(self):
        # check if the file has been saved before
        if self.current_filepath is None:
            self.save_as_file()
        else:
            # create a Pandas Excel writer using the xlsxwriter engine
            writer = pd.ExcelWriter(self.current_filepath, engine='xlsxwriter')
            # write the bill and income DataFrames to the Excel file
            self.bill_class.get_bills().to_excel(writer, sheet_name='Bills', index=False)
            self.income_class.get_incomes().to_excel(writer, sheet_name='Incomes', index=False)
            # save the file
            writer.save()
            self.bill_class.used = False
            self.income_class.used = False

    def save_as_file(self):
        # open a file dialog to select a file
        filepath = tk.filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if filepath:
            # save the file
            self.current_filepath = filepath
            self.save_file()

    def close_app(self):
        # confirm unsaved changes
        if self.bill_class.used or self.income_class.used:
            result = tk.messagebox.askyesnocancel("Unsaved Changes", "There are unsaved changes. Do you want to save them?")
            if result is None:
                return
            elif result:
                self.save_file()
        # destroy the root window
        self.master.destroy()

def main():
    # create the root window
    root = tk.Tk()
    # create the application
    app = FinanceTrackerApp(root)
    # run the main loop
    root.mainloop()

if __name__ == '__main__':
    main()