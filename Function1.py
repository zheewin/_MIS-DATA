#----------------------------------------------------------------------------------
import pandas as pd 
import streamlit as st  #streamlit run MIS-Company.py
import altair as alt
import os
# #----------------------------------------------------------------------------------
# File_Area='/BackUp/MIS_REPORT_效率_单耗_人力.xls'
#----------------------------------------------------------------------------------
def Melt_F(FileExcel,SheetName): # ------- Area + Doc
    df1=pd.read_excel(open(FileExcel, 'rb'), sheet_name='Area') 
    df2=pd.read_excel(open(FileExcel, 'rb'), sheet_name=SheetName) 
    df = pd.merge(df1,df2,on ='Company',how ='inner') 
    SheetName = df.melt(id_vars=['Area','Company'], var_name=['Date'], value_name=SheetName)
    return SheetName
def Area_Wide_Long_AreaCompanyDate(FileData,x):
    # ------- Area + Doc
    DataX={}
    for i,element in enumerate(x):
        DataX[i]=Melt_F(FileData,element)
    # ------- Merge -> df(Wide)
    AllTab=DataX[0]
    # st.dataframe(AllTab)
    for i in range(len(DataX)-1):
        AllTab = pd.merge(AllTab,DataX[i+1],on =['Company','Area','Date'],how ='inner') 
    df=AllTab
    # ------- Melt -> df(Long)
    df = df.melt(id_vars=['Area','Company','Date'], var_name=['VarAll'], value_name='ValueAll')
    # st.dataframe(df)
    return df
def YearMonthValue(FileData,x):
    # ------- All Tab
    DataX={}
    for i,element in enumerate(x):
        df= pd.read_excel(open(FileData, 'rb'), sheet_name=element) 
        DataX[i] = df.melt(id_vars=['Year'], var_name=['Date'], value_name=element)
        # st.dataframe(DataX[i])
    # ------- Merge -> df(Wide)
    AllTab=DataX[0]
    # st.dataframe(AllTab)
    for i in range(len(DataX)-1):
        AllTab = pd.merge(AllTab,DataX[i+1],on =['Year'],how ='inner') 
    df=AllTab
    # st.dataframe(df)
    # ------- Melt -> df(Long)
    df = df.melt(id_vars=['Year','Date'], var_name=['VarAll'], value_name='ValueAll')
    # st.dataframe(df)
    return df
def YearMonthVarValue(FileData,x):
    # ------- All Tab
    DataX={}
    for i,element in enumerate(x):
        df= pd.read_excel(open(FileData, 'rb'), sheet_name=element) 
        # st.dataframe(df)
        DataX[i] = df.melt(id_vars=['Year'], var_name=['Date'], value_name=element)
        # st.dataframe(DataX[i])
    # ------- Merge -> df(Wide)
    AllTab=DataX[0]
    # st.dataframe(AllTab)
    for i in range(len(DataX)-1):
        AllTab = pd.merge(AllTab,DataX[i+1],on =['Year','Date'],how ='inner') 
    df=AllTab
    # st.dataframe(df)
    # ------- Melt -> df(Long)
    df = df.melt(id_vars=['Year','Date'], var_name=['VarAll'], value_name='ValueAll')
    # st.dataframe(df)
    return df
#------------------------------------------------------------------------
def Area_markLine(df,Title,YTitle,Color1): # ------- df -> Line
    selection = alt.selection_multi(fields=[Color1], bind='legend')

    plot = alt.Chart(df).mark_line(interpolate='basis'
        ).encode(
            alt.X('month(Date):N', axis=alt.Axis(labelFontSize=10)),
            alt.Y('average(ValueAll):Q', axis=alt.Axis(labelFontSize=15,title=YTitle)),
            color=alt.Color(Color1,sort=alt.EncodingSortField('average(ValueAll):O', op='mean', order='descending')),
            opacity=alt.condition(selection, alt.value(2), alt.value(0.2)),
        ).configure_axis(
            labelFontSize=15,
            titleFontSize=15
        ).configure_title(
            fontSize=24
        ).properties(
            title=Title,
            height=400,width=600,
        ).configure_axisX(
            labelAngle=-45,
        ).configure_legend(
            titleColor='black', 
            titleFontSize=15,
            labelFontSize=15,
        ).add_selection(
            selection
        )
    return plot
def Area_markLine_NoLeg(df,Title,YTitle,Color1): # ------- df -> Line
    selection = alt.selection_multi(fields=[Color1], bind='legend')

    plot = alt.Chart(df).mark_line(interpolate='basis'
        ).encode(
            alt.X('month(Date):N', axis=alt.Axis(labelFontSize=10)),
            alt.Y('average(ValueAll):Q', axis=alt.Axis(labelFontSize=15,title=YTitle)),
            color=alt.Color(Color1,legend=None,sort=alt.EncodingSortField('average(ValueAll):O', op='mean', order='descending')),
            opacity=alt.condition(selection, alt.value(2), alt.value(0.2)),
        ).configure_axis(
            labelFontSize=15,
            titleFontSize=15
        ).configure_title(
            fontSize=24
        ).properties(
            title=Title,
            height=400,width=600,
        ).configure_axisX(
            labelAngle=-45,
        ).configure_legend(
            titleColor='black', 
            titleFontSize=15,
            labelFontSize=15,
        ).add_selection(
            selection
        )
    return plot
