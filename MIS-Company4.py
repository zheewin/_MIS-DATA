#----------------------------------------------------------------------------------
#   By Company = Function1 + MIS_Data.csv + 
#----------------------------------------------------------------------------------
import pandas as pd 
import streamlit as st  #streamlit run MIS-Company.py
import altair as alt
import Function1 as F1
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
df=pd.read_csv("MIS_Data.csv")
Area = st.sidebar.selectbox('Area', sorted(df['Area'].unique()))
df= df[ (df['Area']==Area) ]
#----------------------------------------
Name = st.sidebar.selectbox('Company', sorted(df['Company'].unique()))
df= df[ (df['Company']==Name) ]
#----------------------------------------------------------------------------------
#---------------------------------------------------------------------------------- 8
df1=df[ (df['VarAll']=='总产量颗粒料产量PELLET') |
        (df['VarAll']=='猪料产量1') |
        (df['VarAll']=='猪三宝产量1') |
        (df['VarAll']=='肉猪料1') |
        (df['VarAll']=='种猪料产量1') |
        (df['VarAll']=='肉鸡料产量1') |
        (df['VarAll']=='蛋鸡料产量1') |
        (df['VarAll']=='肉种鸡料产量1') |
        (df['VarAll']=='鸭料产量1') |
        (df['VarAll']=='鱼料产量1') |
        (df['VarAll']=='虾蟹料产量1') |
        (df['VarAll']=='膨化鱼料产量1') |
        (df['VarAll']=='牛羊料产量1') |
        (df['VarAll']=='其它料产量1') 
    ]
st.write(F1.Company_markLine(df1,'8.生产产量','Ton'))
#---------------------------------------------------------------------------------- 7  
df1= df[ (df['VarAll']=='混合机产量') ]
st.write(F1.Company_markLine_NoLeg(df1,'7.混合机产量','Ton'))
#---------------------------------------------------------------------------------- 6 
plot = F1.Y2axisSTD(df,'Ton','颗粒料产量_','Loss','总损耗_','6.颗粒料产量 vs 总损耗')
st.write(plot)
#---------------------------------------------------------------------------------- 5
df1=df[ (df['VarAll']=='变动费用') |
        (df['VarAll']=='直接制造费用') |
        (df['VarAll']=='其它生产费用') |
        (df['VarAll']=='粒料制造费用') |
        (df['VarAll']=='粉料制造费用') 
    ]
st.write(F1.Company_markLine(df1,'5.费用','RMB'))
#---------------------------------------------------------------------------------- 4  
df1=df[ (df['VarAll']=='ELECTRICCONSUMPTION_') ]
st.write(F1.Company_markLine_NoLeg(df1,'4.电耗','度/吨'))
#---------------------------------------------------------------------------------- 3  
df1=df[ (df['VarAll']=='PERFORMANCE_') ]
st.write(F1.Company_markLine_NoLeg(df1,'3.吨/人/月','Ton'))
#---------------------------------------------------------------------------------- 2  
df1=df[ (df['VarAll']=='AllWageEX') ]
st.write(F1.Company_markLine_NoLeg(df1,'2.劳务费+工资（元/吨）','RMB/Ton'))
#---------------------------------------------------------------------------------- 1
df1=df[ (df['VarAll']=='MANPOWER_Staff') | (df['VarAll']=='MANPOWER_Labour') ]
st.write(F1.Company_markLine_NoLeg(df1,'1.MANPOWER 人数','人'))
#---------------------------------------------------------------------------------- 0 
