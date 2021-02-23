#----------------------------------------------------------------------------------
import pandas as pd 
import streamlit as st  # streamlit run _Convert_MISReport2021_CSV.py
import altair as alt
import Function1 as F1
import sys 
import time
import os
import dateutil
#----------------------------------------------------------------------------------
st.set_page_config(page_title='MIS Analize', page_icon="https://raw.githubusercontent.com/zheewin/PicDATA/master/Man1.jpg", layout='centered', initial_sidebar_state='auto')
#----------------------------------------------------------------------------------
def RunAdmin():
    st.write('Admin')
    datafile = st.file_uploader("Upload xls",type=['xls'])
    if datafile is not None:
        F1.save_uploadedfile(datafile)

        if datafile is not None:
            FileData=r'MIS_Data.xls'
            x = ['Actual2021','Actual2020']
            df= F1.Area_Wide_Long_AreaCompanyDate(FileData,x)
            df.to_csv(r'Data/ActualProduction_ACDx2_L.csv', index = False, header=True)
            st.success("Uploaded Data:{} OK".format('Area_W_L_AreaCompanyDate2X.csv'))
            #----------------------------------------------------------------------------------
            #----------------------------------------------------------------------------------


    FileData=r'MISReport2021.xls'
    x = ['LOSS_总损耗',
        'PELLET_颗粒料产量',
        'MIXER_混合机（理论）产量',
        'PERFORMANCE_吨人月',
        '劳务工_LABOUR',
        '正式工_STAFF',
        'ELECTRIC_CONSUMPTION',
        'ALL_WAGE_EXPENSE',
        'MASH_BAG_EXPENSE',
        'PELLET_BAG_EXPENSE',
        'TOTAL_EXPENSE_总制造费用',
        'OTHERS_EXPENSE_其它生产费用',
        'FACTORY_EXPENSE_直接制造费用',
        'VARIABLE_EXPENSE_变动费用',
        'PRODUCTION_AV_LastY',
        'PRODUCTION_YearPlan',
        'PRODUCTION_All',
        'PRODUCTION_PELLET',
        'PRODUCTION_2021Cap',
        'PRODUCTION_2020',
        ]
    df= F1.Area_Wide_Long_AreaCompanyDate_Code(FileData,x)

    df.to_csv(r'Data/MISReport2021.csv', index = False, header=True)
    st.success("Uploaded Data:{} OK".format('MISReport2021.csv'))
    print("Uploaded Data:{} OK".format('MISReport2021.csv'))




#----------------------------------------------------------------------------------

def LogIn():
    Password1placeholder = st.sidebar.empty()
    btnLogInplaceholder = st.sidebar.empty()
    btnLogOutplaceholder = st.sidebar.empty()

    Password1 = Password1placeholder.text_input('Enter a password',type='password')
    btnLogIn = btnLogInplaceholder.checkbox("Log in")
    btnLogOut = btnLogOutplaceholder.button('Log Out',key=1)

    if btnLogOut:
        Password1 = Password1placeholder.text_input('Enter a password',type='password', value='',key=1)
        btnLogIn = btnLogInplaceholder.checkbox("Log in",key=1)
        Password1placeholder.empty()
        btnLogInplaceholder.empty()
        btnLogOutplaceholder.empty()

        st.success('Logged Out.')
        st.button("Re Sign-In")

        # st.stop()

    if btnLogIn:
        if Password1=='333':
            st.success('Logged in.') 
        #     RunProg()
        elif  Password1=='444':
            st.success('Logged in.') 
            RunAdmin()
        else:
            st.error('Incorrect username or password')
#----------------------------------------------------------------------------------

# LogIn()
RunAdmin()

