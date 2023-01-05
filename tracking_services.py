import pandas as pd
import copy as cp

INCOMES =[]
BILLS = []

class Bill:
    def __init__(self):
        # create an empty DataFrame with the specified fields
        self.df = pd.DataFrame(columns=['Bill Name', 'Account Name', 'Amount', 'Month'])
        self.used = False

    def add_bill(self, bill_name, Acc_name, amount, month):
        # create a new DataFrame with the bill information
        new_bill = pd.DataFrame({'Bill Name': [bill_name], 'Account Name': [Acc_name], 'Amount': [amount], 'Month': [month]})
        # add the new DataFrame to the existing DataFrame using pd.concat
        self.df = pd.concat([self.df, new_bill])

    def remove_bill(self, bill_name):
        # remove a bill from the DataFrame by BillID
        self.df = self.df[self.df['Bill Name'] != bill_name]

    def adjust_bill(self, bill_name, field, new_value):
        # adjust a field of a bill by BillID
        self.df.loc[self.df['Bill Name'] == bill_name, field] = new_value

    def sum_amounts(self):
        # sum the Amount column
        return self.df['Amount'].sum()

    def get_bills(self):
        # return the DataFrame
        return self.df

    def clear_bills(self):
        # clear the DataFrame
        self.df = pd.DataFrame(columns=['Bill Name', 'Account Name', 'Amount', 'Month'])


class Income:
    def __init__(self):
        # create an empty DataFrame with the specified fields
        self.df = pd.DataFrame(columns=['Income Name', 'Account Name', 'Amount', 'Month'])
        self.used = False

    def add_income(self, income_name, Acc_name, amount, month):
        # create a new DataFrame with the income information
        new_income = pd.DataFrame({'Income Name': [income_name], 'Account Name': [Acc_name], 'Amount': [amount], 'Month': [month]})
        # add the new DataFrame to the existing DataFrame using pd.concat
        self.df = pd.concat([self.df, new_income])

    def remove_income(self, income_name):
        # remove an income from the DataFrame by IncomeID
        self.df = self.df[self.df['Income Name'] != income_name]

    def adjust_income(self, income_name, field, new_value):
        # adjust a field of an income by IncomeID
        self.df.loc[self.df['Income Name'] == income_name, field] = new_value

    def sum_amounts(self):
        # sum the Amount column
        return self.df['Amount'].sum()

    def get_incomes(self):
        # return the DataFrame
        return self.df

    def clear_incomes(self):
        # clear the DataFrame
        self.df = pd.DataFrame(columns=['Income Name', 'Account Name', 'Amount', 'Month'])

class BankAccount:
    def __init__(self):
        # create an empty DataFrame with the specified fields
        self.df = pd.DataFrame(columns=['Account Name', 'Owner', 'Bank Name', 'Account Type', 'Account Balance', 'Purpose'])

    def _set_accounts(self, df):
        self.df = df

    def get_accounts(self):
        # return the DataFrame
        return self.df
    
    def get_bills(self):
        return self.bills

    def get_incomes(self):
        return self.incomes

    def add_account(self, account_name, owner, bank_name, account_type, account_balance, purpose):
        # create a new DataFrame with the account information
        new_account = pd.DataFrame({'Account Name': [account_name],
                                    'Owner': [owner], 
                                    'Bank Name': [bank_name],
                                    'Account Type': [account_type], 
                                    'Account Balance': [account_balance], 
                                    'Purpose': [purpose]})
        # add the new DataFrame to the existing DataFrame using pd.concat
        self.df = pd.concat([self.df, new_account])

    def remove_account(self, account_name):
        # remove an account from the DataFrame by AccID
        self.df = self.df[self.df['Account Name'] != account_name]

    def adjust_account(self, account_name, field, new_value):
        # adjust a field of an account by AccID
        self.df.loc[self.df['Account Name'] == account_name, field] = new_value

    def sum_balances(self):
        # sum the Account Balance column
        return self.df['Account Balance'].sum()
    
    def update_accounts(self, bill_table: Bill, income_table: Income):
        if bill_table is None and income_table is None:
            print('accounts are either up-to-date or\
                 there are no bills or incomes to update')
        else:
            if income_table is not None:
                if income_table.used:
                    print('income table has already been used')
                else:
                    for index, row in income_table.df.iterrows():
                        # get the AccID and Amount for the current income
                        acc_name = row['Account Name']
                        amount = row['Amount']
                        # adjust the balance of the corresponding account
                        self.df.loc[self.df['Account Name'] == acc_name, 'Account Balance'] += amount
                    INCOMES.append(income_table)
                    #income_table.clear_incomes()
                    print('incomes are up-to-date')
                    income_table.used = True
                
            if bill_table is not None:
                if bill_table.used:
                    print('bill table has already been used')
                else:
                    for index, row in bill_table.df.iterrows():
                        # get the AccID and Amount for the current bill
                        acc_name = row['Account Name']
                        amount = row['Amount']
                        # adjust the balance of the corresponding account
                        self.df.loc[self.df['Account Name'] == acc_name, 'Account Balance'] -= amount
                    BILLS.append(bill_table)
                    #bill_table.clear_bills()
                    print('bills are up-to-date')
                    bill_table.used = True
                

