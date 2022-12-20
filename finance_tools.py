import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from pandastable import Table, TableModel

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


# Monthly budget
class Monthly_finance:
    ''' per month budget object'''
    def __init__(self, Monthlyid: int, files_folder: str, saved_amount: int = 0):
        # parameters table
        self.members = pd.DataFrame()
        self.bills = pd.DataFrame()
        self. Expenses = pd.DataFrame()

        # output values to return records
        self.Monthlyid = Monthlyid
        self.Total_income = 0
        self.Total_bills = 0
        self.Total_expenses = 0
        self.Net_income = 0
        self.percent_savings = 0 # needs to be calculated based on desired savings
        

        # compute output values
        self.add_members(files_folder + '/members.txt')
        self.add_bills(files_folder + '/bills.txt')
        self.add_expenses(files_folder + '/expenses.txt')
        self.calculate_net_income()
        

        # calculate percent savings
        self.calculate_percent_savings(saved_amount)
        # output table
        self.output = pd.DataFrame({'Monthlyid': [self.Monthlyid],
                                    'Total_income': [self.Total_income], 
                                    'Total_bills': [self.Total_bills], 
                                    'Total_expenses': [self.Total_expenses],
                                    'Net_income': [self.Net_income], 
                                    'percent_savings': [self.percent_savings],
                                    'remaining_spare': [self.Net_income-(self.Net_income * self.percent_savings)]})
        
        
        # results
        #self.view_results()


    # output table
    def view_results(self):
        print('',self.output, '', sep='\n')

    def return_values(self):
        return self.output

    # methods
    def add_members(self, members_txtfle):
        with open(members_txtfle, 'r') as f:
            for line in f:
                name = line.split()[0]
                income = int(line.split()[1])
                new_row = pd.Series({'name': name, 'income': income})
                self.members = pd.concat([self.members, new_row.to_frame().T], ignore_index=True)
        
        self.Total_income = self.members['income'].sum()
                
    def add_bills(self, bills_txtfle):
        with open(bills_txtfle, 'r') as f:
            for line in f:
                name = line.split()[0]
                amount = int(line.split()[1])
                new_row = pd.Series({'name': name, 'amount': amount})
                self.bills = pd.concat([self.bills, new_row.to_frame().T], ignore_index=True)
        
        self.Total_bills = self.bills['amount'].sum()
    
    def add_expenses(self, expenses_txtfle):
        with open(expenses_txtfle, 'r') as f:
            for line in f:
                name = line.split()[0]
                amount = int(line.split()[1])
                new_row = pd.Series({'name': name, 'amount': amount})
                self.Expenses = pd.concat([self.Expenses, new_row.to_frame().T], ignore_index=True)
        
        self.Total_expenses = self.Expenses['amount'].sum()

        
    def calculate_net_income(self):
        self.Net_income = self.Total_income - self.Total_bills - self.Total_expenses
        return self.Net_income

    def calculate_percent_savings(self, amount_saved):
        self.percent_savings = amount_saved / self.Net_income
        return self.percent_savings
    
    def getID(self):
        return self.Monthlyid

    def getMembers(self, field=None):
        if field is not None:
            return self.members[[field]]
        else:
            return self.members

    
    def getBills(self, field=None):
        if field is not None:
            return self.bills[[field]]
        else:
            return self.bills
    
    def getExpenses(self, field=None):
        if field is not None:
            return self.Expenses[[field]]
        else:
            return self.Expenses



class Asset:
    def __init__(self):
        self.TFSA = pd.DataFrame()
        self.RRSP = pd.DataFrame()
        self.Savings = pd.DataFrame()
    

