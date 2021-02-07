#----------------------------------------------------------------------------------
import pandas as pd 
import streamlit as st  # streamlit run 0.py
import altair as alt
import Function1 as F1
import Function2KPI as F2KPI
import sys 
import time
import os
import dateutil
#----------------------------------------------------------------------------------
df=pd.read_csv("Data/Area_Wide_Long_AreaCompanyDate.csv")
df1=pd.read_csv("Data/YearMonthVarValue.csv")
df_2KPI=pd.read_csv("Data/2KPI.csv")
df_3ActualCap=pd.read_csv("Data/3ActualCap.csv")
df_4FeedMill=pd.read_csv("Data/4FeedMill.csv")
df_1CapActual2021=pd.read_csv("Data/1CapActual2021.csv")
#----------------------------------------------------------------------------------
st.set_page_config(page_title='MIS Analize', page_icon="https://www.flaticon.com/svg/vstatic/svg/4150/4150647.svg?token=exp=1612605999~hmac=b02b5040f38bc7b4e348f2e35280e3b8", layout='centered', initial_sidebar_state='auto')

def SideBar():
    st.sidebar.header('User Input Features')
    global  Area,Month,df_Month
    Area = st.sidebar.selectbox('Area', sorted(df['Area'].unique()))
    Month = st.sidebar.selectbox('Month', sorted(pd.DatetimeIndex(df['Date']).month.unique()))
    df_Month= df[ (pd.DatetimeIndex(df['Date']).month==Month) ]
#---------------------------------------------------------------------------------- Black Table
def item1():
    st.header(' %s月份 Nationwide data 2020' %(Month)) 
    # #----------------------------------------
    DataFrame1 ={'Production(Ton)':[''],'ACCUM':[''],'%UTILIZE':[''],'SALE-OUT':['61%'],'GROWTH-YOY':['']}
    #----------------------------------------------------------------------------------
    DataFrame1['Production(Ton)']=  "{0:,.0f}".format(df_Month['ValueAll'].sum())
    DataFrame1['ACCUM']= "{0:,.0f}".format(df['ValueAll'].sum())
    #----------------------------------------------------------------------------------
    Month2020=df1['ValueAll'][  (df1['Year']=='2020年') & (pd.DatetimeIndex(df1['Date']).month==Month) ]
    Month2019=df1['ValueAll'][  (df1['Year']=='2019年') & (pd.DatetimeIndex(df1['Date']).month==Month) ]
    GrowthYOY = (float(Month2020)-float(Month2019))/float(Month2019)
    DataFrame1['GROWTH-YOY']= "{0:,.2%}".format(GrowthYOY)
    #----------------------------------------------------------------------------------
    DataFrame1=pd.DataFrame(DataFrame1)
    st.table(DataFrame1.style.set_properties(**{ 'background-color': 'black','color': 'lawngreen','border-color': 'white'}))
    #----------------------------------------------------------------------------------
def item1a():
    st.header(' %s月份 Nationwide data 2021' %(Month)) 
    # DataFrame2.iloc[2,0]='PRODUCTIVITY= %s' % (TMMonth180)

    df_1CapActual2021_Area_Month=df_1CapActual2021[  (df_1CapActual2021['Area']==Area) & (pd.DatetimeIndex(df_1CapActual2021['Date']).month==Month)  ]
    df_1Actual2021_Month=df_1CapActual2021[  (pd.DatetimeIndex(df_1CapActual2021['Date']).month==Month) & (df_1CapActual2021['VarAll']=='1Actual2021') ]
    df_1Actual2021=df_1CapActual2021[  (df_1CapActual2021['VarAll']=='1Actual2021') ]
    # #----------------------------------------
    DataFrame1 ={'Production(Ton)':[''],'ACCUM':[''],'%UTILIZE':[''],'SALE-OUT':[''],'GROWTH-YOY':['']}
    #----------------------------------------------------------------------------------
    DataFrame1['Production(Ton)']=  "{0:,.0f}".format(df_1Actual2021_Month['ValueAll'].sum())
    DataFrame1['ACCUM']= "{0:,.0f}".format(df_1Actual2021['ValueAll'].sum())
      #----------------------------------------------------------------------------------
    Actual_Month=(df_1CapActual2021['ValueAll'][  (pd.DatetimeIndex(df_1CapActual2021['Date']).month==Month) & (df_1CapActual2021['VarAll']=='1Actual2021')  ].sum())
    Cap_Month=(df_1CapActual2021['ValueAll'][  (pd.DatetimeIndex(df_1CapActual2021['Date']).month==Month) & (df_1CapActual2021['VarAll']=='1Cap2021')  ].sum())
    Utilize=Actual_Month/Cap_Month
    DataFrame1['%UTILIZE']= "{0:,.2%}".format(Utilize)
    #----------------------------------------------------------------------------------
    Month2021=df1['ValueAll'][  (df1['Year']=='2021年') & (pd.DatetimeIndex(df1['Date']).month==Month) ]
    Month2020=df1['ValueAll'][  (df1['Year']=='2020年') & (pd.DatetimeIndex(df1['Date']).month==Month) ]
    GrowthYOY = (float(Month2021)-float(Month2020))/float(Month2020)
    DataFrame1['GROWTH-YOY']= "{0:,.2%}".format(GrowthYOY)
    #----------------------------------------------------------------------------------
    DataFrame1=pd.DataFrame(DataFrame1)
    st.table(DataFrame1.style.set_properties(**{ 'background-color': 'black','color': 'lawngreen','border-color': 'white'}))
