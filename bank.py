import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from pandastable import Table, TableModel
from finance_tools import *

Month_id_dict = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}


### Tool to generate monthly reports


class Bill:
    def __init__(self):
        self.items = pd.DataFrame()
    
    def add_item(self, item_name, item_amount, bill='bill'):
        self.n = bill
        new_row = pd.Series({f'{self.n}_name': item_name, 
                             'item_amount': item_amount})
        self.items = pd.concat([self.items, new_row.to_frame().T], ignore_index=True)
    
    def remove_item(self, item_name):
        self.items.drop(self.items[self.items[f'{self.n}_name'] == item_name].index, inplace=True)
    
    def update_item(self, item_name, new_item_name, new_item_amount):
        self.remove_item(item_name)
        self.add_item(new_item_name, new_item_amount)
    
    def bill(self):
        return self.items

class Income:
    def __init__(self):
        self.items = pd.DataFrame()
    
    
    def add_income(self, income_name, income_amount):
        # add income_name to self.income using pandas.concat
        new_row = pd.Series({'income_name': income_name, 'income_amount': income_amount})
        self.items = pd.concat([self.items, new_row.to_frame().T], ignore_index=True)

    def remove_income(self,income_name):
        # remove the income_name from self.income
        self.items.drop(self.items[self.items['income_name'] == income_name].index, inplace=True)
    
    def update_income(self, income_name, new_income_name, new_income_amount):
        self.remove_income(income_name)
        self.add_income(new_income_name, new_income_amount)
    
    
    def get_income_filtertype(self, income_name):
        return self.income[self.income['income_name'] == income_name]

    def income(self):
        return self.items


       

class Bank_info:
    def __init__(self):
        self.accounts=pd.DataFrame()
        self.bills = {}
        self.expenses = {}
        self.income = {}
        self.cur_bank_id = 0

    def add_account(self, account_name, owner, account_balance, bank, account_type, purpose):
        new_row = pd.Series({'id': self.cur_bank_id,
                             'account_name': account_name,
                             'owner': owner,
                             'account_balance': account_balance,
                             'Bank': bank,
                             'account_type': account_type,
                             'purpose': purpose})
        self.accounts = pd.concat([self.accounts, new_row.to_frame().T], ignore_index=True)
        self.cur_bank_id +=1

    def get_bills(self):
        return self.bills
    
    def get_expenses(self):
        return self.expenses
    
    def get_income(self):
        return self.income

    def get_account_table(self):
        return self.accounts

    def get_account_byname(self, account_name):
        return self.accounts[account_name]

    def add_bill(self, bill: Bill, account_name, month):
        ''' store bill and update account balance in accounts'''
        self.bills[month] = bill.bill()
        total_bill = bill.items['item_amount'].sum()
        # subtract total_bill from account_balance
        self.accounts.loc[self.accounts['account_name'] == account_name, 'account_balance'] -= total_bill

    def on_going_payment(type, account_name, period, Start_Month):
        pass


    def add_expenses(self, expenses: Bill, account_name, month):
        ''' store bill and update account balance in accounts'''
        self.expenses[month] = expenses.bill()
        total_expenses = expenses.items['item_amount'].sum()
        # subtract total_bill from account_balance
        self.accounts.loc[self.accounts['account_name'] == account_name, 'account_balance'] -= total_expenses

    def add_income(self, income: Income, account_name, month):
        ''' store income and update account balance in accounts'''
        self.income[month] = income.income()
        total_income = income.items['income_amount'].sum()
        # add total_income to account_balance
        self.accounts.loc[self.accounts['account_name'] == account_name, 'account_balance'] += total_income
    
    def generate_report(self, parent_dir, year):
        '''generate a folder of all unique months in either bills or income, 
           group bill and income by month and create a txt file of bill.txt and income.txt'''
         
        # create a folder named year in parent_dir
        year_dir = os.path.join(parent_dir, str(year))
        if not os.path.exists(year_dir):
            os.mkdir(year_dir)
            

        # create a folder for each month in year_dir
        print(self.income, self.bills, self.expenses, sep='\n')
        for month in Month_id_dict:
            month_dir = os.path.join(year_dir, month)
            if not os.path.exists(month_dir):
                os.mkdir(month_dir)
                open(os.path.join(month_dir, 'bills.txt'), 'w').close()
                open(os.path.join(month_dir, 'expenses.txt'), 'w').close()
                open(os.path.join(month_dir, 'incomes.txt'), 'w').close()
        
        # create bills.txt
        for month in self.bills.keys():
            month_dir = os.path.join(year_dir, month)
            # write bills txt file
            with open(os.path.join(month_dir, 'bills.txt'), 'w') as f:
                names = self.bills[month]['bill_name']
                item_amounts = self.bills[month]['item_amount']
                for item_name, item_amount in zip(names, item_amounts):
                    f.write(f'{item_name} {item_amount}\n')
            
        # create expenses.txt
        for month in self.expenses.keys():
            month_dir = os.path.join(year_dir, month)
            # write expenses txt file
            with open(os.path.join(month_dir, 'expenses.txt'), 'w') as f:
                names = self.expenses[month]['expense_name']
                item_amounts = self.expenses[month]['item_amount']
                for item_name, item_amount in zip(names, item_amounts):
                    f.write(f'{item_name} {item_amount}\n')

        
        # create income.txt
        for month in self.income.keys():
            month_dir = os.path.join(year_dir, month)
            # write income txt file
            with open(os.path.join(month_dir, 'incomes.txt'), 'w') as f:
                names = self.income[month]['income_name']
                item_amounts = self.income[month]['income_amount']
                for item_name, item_amount in zip(names, item_amounts):
                    f.write(f'{item_name} {item_amount}\n')

    def total_Account_balance(self):
        return format(self.accounts['account_balance'].sum(), '.2f')
    
    def total_income(self):
        return format(self.income['income_amount'].sum(), '.2f')
    
    def total_expenses(self):
        return format(self.expenses['item_amount'].sum(), '.2f')

    def total_bills(self):
        return format(self.bills['item_amount'].sum(), '.2f')
    
        
            

        