class Timeline_budget:
    def __init__(self):
        self.timeline = pd.DataFrame({'Monthlyid': [], 
                                      'Total_income': [], 
                                      'Net_income': [], 
                                      'percent_savings': [], 
                                      'remaining_spare': []})

        # default values                              
        self.total_income = 0
        self.total_net_income = 0
        self.total_bills = 0
        self.total_expenses = 0
        self.total_savings = 0
        self.total_spare = 0
    
        self.realistic_income_existing = 0


        # storage
        self.monthly_records = {}

    def initate_existing_networth(self, networth: float):
        self.realistic_income_existing = networth
    
    def add_outsider_funds(self, amount: float):
        self.realistic_income_existing += amount

    def add_month(self, Monthly_item: pd.DataFrame):
        new_input = Monthly_item[["Monthlyid", "Total_income", "Net_income", "percent_savings", "remaining_spare"]]
        self.realistic_income_existing += Monthly_item['Net_income'].values[0]
        self.timeline = pd.merge(self.timeline, Monthly_item, how='outer')
        
    def retrieve_month_record(self, month_id):
        return self.monthly_records[month_id]

    def add_month_pkg(self, folder_dir, savings_permonth=0):
        year = folder_dir.split('/')[-1]
        for file in os.listdir(folder_dir):
            subfolder = f'{folder_dir}/{file}'
            month_id = int(year + Month_id_dict[file])
            Monthly_item = Monthly_finance(month_id, subfolder, saved_amount=savings_permonth)
            self.monthly_records[month_id] = Monthly_item
            self.add_month(Monthly_item.return_values())

    
            
    def get_pie_chart(self):
        # show pie chart representing the  total_bills, total_expenses, percent_savings, remaining_spare from Total_income
        # pie chart
        labels = ['total bills', 'total expenses', 'savings', 'remaining spare']
        sizes = [self.total_bills, 
                self.total_expenses, 
                self.total_savings, 
                self.total_spare] 
        explode = (0, 0, 0, 0.2)  # only "explode" the 4th slice (i.e. 'Hogs')
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=0)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Finance Breakdown')
        
        return fig1

    def get_stats(self):
        self.total_income = self.timeline['Total_income'].sum()
        self.total_net_income = self.timeline['Net_income'].sum()
        self.total_bills = self.timeline['Total_bills'].sum()
        self.total_expenses = self.timeline['Total_expenses'].sum()
        self.total_savings = self.timeline['Net_income'].sum() - self.timeline['remaining_spare'].sum()
        self.total_spare = self.timeline['remaining_spare'].sum()

        return (f'Total_income: {self.total_income}\n\
            Total_net_income: {self.total_net_income} \n\
            Total_bills: {self.total_bills} \n\
            Total_expenses: {self.total_expenses} \n\
            Total_savings: {self.total_savings} \n\
            Total_remaining_spare: {self.total_spare} \n\
            REALISTIC NETWORTH {self.realistic_income_existing} \n\
            REALISTIC SPARE {self.realistic_income_existing - self.total_savings}'.replace('            ', ''))
    
    def getAvg(self, field):
        return self.timeline[field].mean()

    def replicate_period(self,time):
        print(f'-------replicate {time}-------\n')
        print(f'Total_income: {self.total_income*time}',
            f'Total_net_income: {self.total_net_income*time}',
            f'Total_bills: {self.total_bills*time}', 
            f'Total_expenses: {self.total_expenses*time}',
            f'Total_savings: {self.total_savings*time}',
            f'Total_remaining_spare: {self.total_spare*time}',sep='\n')
        
    def get_timeline(self):
        # sort self.timeline by Monthlyid
        self.timeline = self.timeline.sort_values(by=['Monthlyid'])
        # print('||-----------------------Timeline------------------------||',
        # self.timeline,
        # '||--------------------------------------------------------||', 
        # sep='\n \n \n')
        return self.timeline





class Cam_input:
    '''Use text recognition to input the data from the picture'''
    def __init__(self):
        pass

    def get_text(self, img_path):
        # get the text from the picture
        pass



if __name__ == "__main__":
    ## test
    timeline = Timeline_budget()
    timeline.initate_existing_networth(35000)
    timeline.add_month_pkg('/home/bao_wy/Documents/Start_up_dev/Finance_tracking/2023', 1000)
    timeline.add_outsider_funds(300000)
    frame = timeline.get_timeline()
    g = timeline.get_stats()
    chart = timeline.get_pie_chart()
    
    print(frame, chart, g)

    

    ## replicate Period 
    # timeline.replicate_period(2)

    ## retive month record
    #Jan = timeline.retrieve_month_record(202301)
    #print(Jan.getMembers())
    
    # avg_income = timeline.getAvg('Net_income')
    # print(f'Average income: {avg_income}')