#---------------------------------------------------------------------------------- KPI
def item2():
    st.header('2020-%s月份 KPI' %(Month) ) 


    DataFrame2 ={'0':['VC','LOSS','PRODUCTIVITY'],
                '1':['GASS CONSUMPTION','UNQUALITIED PRODUCT','MAJOR ACCIDENT'],
                '2':['STANDARD FACTORY','INNOVATION PROJECT','CONSTRUCTION MAJOR ACCIDENT']}
    DataFrame2=pd.DataFrame(DataFrame2)
    df=df_2KPI
    #---------------------------
    VC45=float(df['ValueAll'][  (df['Year']=='VC45') & (pd.DatetimeIndex(df['Date']).month==Month) ])
    DataFrame2.iloc[0,0]='VC= %s' % (VC45)

    SHRINKAGE043=float(df['ValueAll'][  (df['Year']=='SHRINKAGE043') & (pd.DatetimeIndex(df['Date']).month==Month) ])
    DataFrame2.iloc[1,0]='LOSS= %s' % (SHRINKAGE043)

    TMMonth180=float(df['ValueAll'][  (df['Year']=='TMMonth180') & (pd.DatetimeIndex(df['Date']).month==Month) ])
    DataFrame2.iloc[2,0]='PRODUCTIVITY= %s' % (TMMonth180)
    #---------------------------
    GAS45=float(df['ValueAll'][  (df['Year']=='GAS45') & (pd.DatetimeIndex(df['Date']).month==Month) ])
    DataFrame2.iloc[0,1]='GASS CONSUMPTION= %s' % (GAS45)

    UnQualified003=float(df['ValueAll'][  (df['Year']=='UnQualified003') & (pd.DatetimeIndex(df['Date']).month==Month) ])
    DataFrame2.iloc[1,1]='UNQUALITIED PRODUCT= %s' % (UnQualified003)

    MASH85=float(df['ValueAll'][  (df['Year']=='MASH85') & (pd.DatetimeIndex(df['Date']).month==Month) ])
    DataFrame2.iloc[2,1]='MAJOR ACCIDENT= %s' % (MASH85)

    #---------------------------
    # GAS45=float(df['ValueAll'][  (df['Year']=='GAS45') & (pd.DatetimeIndex(df['Date']).month==Month) ])
    # DataFrame2.iloc[0,2]='GASS CONSUMPTION= %s' % (GAS45)

    InnoQuarter246=float(df['ValueAll'][  (df['Year']=='InnoQuarter246') & (pd.DatetimeIndex(df['Date']).month==Month) ])
    DataFrame2.iloc[1,2]='INNOVATION PROJECT= %s' % (InnoQuarter246)

    # MASH85=float(df['ValueAll'][  (df['Year']=='MASH85') & (pd.DatetimeIndex(df['Date']).month==Month) ])
    # DataFrame2.iloc[2,2]='MAJOR ACCIDENT= %s' % (MASH85)

    #---------------------------

    def hl(x):
        r = 'background-color: red'
        g = 'background-color: lawngreen'
        y = pd.DataFrame('', index=x.index, columns=x.columns)
        # zw= 'border: solid' 'background-color: red'

        STD1=45
        c = g if VC45 <= STD1 else r
        y.iloc[0, 0] = c

        STD1=0.43
        c = g if SHRINKAGE043 <= STD1 else r
        y.iloc[1, 0] = c

        STD1=180
        c = g if TMMonth180 >= STD1 else r
        y.iloc[2, 0] = c
        #---------------------------
        STD1=4.5
        c = g if GAS45 <= STD1 else r
        y.iloc[0, 1] = c


        STD1=0.03
        c = g if UnQualified003 <= STD1 else r
        y.iloc[1, 1] = c

        STD1=85
        c = g if MASH85 <= STD1 else r
        y.iloc[2, 1] = c
        #---------------------------
        # STD1=4.5
        # c = g if GAS45 <= STD1 else r
        # y.iloc[0, 2] = c


        STD1=246
        c = g if InnoQuarter246 >= STD1 else r
        y.iloc[1, 2] = c

        # STD1=85
        # c = g if MASH85 <= STD1 else r
        # y.iloc[2, 2] = c

        return y

    def color_negative_values(val):
        return  'width: auto;border: 1mm ridge rgba(50, 50, 220, .6); border-width: 4px ; border-radius: 12px'

    df= DataFrame2.style.applymap(color_negative_values).apply(hl, axis=None)

    # df= DataFrame2.style.apply(hl, axis=None).applymap(hl)
    # df= DataFrame2.style.apply(lambda x: fLessSTDG(x,STD1, VC45,0,0), axis=None)
    # st.table(DataFrame1.style.set_properties(**{ 'background-color': 'black','color': 'lawngreen','border-color': 'white'}))
    st.table(df)

    #-------------------
