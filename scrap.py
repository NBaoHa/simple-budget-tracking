import pandas as pd

# create three sample DataFrames
df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df2 = pd.DataFrame({'C': [7, 8, 9], 'D': [10, 11, 12]})
df3 = pd.DataFrame({'E': [13, 14, 15], 'F': [16, 17, 18]})

# save each DataFrame to a separate sheet in an Excel spreadsheet

writer = pd.ExcelWriter('/Users/baoha/Desktop/Automation Script/Budget_Tracking/src/ttt.xlsx', engine='xlsxwriter')

df1.to_excel(writer, index=False, sheet_name='Sheet1')
df2.to_excel(writer, index=False, sheet_name='Sheet2', startrow=0, startcol=0, header=False)
df3.to_excel(writer, index=False, sheet_name='Sheet3', startrow=0, startcol=0, header=False)

writer.save()