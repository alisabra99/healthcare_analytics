import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import hydralit_components as hc
from plotly.offline import init_notebook_mode, iplot
from PIL import Image

st.set_page_config(
    page_title="Suicides Dashboard",
    layout='wide'
)

#reading the csv file,
#filling na values of suicides with 0
df=pd.read_csv(r"C:\Users\aasab\Desktop\who_suicide.csv")
df["suicides_no"].fillna(0,inplace=True)
df.info()



##################################
    
over_theme = {'txc_inactive': 'white','menu_background':'rgb(128,0,0)', 'option_active':'white'}
    
menu_data = [
    {'label': "Data Description"},
    {'label': 'Visuals'},
    {'label': 'Map'}
    ]


menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    sticky_nav=True,
    sticky_mode='sticky'
)




if menu_id == 'Data Description':
    st.write('')
    st.title(' Suicides Dashboard ')
    st.header('This dashboard helps you understand the distribution of suicides among age groups, countries, and gender.')
    coll,colll=st.columns(2)
    with coll:
        st.write(df)
    with colll:
        st.image(Image.open('istockphoto-1029317396-612x612.jpg'))
   
    
   
if menu_id == 'Visuals':
    st.write('')
    st.title(' Suicides Dashboard ')
    col1, col2 = st.columns([4,3])

    with col1:
        
        suicides = df.groupby('year').suicides_no.sum()
        df2 = pd.DataFrame(df.groupby(['year','sex']).suicides_no.sum())
        df2 = df2.unstack()
        
        # a line graph that shows the number of suicides among males and females between year 1979 and 2016
        fig0= px.line(
              df2,
              x=df2.index,
              y=df2.suicides_no.male,
              color_discrete_sequence=["blue"] * len(df2),
              title="Total Number of Suicides between 1979 and 2016",
              labels={
                     "index": "Year",
                     "y": "Number of Suicides",
                 },
              )
        
        fig0.add_scatter(x=df2.index, y=df2.suicides_no.female, name="Female")
        
        # to show the legends
        fig0['data'][0]['showlegend'] = True
        fig0['data'][0]['name'] = 'Male'
        fig0=go.Figure(fig0)
        st.plotly_chart(fig0)


    with col2: 
        #plot of percentage distribution of gender among total number of suicides
        total_number_of_suicides = df.groupby('sex').suicides_no.sum().sum()
        number_of_suicides_by_sex =df.groupby('sex').suicides_no.sum() 
        
        suicide_percentage_by_sex = (number_of_suicides_by_sex / total_number_of_suicides) * 100
        round(suicide_percentage_by_sex, 2)
        fig1= px.bar(suicide_percentage_by_sex,  
                     title="Gender Distribution of the Total Number of Suicides",
                     color_discrete_sequence=["blue"] * len(df2),
                     labels={
                         
                         "value": "Percentage",
                     }, )
        fig1['data'][0]['showlegend'] = False
        fig1=go.Figure(fig1)
        st.plotly_chart(fig1)
        
        
    st.write('')
    
    
    col3, col4 = st.columns([4,3])    
     
    with col3:
        #plot of top countries with suicide
        suicides_by_country=pd.DataFrame(df.groupby('country').suicides_no.sum())
        top_countries_suicide = suicides_by_country.sort_values(by = 'suicides_no', ascending = False).head(6)
        
        
        fig2= px.bar(
              top_countries_suicide,
              title="Top 6 Countries with the Highest Number of Suicides",
              color_discrete_sequence=["blue"] * len(top_countries_suicide),
              labels={
                     "index": "Countries",
                     "y": "Number of Suicides"})
        fig2['data'][0]['showlegend'] = False
        fig2=go.Figure(fig2)
        st.plotly_chart(fig2)


    with col4:
        #plot of top countries with suicide       
        least_countries_suicide=suicides_by_country.sort_values(by = 'suicides_no', ascending = True).head(6) 
        fig3= px.bar(
              least_countries_suicide,
              title="Top 6 Countries with the Lowest Number of Suicides ",
              color_discrete_sequence=["red"] * len(least_countries_suicide),
              labels={
                     "index": "Countries",
                     "y": "Number of Suicides",
                 },
              )
        fig3['data'][0]['showlegend'] = False
        fig3=go.Figure(fig3)
        st.plotly_chart(fig3)
        
        st.write('')
        
        
    col5,col6=st.columns([4,3])
    
    with col5:
        
        suicide_age = df.groupby('age').suicides_no.sum()
        suicide_age = pd.DataFrame(suicide_age)
        
        fig4= px.line(
                  suicide_age,
                  x=suicide_age.index,
                  y=suicide_age.suicides_no,
                  color_discrete_sequence=["blue"] * len(df2),
                  title="Distribution of Suicides by Age",
                  labels={
                         "index": "Age",
                         "suicides_no": "Number of Suicides",
                     },
                  )
        fig4=go.Figure(fig4)
        st.plotly_chart(fig4)

     
    with col6:
        # Plot for distribution of gender in top 6 countries with most suicides
        df_gen=pd.DataFrame(df.groupby(['country','sex'])['suicides_no'].sum()).reset_index()
        df_gen=pd.merge(df_gen,pd.DataFrame(df_gen.groupby(['country'])['suicides_no'].sum()).reset_index(),on=['country'])
        df_gen.rename(columns={'suicides_no_x':'gender_suicides','suicides_no_y':'total_suicides'},inplace=True)
        df_gen.sort_values(by=['total_suicides'],ascending=False,inplace=True)
        df_gen_m=df_gen[df_gen['sex']=="male"]
        df_gen_fm=df_gen[df_gen['sex']=="female"]
        trace1 = go.Bar(
            x=df_gen_m['country'].head(7),
            y=df_gen_m['gender_suicides'].head(7),
            name='Male Suicides'
        )
        trace2 = go.Bar(
            x=df_gen_fm['country'].head(7),
            y=df_gen_fm['gender_suicides'].head(7),
            name='Female Suicides'
        )
        
        data = [trace1, trace2]
        layout = go.Layout(
            barmode='group',
            title='Suicide Distribution amongst the Genders in top 7 countries'
        )
        
        fig5 = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig5)
        
if menu_id == 'Map':
    st.write('')
    df_sui=pd.DataFrame(df.groupby(['country','year'])['suicides_no'].sum().reset_index())
    count_max_sui=pd.DataFrame(df_sui.groupby('country')['suicides_no'].sum().reset_index())

    count = [ dict(
        type = 'choropleth',
        locations = count_max_sui['country'],
        locationmode='country names',
        z = count_max_sui['suicides_no'],
        text = count_max_sui['country'],
        colorscale = 'Viridis',
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick =False,
            title = 'Suicides Country-based'),
      ) ]
    layout = dict(
        title = 'Suicides happening across the Globe',
        geo = dict(
            showframe = True,
            showcoastlines = True,
            projection = dict(
                type = 'Mercator'
                )
            )      
        )
    fig_map = dict( data=count, layout=layout )
    iplot( fig_map, validate=False, filename='d3-world-map' )
    st.plotly_chart(fig_map)
    