#---------------------------------------------------------------------------------- Chart
def item3():
    #---------------------------------- Bar1 
    def Bar10Year():
        ShowAll=st.button('全国 10年')
        if ShowAll:
            Title1= 'Nationwide Actual/Cap' 
            df_3ActualCap_Month= df_3ActualCap
        else:
            Title1= '%s 月份 Actual/Cap' %(Month)
            df_3ActualCap_Month= df_3ActualCap[ (pd.DatetimeIndex(df_3ActualCap['Date']).month==Month) ]
        plot= alt.Chart(df_3ActualCap_Month).mark_bar(opacity=0.7
            ).encode(
                alt.X('Year:N', axis=alt.Axis(labelFontSize=13)),
                alt.Y('sum(ValueAll):Q', stack=None, axis=alt.Axis(labelFontSize=15,title='Unit: 1000Ton')),
                color=alt.Color('VarAll:N'),
            ).configure_axis(
                labelFontSize=15,
                titleFontSize=15
            ).configure_title(
                fontSize=24
            ).properties(
                title="%s" %(Title1),
                height=400,width=600
            ).configure_axisX(
                labelAngle=-45,
            ).configure_legend(
                titleColor='black', 
                titleFontSize=15,
                labelFontSize=15,
            )
        st.write(plot)
    Bar10Year()
    #---------------------------------- Bar2
    def Bar2021():
        ShowAll=st.button('全国 2021')
        if ShowAll:
            Title1= 'Actual/Cap 2021 Nationwide' 
            df_1CapActual2021_Area= df_1CapActual2021
        else:
            Title1= "Actual/Cap 2021 %s" %Area
            df_1CapActual2021_Area= df_1CapActual2021[  (df_1CapActual2021['Area']==Area) ]
        plot= alt.Chart(df_1CapActual2021_Area).mark_bar(opacity=0.7
            ).encode(
                alt.X('month(Date):N', axis=alt.Axis(labelFontSize=13)),
                alt.Y('sum(ValueAll):Q', stack=None, axis=alt.Axis(labelFontSize=15,title='Unit: Ton')),
                color=alt.Color('VarAll:N'),
            ).configure_axis(
                labelFontSize=15,
                titleFontSize=15
            ).configure_title(
                fontSize=24
            ).properties(
                title= Title1 ,
                height=400,width=600
            ).configure_axisX(
                labelAngle=-45,
            ).configure_legend(
                titleColor='black', 
                titleFontSize=15,
                labelFontSize=15,
            )
        st.write(plot)
    Bar2021()
    #---------------------------------- Line 2021 vs 2020
    def Line2020_2021():
        df_3Actual_Year2020= df_3ActualCap[ (df_3ActualCap['VarAll']=='3Actual') & (df_3ActualCap['Year']==2020) ]
        df_3Actual_Year2020["Date"] = df_3Actual_Year2020["Date"].apply(lambda x: dateutil.parser.parse(x))
        df_3Actual_Year2020['Month'] = df_3Actual_Year2020['Date'].dt.month
        df_3Actual_Year2020['2020'] = df_3Actual_Year2020['ValueAll']*1000
        df_3Actual_Year2020=df_3Actual_Year2020[['Date','Month','2020']].reset_index()
        df_3Actual_Year2020=df_3Actual_Year2020[['Date','Month','2020']]
        # st.write(df_3Actual_Year2020)

        df_3Actual_Year2021=(df_1CapActual2021[  (df_1CapActual2021['VarAll']=='1Actual2021') ])
        df_3Actual_Year2021["Date"] = df_3Actual_Year2021["Date"].apply(lambda x: dateutil.parser.parse(x))
        df_3Actual_Year2021['Month'] = df_3Actual_Year2021['Date'].dt.month
        df_3Actual_Year2021=df_3Actual_Year2021.groupby(by=["Month"]).sum().reset_index()
        df_3Actual_Year2021['2021'] = df_3Actual_Year2021['ValueAll']
        df_3Actual_Year2021=df_3Actual_Year2021[['Month','2021']]
        # st.write(df_3Actual_Year2021)

        df_3Actual_Year = pd.merge(df_3Actual_Year2020,df_3Actual_Year2021,on ='Month',how ='inner') 
        df_3Actual_Year = df_3Actual_Year.melt(id_vars=['Date','Month'], var_name=['VarAll'], value_name='ValueAll')
        # st.write(df_3Actual_Year)

        st.write(F1.Company_markLine(df_3Actual_Year,'2021 vs 2020 Production','Unit: Ton'))
    Line2020_2021()
    #---------------------------------- markLine 10 Year
    def Line10Year():
        df_3Actual_Year= df_3ActualCap[ (df_3ActualCap['VarAll']=='3Actual') ]
        st.write(F1.markLine_Month_ValueAll_legend(df_3Actual_Year,'10 Years Production','Unit: 1000 Ton'))
    Line10Year()