def Company_markLine(df,Title,YTitle): # ------- df -> Line
    selection = alt.selection_multi(fields=['VarAll'], bind='legend')

    plot = alt.Chart(df).mark_line(interpolate='basis'
        ).encode(
            alt.X('month(Date):N', axis=alt.Axis(labelFontSize=10)),
            alt.Y('ValueAll:Q', axis=alt.Axis(labelFontSize=15,title=YTitle)),
            color=alt.Color('VarAll:N',sort=alt.EncodingSortField('ValueAll:O', op='mean', order='descending')),
            opacity=alt.condition(selection, alt.value(2), alt.value(0.2)),
        ).configure_axis(
            labelFontSize=15,
            titleFontSize=15
        ).configure_title(
            fontSize=24
        ).properties(
            title=Title,
            height=400,width=600,
        ).configure_axisX(
            labelAngle=-45,
        ).configure_legend(
            titleColor='black', 
            titleFontSize=15,
            labelFontSize=15,
        ).add_selection(
            selection
        )
    return plot
def Company_markLine_NoLeg(df,Title,YTitle): # ------- df -> Line
    selection = alt.selection_multi(fields=['VarAll'], bind='legend')

    plot = alt.Chart(df).mark_line(interpolate='basis'
        ).encode(
            alt.X('month(Date):N', axis=alt.Axis(labelFontSize=10)),
            alt.Y('ValueAll:Q', axis=alt.Axis(labelFontSize=15,title=YTitle)),
            color=alt.Color('VarAll:N',legend=None,sort=alt.EncodingSortField('ValueAll:O', op='mean', order='descending')),
            opacity=alt.condition(selection, alt.value(2), alt.value(0.2)),
        ).configure_axis(
            labelFontSize=15,
            titleFontSize=15
        ).configure_title(
            fontSize=24
        ).properties(
            title=Title,
            height=400,width=600,
        ).configure_axisX(
            labelAngle=-45,
        ).configure_legend(
            titleColor='black', 
            titleFontSize=15,
            labelFontSize=15,
        ).add_selection(
            selection
        )
    return plot

def markLine_Month_ValueAll_legend(df,Title,YTitle): # ------- df -> Line
    selection = alt.selection_multi(fields=['Year'], bind='legend')

    plot = alt.Chart(df).mark_line(interpolate='basis'
        ).encode(
            alt.X('month(Date):N', axis=alt.Axis(labelFontSize=10)),
            alt.Y('ValueAll:Q', axis=alt.Axis(labelFontSize=15,title=YTitle)),
            color=alt.Color('Year:N'),
            opacity=alt.condition(selection, alt.value(2), alt.value(0.2)),
        ).configure_axis(
            labelFontSize=15,
            titleFontSize=15
        ).configure_title(
            fontSize=24
        ).properties(
            title=Title,
            height=400,width=600,
        ).configure_axisX(
            labelAngle=-45,
        ).configure_legend(
            titleColor='black', 
            titleFontSize=15,
            labelFontSize=15,
        ).add_selection(
            selection
        )
    return plot
 

#------------------------------------------------------------------------
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

#------------------------------------------------------------------------
def Y2axisSTD(df,Y1T,Y1D,Y2T,Y2D,fTitle): # ------- Melt -> df(Long)
    base = alt.Chart(df).encode(alt.X('month(Date):T'))
    line_A = base.mark_line(color='#5276A7',interpolate='basis').encode(
        alt.Y('average(ValueAll):Q', axis=alt.Axis(titleColor='#F18727',title= Y1T))
    ).transform_filter("datum.VarAll ==" + "'" + Y1D + "'")

    line_B = base.mark_line(color='#F18727',interpolate='basis').encode(
        alt.Y('average(ValueAll):Q', axis=alt.Axis(titleColor='#5276A7',title= Y2T))
    ).transform_filter("datum.VarAll == " + "'" + Y2D + "'")
    
    showG=alt.layer(line_A, line_B
        ).resolve_scale(
            y='independent',
        ).configure_axis(
            labelFontSize=15,
            titleFontSize=20
        ).configure_title(
            fontSize=24
        ).properties(
            title =fTitle ,
            height=400,width=600
        ).configure_axisX(
            labelAngle=-45,
        ).encode(
            color=alt.Color('VarAll:N'),
        ).configure_legend(
            titleColor='black', 
            titleFontSize=15,
            labelFontSize=15,
    )
    return showG
#------------------------------------------------------------------------
def save_uploadedfile(uploadedfile):
     with open(os.path.join("",'MIS_Data.xls'),"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success("Saved File:{} OK".format('MIS_Data.xls'))





