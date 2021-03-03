import pandas as pd
# import pyodbc 
import altair as alt
import streamlit as st # streamlit run app.py
import numpy as np



st.set_page_config(page_title='Audit Analize', page_icon="https://raw.githubusercontent.com/zheewin/PicDATA/master/Man1.jpg", layout='centered', initial_sidebar_state='auto')

# =============================================
st.markdown("""
<style>
body {
    color: black;
    background-color: white;
}
</style>
    """, unsafe_allow_html=True)
    
# =============================================
st.sidebar.title("User Input Features")
btn1 = st.sidebar.button('Update Data')
# ============================================= Refresh Data
# if btn1:
    # # ============================================= DataBase
    # conn = pyodbc.connect('Driver={SQL Server};'
    #                     'Server=103.244.82.194,1433\SQLEXPRESS;'
    #                     'UID=sa;'
    #                     'PWD=cpgroup@1;'
    #                     'Database=_2021_FacCheck;'
    #                     )
    # cursor = conn.cursor()
    # df_o = pd.read_sql_query("SELECT * FROM [3_Data] ",conn)
    # df_o.to_csv(r'Data_SQL.csv', index = False, header=True)
# ============================================= Data Original
df_o=pd.read_csv('Data_SQL.csv')
df_o=df_o[ (df_o['enable'])!='-' ]

def SideBar():
    # st.sidebar.header('User Input Features')
    # OptionSidebar = st.sidebar.empty()
    # AreaSidebar = st.sidebar.empty()
    CompanySidebar = st.sidebar.empty()

    df=df_o
    # global  Area,Company,Title1,df_Selected
    # option1 = OptionSidebar.radio("", ('Nationwide','Area','Company'), index=2) 
    # if option1 == 'Area':
    #     CompanySidebar.empty()
    #     Area = AreaSidebar.selectbox('Area', sorted(df['Area'].unique()))
    #     Title1= ' - %s' %(Area)
    #     df=df[ (df['Area'])==Area ]

    # elif option1 == 'Company': 
    #     AreaSidebar.empty()
    #     Company = CompanySidebar.selectbox('Company', sorted(df['Company'].unique()))
    #     Title1= ' - %s' %(Company)
    #     df=df[ (df['Company'])==Company ]

    # elif option1 == 'Nationwide': 
    #     AreaSidebar.empty()
    #     CompanySidebar.empty()
    #     Title1= ' - Nationwide' 
    #     df=df

    Company = CompanySidebar.selectbox('选择公司', sorted(df['Company'].unique()))
    global Title1,df_Selected
    Title1= '%s' %(Company)
    df=df[ (df['Company'])==Company ]

    df_Selected = df
SideBar()
st.header(Title1)
# ============================================= Function Show

def FindSerious():
    title=''
    # ============================================= Data for chart1
    def CheckJiBie(jiBie):
        df=df_Selected[ (df_Selected['jiBie'])==jiBie ]
        jiBieCountAll=df['jiBie'].value_counts()

        df['ManFen_GetFen']=df['manFen']-df['getFen']
        df=df[ (df['ManFen_GetFen']) != 0 ]
        jiBieData=df[['id0','Bitem1','Bitem2','itemT','manFen','getFen','Comment']]
        jiBieCount=df['jiBie'].value_counts()
        return jiBieCount,jiBieCountAll,jiBieData

    di_jiBieCount,di_jiBieCountAll,di_jiBieData=CheckJiBie('di')
    zhong_jiBieCount,zhong_jiBieCountAll,zhong_jiBieData=CheckJiBie('zhong')
    gao_jiBieCount,gao_jiBieCountAll,gao_jiBieData=CheckJiBie('gao')

 
    df=pd.DataFrame({'风险及':['低','中','高']
                    ,'# โดนตัด':[di_jiBieCount.values,zhong_jiBieCount.values,gao_jiBieCount.values]
                    ,'# หัวข้อทั้งหมด':[di_jiBieCountAll.values,zhong_jiBieCountAll.values,gao_jiBieCountAll.values]
    })
  
    df['# หัวข้อทั้งหมด']=df['# หัวข้อทั้งหมด'].astype(int) # Change Type 
    df['# โดนตัด']=df['# โดนตัด'].astype(str) # Change Type 
   
    st.table(df.style.set_properties(**{ 'text-align': 'right','background-color': 'black','color': 'lawngreen','border-color': 'white'}))

    st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    JiBieoption1 = st.radio("风险及", ('低','中','高'), index=2) 
    if JiBieoption1 == '低':
        df_selectJiBie=di_jiBieData
    elif JiBieoption1 == '中': 
        df_selectJiBie=zhong_jiBieData
    elif JiBieoption1 == '高': 
        df_selectJiBie=gao_jiBieData
    st.table(df_selectJiBie.assign(hack='').set_index('hack'))
