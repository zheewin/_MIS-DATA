#----------------------------------------------------------------------------------
#   
#----------------------------------------------------------------------------------
import pandas as pd 
import streamlit as st  #streamlit run 0.py
import altair as alt
import Function1 as F1
import Function2KPI as F2KPI
import sys 
import time

#----------------------------------------------------------------------------------
df=pd.read_csv("Data/Area_Wide_Long_AreaCompanyDate.csv")
df1=pd.read_csv("Data/YearMonthVarValue.csv")
df_2KPI=pd.read_csv("Data/2KPI.csv")
df_3ActualCap=pd.read_csv("Data/3ActualCap.csv")
df_4FeedMill=pd.read_csv("Data/4FeedMill.csv")
#----------------------------------------------------------------------------------
def SideBar():
    st.sidebar.header('User Input Features')
    global  Area,Month,df_Month
    Area = st.sidebar.selectbox('Area', sorted(df['Area'].unique()))
    Month = st.sidebar.selectbox('Month', sorted(pd.DatetimeIndex(df['Date']).month.unique()))
    df_Month= df[ (pd.DatetimeIndex(df['Date']).month==Month) ]
#----------------------------------------------------------------------------------

def item1():
    # #----------------------------------------
    DataFrame1 ={'Production(Ton)':[0],'ACCUM':[0],'%UTILIZE':['xx'],'SALE-OUT':['61%'],'GROWTH-YOY':['XXX']}
    #----------------------------------------------------------------------------------
    DataFrame1['Production(Ton)']=  "{0:,.2f}".format(df_Month['ValueAll'].sum())
    DataFrame1['ACCUM']= "{0:,.2f}".format(df['ValueAll'].sum())
    #----------------------------------------------------------------------------------
    Month2020=df1['ValueAll'][  (df1['Year']=='2020年') & (pd.DatetimeIndex(df1['Date']).month==Month) ]
    Month2019=df1['ValueAll'][  (df1['Year']=='2019年') & (pd.DatetimeIndex(df1['Date']).month==Month) ]
    GrowthYOY = (float(Month2020)-float(Month2019))/float(Month2019)
    DataFrame1['GROWTH-YOY']= "{0:,.2%}".format(GrowthYOY)
    #----------------------------------------------------------------------------------
    DataFrame1=pd.DataFrame(DataFrame1)
    st.table(DataFrame1.style.set_properties(**{ 'background-color': 'black','color': 'lawngreen','border-color': 'white'}))
    #----------------------------------------------------------------------------------
def item2():
    DataFrame2 ={'1':['VC','LOSS','PRODUCTIVITY'],
                '2':['GASS CONSUMPTION','UNQUALITIED PRODUCT','MAJOR ACCIDENT'],
                '3':['STANDARD FACTORY','INNOVATION PROJECT','CONSTRUCTION MAJOR ACCIDENT']}
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
    df= DataFrame2.style.apply(hl, axis=None)
    # df= DataFrame2.style.apply(lambda x: fLessSTDG(x,STD1, VC45,0,0), axis=None)

    #-------------------
    st.table(df)
def item3():
    df_3ActualCap_Month= df_3ActualCap[ (pd.DatetimeIndex(df_3ActualCap['Date']).month==Month) ]
    plot= alt.Chart(df_3ActualCap_Month).mark_bar(opacity=0.7
        ).encode(
            alt.X('Year:N', axis=alt.Axis(labelFontSize=13)),
            alt.Y('ValueAll:Q', stack=None, axis=alt.Axis(labelFontSize=15)),
            color=alt.Color('VarAll:N'),
        ).configure_axis(
            labelFontSize=15,
            titleFontSize=15
        ).configure_title(
            fontSize=24
        ).properties(
            title="Actual VS Cap",
            height=400,width=600
        ).configure_axisX(
            labelAngle=-45,
        ).configure_legend(
            titleColor='black', 
            titleFontSize=15,
            labelFontSize=15,
        )
    st.write(plot)
def item4():
    DataFrame1 ={'FeedMill':['0'],'Building':['0']}
    DataFrame1['FeedMill']=df_4FeedMill['ValueAll'][  (df_4FeedMill['Year 2021']=='Feedmill') & (df_4FeedMill['VarAll']=='ACTIVE')]

    Build1=str(df_4FeedMill['ValueAll'][  (df_4FeedMill['Year 2021']=='building') ].sum())
    Active1=str(df_4FeedMill['ValueAll'][  (df_4FeedMill['Year 2021']=='building') &  (df_4FeedMill['VarAll']=='ACTIVE') ].sum())
    Stop1=str(df_4FeedMill['ValueAll'][  (df_4FeedMill['Year 2021']=='building') &  (df_4FeedMill['VarAll']=='STOP') ].sum())

    DataFrame1['Building']=str(Build1) + ' ( Active=' + str(Active1) + ' Stop='+str(Stop1)+' )' 

    DataFrame1=pd.DataFrame(DataFrame1)
    st.table(DataFrame1.style.set_properties(**{ 'background-color': 'black','color': 'lawngreen','border-color': 'white'}))
def cut1td():
    st.markdown("""
    <style>
    table td:nth-child(1) {
        display: none
    }
    table th:nth-child(1) {
        display: none
    }
    </style>
    """, unsafe_allow_html=True)

def LogIn():
    Password1placeholder = st.sidebar.empty()
    btnLogInplaceholder = st.sidebar.empty()

    Password1 = Password1placeholder.text_input('Enter a password',type='password')
    btnLogIn = btnLogInplaceholder.checkbox("Log in")
    btnLogOut = st.sidebar.button('Log Out',key=1)

    if btnLogOut:
        Password1 = Password1placeholder.text_input('Enter a password', value='',key=1)
        btnLogIn = btnLogInplaceholder.checkbox("Log in",key=1)
        st.success('Logged Out.')
    if btnLogIn:
        if Password1=='333':
            st.success('Logged in.') 
            RunProg()
        else:
            st.error('Incorrect username or password')

def RunProg():
    SideBar()
    cut1td()
    item1()
    item2()
    item3()
    item4()

LogIn()
