import tkinter as tk
from tkinter import *
from tkinter import filedialog, ttk
from tkinter.filedialog import askopenfile 
from Manage import *
import pandas as pd


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Financial Manager")

        # Create instances of the Bill, Income, and BankAccount classes
        self.bill = Bill()
        self.income = Income()
        self.bank_account = BankAccount()

        # Set up the GUI
        self.setup_gui()

    def setup_gui(self):
        # Set up the tabbed interface
        self.tab_parent = tk.Frame(self.root)
        self.tab_parent.pack(expand=1, fill='both')
        self.tabs = ttk.Notebook(self.tab_parent)

        # Set up the "Bills" tab
        self.tab_bills = tk.Frame(self.tabs)
        self.tabs.add(self.tab_bills, text="Bills")
        self.setup_bills_tab()

        # Set up the "Incomes" tab
        self.tab_incomes = tk.Frame(self.tabs)
        self.tabs.add(self.tab_incomes, text="Incomes")
        self.setup_incomes_tab()

        # Set up the "Bank Accounts" tab
        self.tab_bank_accounts = tk.Frame(self.tabs)
        self.tabs.add(self.tab_bank_accounts, text="Bank Accounts")
        self.setup_accounts_tab()

        self.tabs.pack(expand=1, fill='both')

    def setup_bills_tab(self):
        # Set up the "Add Bill" frame
        self.frame_add_bill = tk.Frame(self.tab_bills)
        self.frame_add_bill.pack(side='top', fill='x')

        tk.Label(self.frame_add_bill, text="Bill Name:").pack(side='left')
        self.entry_bill_name = tk.Entry(self.frame_add_bill)
        self.entry_bill_name.pack(side='left')

        tk.Label(self.frame_add_bill, text="Account Name:").pack(side='left')
        self.entry_account_name = tk.Entry(self.frame_add_bill)
        self.entry_account_name.pack(side='left')

        tk.Label(self.frame_add_bill, text="Amount:").pack(side='left')
        self.entry_amount = tk.Entry(self.frame_add_bill)
        self.entry_amount.pack(side='left')

        tk.Label(self.frame_add_bill, text="Month:").pack(side='left')
        self.entry_month = tk.Entry(self.frame_add_bill)
        self.entry_month.pack(side='left')

        tk.Button(self.frame_add_bill, text="Add Bill", command=self.add_bill).pack(side='left')

        # Set up the "Remove Bill" frame
        self.frame_remove_bill = tk.Frame(self.tab_bills)
        self.frame_remove_bill.pack(side='top', fill='x')

        tk.Label(self.frame_remove_bill, text="Bill Name:").pack(side='left')
        self.entry_bill_name_remove = tk.Entry(self.frame_remove_bill)
        self.entry_bill_name_remove.pack(side='left')

        tk.Button(self.frame_remove_bill, text="Remove Bill", command=self.remove_bill).pack(side='left')

        # Set up the "Adjust Bill" frame
        self.frame_adjust_bill = tk.Frame(self.tab_bills)
        self.frame_adjust_bill.pack(side='top', fill='x')

        tk.Label(self.frame_adjust_bill, text="Bill Name:").pack(side='left')
        self.entry_bill_name_adjust = tk.Entry(self.frame_adjust_bill)
        self.entry_bill_name_adjust.pack(side='left')

        tk.Label(self.frame_adjust_bill, text="Field:").pack(side='left')
        self.entry_field = tk.Entry(self.frame_adjust_bill)
        self.entry_field.pack(side='left')

        tk.Label(self.frame_adjust_bill, text="New Value:").pack(side='left')
        self.entry_new_value = tk.Entry(self.frame_adjust_bill)
        self.entry_new_value.pack(side='left')

        tk.Button(self.frame_adjust_bill, text="Adjust Bill", command=self.adjust_bill).pack(side='left')

        # Set up the "Total Amount" frame
        self.frame_total_amount = tk.Frame(self.tab_bills)
        self.frame_total_amount.pack(side='top', fill='x')

        tk.Label(self.frame_total_amount, text="Total Amount:").pack(side='left')
        self.label_total_amount = tk.Label(self.frame_total_amount, text="")
        self.label_total_amount.pack(side='left')

        tk.Button(self.frame_total_amount, text="Update Total Amount", command=self.update_total_amount_bill).pack(side='left')

        # Set up the "Bills" frame
        self.frame_bills = tk.Frame(self.tab_bills)
        self.frame_bills.pack(side='top', fill='both', expand=True)

        self.treeview_bills = ttk.Treeview(self.frame_bills, columns=['Bill Name', 'Account Name', 'Amount', 'Month'])
        self.treeview_bills.pack(side='left', fill='both', expand=True)

        self.treeview_bills.heading('Bill Name', text='Bill Name')
        self.treeview_bills.heading('Account Name', text='Account Name')
        self.treeview_bills.heading('Amount', text='Amount')
        self.treeview_bills.heading('Month', text='Month')

        tk.Button(self.frame_bills, text="Clear Bills", command=self.clear_bills).pack(side='left')

    def setup_incomes_tab(self):
        # Set up the "Add Income" frame
        self.frame_add_income = tk.Frame(self.tab_incomes)
        self.frame_add_income.pack(side='top', fill='x')

        tk.Label(self.frame_add_income, text="Income Name:").pack(side='left')
        self.entry_income_name = tk.Entry(self.frame_add_income)
        self.entry_income_name.pack(side='left')

        tk.Label(self.frame_add_income, text="Account Name:").pack(side='left')
        self.entry_account_name_income = tk.Entry(self.frame_add_income)
        self.entry_account_name_income.pack(side='left')

        tk.Label(self.frame_add_income, text="Amount:").pack(side='left')
        self.entry_amount_income = tk.Entry(self.frame_add_income)
        self.entry_amount_income.pack(side='left')

        tk.Label(self.frame_add_income, text="Month:").pack(side='left')
        self.entry_month_income = tk.Entry(self.frame_add_income)
        self.entry_month_income.pack(side='left')

        tk.Button(self.frame_add_income, text="Add Income", command=self.add_income).pack(side='left')

        # Set up the "Remove Income" frame
        self.frame_remove_income = tk.Frame(self.tab_incomes)
        self.frame_remove_income.pack(side='top', fill='x')

        tk.Label(self.frame_remove_income,text="Income Name:").pack(side='left')
        self.entry_income_name_remove = tk.Entry(self.frame_remove_income)
        self.entry_income_name_remove.pack(side='left')

        tk.Button(self.frame_remove_income, text="Remove Income", command=self.remove_bill).pack(side='left')

        # Set up the "Adjust Income" frame
        self.frame_adjust_income = tk.Frame(self.tab_incomes)
        self.frame_adjust_income.pack(side='top', fill='x')

        tk.Label(self.frame_adjust_income, text="Income Name:").pack(side='left')
        self.entry_income_name_adjust = tk.Entry(self.frame_adjust_income)
        self.entry_income_name_adjust.pack(side='left')

        tk.Label(self.frame_adjust_income, text="Field:").pack(side='left')
        self.entry_field_income = tk.Entry(self.frame_adjust_income)
        self.entry_field_income.pack(side='left')

        tk.Label(self.frame_adjust_income, text="New Value:").pack(side='left')
        self.entry_new_value_income = tk.Entry(self.frame_adjust_income)
        self.entry_new_value_income.pack(side='left')

        tk.Button(self.frame_adjust_income, text="Adjust Income",
        command=self.adjust_bill).pack(side='left')

        # Set up the "Total Amount" frame
        self.frame_total_amount_income = tk.Frame(self.tab_incomes)
        self.frame_total_amount_income.pack(side='top', fill='x')

        tk.Label(self.frame_total_amount_income, text="Total Amount:").pack(side='left')
        self.label_total_amount_income = tk.Label(self.frame_total_amount_income, text="")
        self.label_total_amount_income.pack(side='left')

        tk.Button(self.frame_total_amount_income, text="Update Total Amount", command=self.update_total_amount_income).pack(side='left')

        # Set up the "Incomes" frame
        self.frame_incomes = tk.Frame(self.tab_incomes)
        self.frame_incomes.pack(side='top', fill='both', expand=True)

        self.treeview_incomes = ttk.Treeview(self.frame_incomes, columns=['Income Name', 'Account Name', 'Amount', 'Month'])
        self.treeview_incomes.pack(side='left', fill='both', expand=True)

        self.treeview_incomes.heading('Income Name', text='Income Name')
        self.treeview_incomes.heading('Account Name', text='Account Name')
        self.treeview_incomes.heading('Amount', text='Amount')
        self.treeview_incomes.heading('Month', text='Month')

        tk.Button(self.frame_incomes, text="Clear Incomes", command=self.clear_incomes).pack(side='left')


    def setup_accounts_tab(self):
        # Set up the "Add Account" frame
        self.frame_add_account = tk.Frame(self.frame_accounts)
        self.frame_add_account.pack(side='top', fill='x')

        tk.Label(self.frame_add_account, text="Account Name:").pack(side='left')
        self.entry_account_name_add = tk.Entry(self.frame_add_account)
        self.entry_account_name_add.pack(side='left')

        tk.Label(self.frame_add_account, text="Owner:").pack(side='left')
        self.entry_owner = tk.Entry(self.frame_add_account)
        self.entry_owner.pack(side='left')

        tk.Label(self.frame_add_account, text="Bank Name:").pack(side='left')
        self.entry_bank_name = tk.Entry(self.frame_add_account)
        self.entry_bank_name.pack(side='left')

        tk.Label(self.frame_add_account, text="Account Type:").pack(side='left')
        self.entry_account_type = tk.Entry(self.frame_add_account)
        self.entry_account_type.pack(side='left')

        tk.Label(self.frame_add_account, text="Account Balance:").pack(side='left')
        self.entry_account_balance = tk.Entry(self.frame_add_account)
        self.entry_account_balance.pack(side='left')

        tk.Label(self.frame_add_account, text="Purpose:").pack(side='left')
        self.entry_purpose = tk.Entry(self.frame_add_account)
        self.entry_purpose.pack(side='left')

        tk.Button(self.frame_add_account, text="Add Account", command=self.add_account).pack(side='left')

        # Set up the "Remove Account" frame
        self.frame_remove_account = tk.Frame(self.tab_accounts)
        self.frame_remove_account.pack(side='top', fill='x')

        tk.Label(self.frame_remove_account, text="Account Name:").pack(side='left')
        self.entry_account_name_remove = tk.Entry(self.frame_remove_account)
        self.entry_account_name_remove.pack(side='left')

        tk.Button(self.frame_remove_account, text="Remove Account", command=self.remove_account).pack(side='left')

        # Set up the "Adjust Account" frame
        self.frame_adjust_account = tk.Frame(self.tab_accounts)
        self.frame_adjust_account.pack(side='top', fill='x')

        tk.Label(self.frame_adjust_account, text="Account Name:").pack(side='left')
        self.entry_account_name_adjust = tk.Entry(self.frame_adjust_account)

        # Set up the "Accounts" frame
        self.frame_accounts = tk.Frame(self.tab_accounts)
        self.frame_accounts.pack(side='top', fill='both', expand=True)

        self.treeview_accounts = ttk.Treeview(self.frame_accounts, columns=['Account Name', 'Owner', 'Bank Name', 'Account Type', 'Account Balance', 'Purpose'])
        self.treeview_accounts.pack(side='left', fill='both', expand=True)

        self.treeview_accounts.heading('Account Name', text='Account Name')
        self.treeview_accounts.heading('Owner', text='Owner')
        self.treeview_accounts.heading('Bank Name', text='Bank Name')
        self.treeview_accounts.heading('Account Type', text='Account Type')
        self.treeview_accounts.heading('Account Balance', text='Account Balance')
        self.treeview_accounts.heading('Purpose', text='Purpose')

        tk.Button(self.frame_accounts, text="Clear Accounts", command=self.clear_accounts).pack(side='left')

    def add_bill(self):
        bill_name = self.entry_bill_name.get()
        account_name = self.entry_account_name_bill.get()
        amount = self.entry_amount_bill.get()
        month = self.entry_month_bill.get()

        self.bills.add_bill(bill_name, account_name, amount, month)
        self.update_bills()

    def remove_bill(self):
        bill_name = self.entry_bill_name_remove.get()

        self.bills.remove_bill(bill_name)
        self.update_bills()

    def adjust_bill(self):
        bill_name = self.entry_bill_name_adjust.get()
        field = self.entry_field_bill.get()
        new_value = self.entry_new_value_bill.get()

        self.bills.adjust_bill(bill_name, field, new_value)
        self.update_bills()

    def update_total_amount_bill(self):
        total_amount = self.bills.sum_amounts()
        self.label_total_amount_bill.config(text=str(total_amount))

    def clear_bills(self):
        self.bills.clear_bills()
        self.update_bills()

    def update_bills(self):
        self.treeview_bills.delete(*self.treeview_bills.get_children())

        bills = self.bills.get_bills()
        for _, bill in bills.iterrows():
            self.treeview_bills.insert('', 'end', values=bill.tolist())

        self.update_total_amount_bill()

    def add_income(self):
        income_name = self.entry_income_name.get()
        account_name = self.entry_account_name_income

    def update_total_amount_income(self):
        total_amount = self.incomes.sum_amounts()
        self.label_total_amount_income.config(text=str(total_amount))

    def clear_incomes(self):
        self.incomes.clear_incomes()
        self.update_incomes()

    def update_incomes(self):
        self.treeview_incomes.delete(*self.treeview_incomes.get_children())

        incomes = self.incomes.get_incomes()
        for _, income in incomes.iterrows():
            self.treeview_incomes.insert('', 'end', values=income.tolist())

        self.update_total_amount_income()

    def add_account(self):
        account_name = self.entry_account_name_add.get()
        owner = self.entry_owner.get()
        bank_name = self.entry_bank_name.get()
        account_type = self.entry_account_type.get()
        account_balance = self.entry_account_balance.get()
        purpose = self.entry_purpose.get()

        self.accounts.add_account(account_name, owner, bank_name, account_type, account_balance, purpose)
        self.update_accounts()

    def remove_account(self):
        account_name = self.entry_account_name_remove.get()

        self.accounts.remove_account(account_name)
        self.update_accounts()

    def adjust_account(self):
        account_name = self.entry_account_name_adjust.get()
        field = self.entry_field_account.get()
        new_value = self.entry_new_value_account.get()

        self.accounts.adjust_account(account_name, field, new_value)
        self.update_accounts()

    def clear_accounts(self):
        self.accounts.clear_accounts()
        self.update_accounts()

    def update_accounts(self):
        self.treeview_accounts.delete(*self.treeview_accounts.get_children())

        accounts = self.accounts.get_accounts()
        for _, account in accounts.iterrows():
            self.treeview_accounts.insert('', 'end', values=account.tolist())

    def run(self):
        self.root.mainloop()


def main():
    gui = App()
    gui.run()

if __name__ == '__main__':
    main()