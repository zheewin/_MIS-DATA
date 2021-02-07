#----------------------------------------------------------------------------------
#   Doing CSV DATA _Excel-CSV.py
#----------------------------------------------------------------------------------
import pandas as pd  # python _excel-csv.py
import streamlit as st  #streamlit run _Excel-CSV.py
import Function1 as F1
#----------------------------------------------------------------------------------
FileData=r'MIS_Data.xls'
x = ['1总产量颗粒料产量'
    ]
df= F1.Area_Wide_Long_AreaCompanyDate(FileData,x)
df.to_csv(r'Data/Area_Wide_Long_AreaCompanyDate.csv', index = False, header=True)
#----------------------------------------------------------------------------------
x = ['1产量']
df= F1.YearMonthValue(FileData,x)
df.to_csv(r'Data/YearMonthVarValue.csv', index = False, header=True)

#----------------------------------------------------------------------------------
x = ['2KPI']
df= F1.YearMonthValue(FileData,x)
df.to_csv(r'Data/2KPI.csv', index = False, header=True)

#----------------------------------------------------------------------------------
x = ['3Cap','3Actual']
df= F1.YearMonthVarValue(FileData,x)
df.to_csv(r'Data/3ActualCap.csv', index = False, header=True)

#----------------------------------------------------------------------------------
x = '4FeedMill'
df=pd.read_excel(open(FileData, 'rb'), sheet_name=x)
df.to_csv(r'Data/4FeedMill.csv', index = False, header=True)

#----------------------------------------------------------------------------------

#----------------------------------------------------------------------------------