#---------------------------------------------------------------------------------- Black Table
def item4():
    DataFrame1 ={'FeedMill':['0'],'Building':['0']}
    DataFrame1['FeedMill']=df_4FeedMill['ValueAll'][  (df_4FeedMill['Year 2021']=='Feedmill') & (df_4FeedMill['VarAll']=='ACTIVE')]

    Build1=str(df_4FeedMill['ValueAll'][  (df_4FeedMill['Year 2021']=='building') ].sum())
    Active1=str(df_4FeedMill['ValueAll'][  (df_4FeedMill['Year 2021']=='building') &  (df_4FeedMill['VarAll']=='ACTIVE') ].sum())
    Stop1=str(df_4FeedMill['ValueAll'][  (df_4FeedMill['Year 2021']=='building') &  (df_4FeedMill['VarAll']=='STOP') ].sum())

    DataFrame1['Building']=str(Build1) + ' ( Active=' + str(Active1) + ' Stop='+str(Stop1)+' )' 

    DataFrame1=pd.DataFrame(DataFrame1)
    st.table(DataFrame1.style.set_properties(**{ 'background-color': 'black','color': 'lawngreen','border-color': 'white'}))
#----------------------------------------------------------------------------------
def RunProg():
    SideBar()
    F1.cut1td()
    item1()
    item1a()
    item2()
    item3()
    item4()
def RunAdmin():
    st.write('Admin')
    datafile = st.file_uploader("Upload xls",type=['xls'])
    if datafile is not None:
        F1.save_uploadedfile(datafile)

        if datafile is not None:
            FileData=r'MIS_Data.xls'
            x = ['1总产量颗粒料产量'
                ]
            df= F1.Area_Wide_Long_AreaCompanyDate(FileData,x)
            df.to_csv(r'Data/Area_Wide_Long_AreaCompanyDate.csv', index = False, header=True)
            st.success("Uploaded Data:{} OK".format('Area_Wide_Long_AreaCompanyDate.csv'))
            #----------------------------------------------------------------------------------
            x = ['1产量']
            df= F1.YearMonthValue(FileData,x)
            df.to_csv(r'Data/YearMonthVarValue.csv', index = False, header=True)
            st.success("Uploaded Data:{} OK".format('YearMonthVarValue.csv'))
            #----------------------------------------------------------------------------------
            x =  ['1Cap2021','1Actual2021']
            df= F1.Area_Wide_Long_AreaCompanyDate(FileData,x)
            df.to_csv(r'Data/1CapActual2021.csv', index = False, header=True)
            st.success("Uploaded Data:{} OK".format('1CapActual2021.csv'))

            #----------------------------------------------------------------------------------
            x = ['2KPI']
            df= F1.YearMonthValue(FileData,x)
            df.to_csv(r'Data/2KPI.csv', index = False, header=True)
            st.success("Uploaded Data:{} OK".format('2KPI.csv'))

            #----------------------------------------------------------------------------------
            x = ['3Cap','3Actual']
            df= F1.YearMonthVarValue(FileData,x)
            df.to_csv(r'Data/3ActualCap.csv', index = False, header=True)
            st.success("Uploaded Data:{} OK".format('3ActualCap.csv'))
            #----------------------------------------------------------------------------------
            x = '4FeedMill'
            df=pd.read_excel(open(FileData, 'rb'), sheet_name=x)
            df.to_csv(r'Data/4FeedMill.csv', index = False, header=True)
            st.success("Uploaded Data:{} OK".format('4FeedMill.csv'))
            #----------------------------------------------------------------------------------
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
            RunProg()
        elif  Password1=='444':
            st.success('Logged in.') 
            RunAdmin()
        else:
            st.error('Incorrect username or password')
#----------------------------------------------------------------------------------

LogIn()


  