class Timeline:
    def __init__(self):
        # create an empty DataFrame with the specified fields and indexes
        self.df = pd.DataFrame()
        self.bank_accounts = {}

    def _set_df(self, df):
        self.df = df
        
    def get_timeline(self):
        # return the DataFrame
        return self.df

    def get_all_bank_accounts(self):
        return self.bank_accounts
    
    def configure_bank_accounts(self, final_bankaccounts: BankAccount):
        final_accs = final_bankaccounts.get_accounts()
        for col in self.df.columns:
            bank_accounts = self.df.loc[self.df[col].notna(), col][:-1]
            # get index of bank accounts
            bank_accounts = bank_accounts.index.tolist()
            #retrieve rows from final_accs where Account Name is in bank_accounts
            bank_accounts = final_accs[final_accs['Account Name'].isin(bank_accounts)]
            self.bank_accounts[col] = bank_accounts
        
    def update_timeline(self, month, year, bank_account: BankAccount):
        # get the account names and balances from the bank_account object
        self.bank_accounts[f'{month}/{year}'] = bank_account
        bank_account = bank_account.get_accounts()
        account_names = bank_account['Account Name'].tolist()
        balances = bank_account['Account Balance'].tolist()

        for i in range(len(account_names)):
            if account_names[i] not in self.df.index:  # for initialization or new accounts 
                # create a new DataFrame with the timeline information
                new_timeline = pd.DataFrame({f'{month}/{year} Balance (CAD)': [round(balances[i],2)]}, index=[account_names[i]])
                # add the new DataFrame to the existing DataFrame using pd.concat
                self.df = pd.concat([self.df, new_timeline])
            else:
                # update the timeline DataFrame
                self.df.loc[account_names[i], f'{month}/{year} Balance (CAD)'] = round(balances[i],2)
        #add total index where the total balance of all accounts is stored
        if 'Total' not in self.df.index:
            self.df.loc['Total'] = 0
        self.df.loc['Total', f'{month}/{year} Balance (CAD)'] = bank_account['Account Balance'].sum()

        

    def save_timeline(self, file_path):
        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        
        #generate all bills and incomes dataframes
        bills_df = pd.DataFrame()
        incomes_df = pd.DataFrame()
        accounts_df = pd.DataFrame(columns=['Account Name', 'Owner', 
                                            'Bank Name', 'Account Type', 
                                            'Account Balance', 'Purpose'])
        for bill in BILLS:
            bill_df = bill.get_bills()
            bills_df = pd.concat([bills_df, bill_df])
        for income in INCOMES:
            income_df = income.get_incomes()
            incomes_df = pd.concat([incomes_df, income_df])

        for period in self.bank_accounts:
            new_df = self.bank_accounts[period].get_accounts()
            print(new_df)
            print('---')
            accounts_df = pd.merge(accounts_df,new_df,on=['Account Name', 'Owner', 
                                                          'Bank Name', 'Account Type', 
                                                          'Account Balance', 'Purpose'], how='outer')
        
        

        self.df.to_excel(writer, index=True, sheet_name='Timeline', startrow=0, startcol=0)
        bills_df.to_excel(writer, index=True, sheet_name='Bills', startrow=0, startcol=0, header=True)
        accounts_df.to_excel(writer, index=True, sheet_name='Up-to-date Accounts', startrow=0, startcol=0, header=True)
        incomes_df.to_excel(writer, index=True, sheet_name='Incomes', startrow=0, startcol=0, header=True)

        writer.save()





#function to continue a Timeline session
def continue_session(time_line_file) -> Timeline:
    #read in the timeline file
    time_line_df = pd.read_excel(time_line_file, sheet_name='Timeline', index_col=0)
    bills_df = pd.read_excel(time_line_file, sheet_name='Bills', index_col=0)
    incomes_df = pd.read_excel(time_line_file, sheet_name='Incomes', index_col=0)
    accounts_df = pd.read_excel(time_line_file, sheet_name='Up-to-date Accounts', index_col=0)

    t = Timeline()
    t._set_df(time_line_df)
    #create a bank account object
    ba = BankAccount()
    ba._set_accounts(accounts_df)

    #create bill and income objects
    BILLS=[bills_df]
    INCOMES=[incomes_df]

    # append to t.bank_accounts
    t.configure_bank_accounts(ba)
    print('---Summary of Continuation--')

    print('Timeline')
    print(t.get_timeline())
    print('Bills')
    print(BILLS)
    print('Incomes')
    print(INCOMES)
    print('Bank Accounts')
    print(t.get_all_bank_accounts())
    print('---End of Summary---')

    
    

if __name__ == '__main__':

    # # create an instance of the BankAccount class
    # ba = BankAccount()

    # # add some accounts
    # ba.add_account('Account 1', 'Bob', 'Bank 1', 'Checking', 1000, 'Personal')
    # ba.add_account('Account 2', 'Alice', 'Bank 1', 'Savings', 2000, 'Business')
    # ba.add_account('Account 3', 'Bobby', 'Bank 2', 'Checking', 3000, 'Personal')

    # t = Timeline()
    # t.update_timeline('March', 2020, ba)
    # timeline = t.get_timeline()
    # print('before bill & income',timeline)

    # b = Bill()
    # b.add_bill('Bill 3', 'Account 1', 300, 'April')
    # i = Income()
    # i.add_income('Income 3', 'Account 1', 500, 'April')
    # print('-----------------------------------------')

    # ba.update_accounts(b, i)

    # t.update_timeline('April', 2020, ba)
    # timeline2 = t.get_timeline()
    # print(timeline2)

    # print('++++++++++++++++++++++Save_timeline++++++++++++++++++++++++')
    # t.save_timeline('/Users/baoha/Desktop/Automation Script/Budget_Tracking/src/test2.xlsx')

   print('open an existing session')
   continue_session('/Users/baoha/Desktop/Automation Script/Budget_Tracking/src/test2.xlsx')