## Debt
        

if __name__ == '__main__':
    ## Income
    print('__________Income_________')
    i = Income()
    i.add_income('Bao_salary', 3000)
    i.add_income('Tram_salary', 3000)
    print(i.items)
    print('_______________________')

    ## Bills
    print('__________Bill__________')
    b = Bill()
    b.add_item('Gas', 100)
    b.add_item('Groceries', 200)
    b.add_item('Rent', 1000)
    print(b.items)
    print('_______________________')


    ## expenses
    print('__________Expenses_________')
    e = Bill()
    e.add_item('PC', 100, bill='expense')
    e.add_item('Mouse', 200, bill='expense')
    e.add_item('flowers', 1000, bill='expense')
    print(e.items)
    print('_______________________')


    # Bank
    print('_________Bank___________')
    bank1 = Bank_info()
    bank1.add_account('Bao_chequing', 'Bao', 12000, 'TD', 'Chequing', 'Gas')
    bank1.add_account('Bao_savings', 'Bao', 5000, 'TD', 'Savings', 'Personal')
    bank1.add_account('Tram_chequing', 'Tram', 2000, 'TD', 'Chequing', 'Groceries')
    bank1.add_account('Tram_savings', 'Tram', 2000, 'TD', 'Savings', 'Personal')
    bank1.add_account('Joint_savings', 'Bao&Tram', 13000, 'TD', 'Savings', 'Joint savings for bills')
    print(bank1.get_account_table())
    print('_______________________')

    # add bills
    print('_________Add Bills___________')
    bank1.add_bill(b, 'Bao_chequing', 'Jan')
    print(bank1.get_account_table())
    print('_______________________')
    print(bank1.get_bills())

    # add expenses
    print('_________Add Expenses___________')
    bank1.add_expenses(e, 'Bao_chequing', 'Feb')
    print(bank1.get_account_table())
    print('_______________________')
    print(bank1.get_expenses())

    # add income
    print('_________Add Income___________')
    bank1.add_income(i, 'Joint_savings', 'Jan')
    print(bank1.get_account_table())

    # generate report
    print('_________Generate Report___________')
    bank1.generate_report('/Users/baoha/Desktop/Automation Script/Budget_Tracking', 2024)


    timeline = Timeline_budget()
    timeline.initate_existing_networth(35000)
    timeline.add_month_pkg('/Users/baoha/Desktop/Automation Script/Budget_Tracking/2024', 0)
    frame = timeline.get_timeline()
    print(frame)