def barChart2():
    st.header('คะแนนแต่ละพื้นที่')
    title=''
    # ============================================= Data for chart1
    # df = df_o[['id0','Bitem1','getFen','manFen']].groupby(['Bitem1'])['getFen','manFen'].sum().reset_index()
    df=df_Selected.groupby('Bitem1').agg({'id0': 'min', 'getFen': 'sum', 'manFen': 'sum'}).reset_index()
    df = df.sort_values('id0', ascending=True)
    df['Percentage']=df['getFen']/df['manFen'] 
    source = df
    # =============================================
    bar = alt.Chart(source
            ).encode(alt.X('getFen:Q', axis=alt.Axis(labelFontSize=10),scale=alt.Scale(domain=[1, 1])),
                    alt.Y('Bitem1:O', axis=alt.Axis(labelFontSize=15,titleFontSize=30,title='区域',labelColor='lawngreen',titleColor='white'), sort=['id0']),
                    color=alt.Color('Bitem1:N', legend=None),
            ).mark_bar(
            )

    text = bar.mark_text(align='left', baseline='middle',fontSize=15,color='white').encode(text=alt.Text('sum(Percentage):Q',format=".1%"),)
    #---------------------------------------- Show Chart
    plot=(bar   + text
        ).properties(width=500,title=title ,
        ).configure_axis(labelFontSize=10,titleFontSize=15,
        ).configure_title(fontSize=24,
        ).configure_axisX(labelAngle=-45,
        ).encode( #tooltip=['Bitem1'],
        ).interactive(
        ).configure_point(size=200
        ).configure_legend(orient="bottom"
        ).interactive(bind_x=True, bind_y=True
        ).configure(background='black',
        )
    st.write(plot)
def barChart1():
    st.header('2021年 达标及质量安全管理检查')
    # ============================================= Data for chart1
    df = df_o[['Company','getFen','manFen']].groupby(['Company'])['getFen','manFen'].sum().reset_index()
    df['Percentage']=df['getFen']/df['manFen'] 
    source = df
    # =============================================
    bar = alt.Chart(source
            ).encode(alt.X('getFen:Q', axis=alt.Axis(labelFontSize=10),title='',scale=alt.Scale(domain=[1, 1])),
                    alt.Y('Company:O', axis=alt.Axis(labelFontSize=15,titleFontSize=30,title='',labelColor='lawngreen',titleColor='white'), sort='x'),
            ).mark_bar(
            )

    text = bar.mark_text(align='left', baseline='middle',fontSize=15,color='white').encode(text=alt.Text('sum(Percentage):Q',format=".1%"),)
    #---------------------------------------- Show Chart
    plot=(bar   + text
        ).properties(width=500,title='' ,
        ).configure_axis(labelFontSize=10,titleFontSize=15,
        ).configure_title(fontSize=24,
        ).configure_axisX(labelAngle=-45,
        ).encode(tooltip=['Company'],
        ).interactive(
        ).configure_point(size=200
        ).configure_legend(orient="bottom"
        ).interactive(bind_x=True, bind_y=True
        ).configure(background='black',
        )
    st.write(plot)

FindSerious()
barChart2()
barChart1()





