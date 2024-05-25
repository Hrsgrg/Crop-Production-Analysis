import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import json
import plotly.express as px
from collections import deque
from raceplotly.plots import barplot
from PIL import Image
import geopandas as gpd
import math

# Sidebar menu
with st.sidebar:
    choose = option_menu("Main Menu", ["About", "Task1", "Task2", "Task3"],
                         icons=['house', 'pin-map', 'bar-chart-steps', 'pin-map-fill'],
                         menu_icon="list", default_index=0,
                         styles={
                             "container": {"padding": "5!important", "background-color": "#FFF3E2"},
                             "icon": {"color": "#7C9070", "font-size": "25px"},
                             "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee", "color": "#7C9070", "font-weight": "bold"},
                             "nav-link-selected": {"background-color": "#FEE8B0", 'color': '#7C9070', 'border-radius': '5px'},
                         }
                         )

logo = Image.open('logo.jpg')

# About Page
if choose == "About":
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.markdown(""" <style> .font {
        font-size:55px ; font-family: 'Comic Sans'; color: #cca300} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">About</p>', unsafe_allow_html=True)
    with col2:
        st.image(logo, width=130)

    st.write("## Data")
    st.write("We have used the following datasets for our analysis:")
    st.write("1. India's 1998-2017 crop production statistics by state and district showing annual production of more than fifty crops.")
    st.write("2. Rainfall statistics of India from 1998 to 2017, categorized by district, state, and sub-division.")
    st.write("3. India district-wise geojson (epsg:4326) created from India shapefile using QGIS software.")

    st.write("## Tasks")
    st.write("We have implemented the following tasks in our dashboard:")
    st.write("-**Task 1:** To analyze crop production statistics across the nation (district-wise)")
    st.write("-**Task 2:** To analyze trends in crop production over the years")
    st.write("-**Task 3:** To correlate rainfall pattern with crop production trends")

    st.markdown('<p class="font">Other Crop Production Insights</p>', unsafe_allow_html=True)
    videos = ['videos/vid2.mp4', 'videos/vid1.mp4', 'videos/vid3.mp4']
    for video in videos:
        video_file = open(video, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

    st.write("## Team Members (Group 8)")
    st.write("- Arya Pinaki :smirk:")
    st.write("- Bhavya Garg :unamused:")
    st.write("- Gauri G Menon :penguin:")
    st.write("- Kaushik Raj Nadar :confused:")
    st.write("- S Pradeep :sunglasses:")

# Task 1: Crop Production Map
elif choose == 'Task1':
    st.markdown(""" <style> .font {
        font-size:45px ; font-family: 'Comic Sans'; color: #cca300} 
        </style> """, unsafe_allow_html=True)

    with open('districtsm.geojson') as response:
        geodata = json.load(response)
    df_g = pd.read_csv('merged.csv')
    cr_list = df_g.Crop.unique()

    st.markdown('<p class="font">Crop Annual Production Map</p>', unsafe_allow_html=True)
    with st.form(key='crops_form'):
        st.markdown('<p style="font-family:sans-serif; color:red; font-size: 15px;">***These input fields are required***</p>', unsafe_allow_html=True)
        col0, col01 = st.columns([1, 1])
        with col0:
            Crop = st.selectbox('Crop', cr_list, index=0, help='Choose the crop whose map you desire')
        with col01:
            submitted_crop = st.form_submit_button('Submit')

    st.write("----")

    if submitted_crop:
        if Crop == '-':
            st.warning("You must complete the required fields")
        else:
            crop_file = f'Crops/crop_{Crop}.csv' if Crop != 'Arhar/Tur' else 'Crops/crop_Arhar.csv'
            df = pd.read_csv(crop_file)
            fig = px.choropleth_mapbox(
                df,
                geojson=geodata,
                locations=df.Districts,
                color=df["Production"],
                color_continuous_scale="YlGn",
                range_color=[min(df["Production"]), max(df["Production"])],
                featureidkey="properties.District",
                mapbox_style="carto-positron",
                center={"lat": 22.5937, "lon": 82.9629},
                hover_data=['STATE'],
                animation_frame=df["Crop_Year"],
                zoom=3.5,
                opacity=1.0
            )
            fig.update_layout(autosize=False, height=700, width=600, margin={"r": 0, "t": 0, "l": 0, "b": 0})
            st.plotly_chart(fig, use_container_width=True)

# Task 2: Crop Production Trends
elif choose == 'Task2':
    st.markdown(""" <style> .font {
        font-size:45px ; font-family: 'Comic Sans'; color: #cca300} 
        </style> """, unsafe_allow_html=True)

    df = pd.read_csv('APY.csv')
    st.markdown('<p class="font">National Annual Crop Production</p>', unsafe_allow_html=True)
    df.rename(columns={'District ': 'District', 'Area ': 'Area'}, inplace=True)

    df.dropna(subset=['Production'], inplace=True)
    df.drop(["Season", "Yield", "State", "District", "Area"], axis=1)
    df_new = df.groupby(['Crop', 'Crop_Year'])['Production'].sum().reset_index()
    crops_list = df_new['Crop'].unique()

    cereals = ['Maize', 'Rice', 'Wheat', 'Other Cereals', 'Barley', 'Jowar', 'Ragi', 'Small millets', 'Bajra']
    pulses = ['Arhar/Tur', 'Cowpea(Lobia)', 'Moong(Green Gram)', 'Urad', 'Gram', 'Horse-gram', 'Masoor', 'Other Rabi pulses', 'Peas & beans (Pulses)', 'Other Summer Pulses', 'Other Kharif pulses', 'Peas & beans (Pulses)', 'Khesari', 'Moth']
    nuts_seeds = ['Arecanut', 'Cashewnut', 'Oilseeds total', 'other oilseeds', 'Sunflower', 'Castor seed', 'Linseed', 'Niger seed', 'Safflower']
    spices = ['Black pepper', 'Dry chillies', 'Ginger', 'Rapeseed & Mustard', 'Sesamum', 'Turmeric', 'Coriander', 'Garlic', 'Cardamom']
    vegetables_fruits = ['Banana', 'Sweet potato', 'Tapioca', 'Guar seed', 'Onion', 'Potato', 'Soyabean']
    cash_crops = ['Sugarcane', 'Cotton(lint)', 'Groundnut', 'Jute', 'Tobacco']

    with st.form(key='columns_in_form'):
        st.markdown('<p style="font-family:sans-serif; color:red; font-size: 15px;">***These input fields are required***</p>', unsafe_allow_html=True)
        col0, col01 = st.columns([1, 1])
        with col0:
            master_dropdown = st.selectbox('Type of bar plot', ['cereals', 'pulses', 'nuts_seeds', 'spices', 'vegetables_fruits', 'cash_crops', 'customize'], index=0, help='Choose the type of racing bar plot desired, e.g., cereals, pulses, etc.')
        if master_dropdown == 'customize':
            st.markdown('<p style="font-family:sans-serif; color:red; font-size: 15px;">***Customize your plot***</p>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                dropdown1 = st.selectbox('Crop1:', crops_list)
            with col2:
                dropdown2 = st.selectbox('Crop2:', crops_list)
            with col3:
                dropdown3 = st.selectbox('Crop3:', crops_list)
            col4, col5, col6 = st.columns([1, 1, 1])
            with col4:
                dropdown4 = st.selectbox('Crop4:', crops_list)
            with col5:
                dropdown5 = st.selectbox('Crop5:', crops_list)
            with col6:
                dropdown6 = st.selectbox('Crop6:', crops_list)
            submitted_custom = st.form_submit_button('Submit')

    if master_dropdown != 'customize' or submitted_custom:
        st.write("----")
        if master_dropdown == 'customize':
            crops = [dropdown1, dropdown2, dropdown3, dropdown4, dropdown5, dropdown6]
            crops = [crop for crop in crops if crop != '-']
        else:
            crops = eval(master_dropdown)

        if len(crops) == 0:
            st.warning("You must select at least one crop.")
        else:
            df_new = df_new[df_new['Crop'].isin(crops)]
            fig = barplot(df_new, item_column='Crop', value_column='Production', time_column='Crop_Year')
            fig.show()
            st.plotly_chart(fig, use_container_width=True)

# Additional Tasks (e.g., Task3) can be added here

# Task 3: Rainfall Data and Crop Production Map
elif choose == 'Task3':
    st.markdown(""" <style> .font {
        font-size:45px ; font-family: 'Comic Sans'; color: #cca300} 
        </style> """, unsafe_allow_html=True)

    with open('districtsm.geojson') as response:
        geodata = json.load(response)
    
    dist_names = [feature['properties']['REMARKS'] for feature in geodata['features']]
    geo_df = gpd.GeoDataFrame.from_features(geodata["features"])
    df_rainfall = pd.read_csv('Rainfall_Final.csv')
    df_rainfall = df_rainfall[df_rainfall['SUBDIVISION'].isin(dist_names)]
    
    loca = df_rainfall['Districts']
    cola = df_rainfall['Annual Rainfall']
    ani = df_rainfall['Year']
    
    df_g = pd.read_csv('merged.csv')
    cr_list = df_g.Crop.unique()

    st.markdown('<p class="font">Annual Rainfall Data Map</p>', unsafe_allow_html=True)
    st.write("----")

    fig = px.choropleth_mapbox(geojson=geodata, 
                                locations=loca, 
                                color=cola, 
                                color_continuous_scale="Blues",
                                range_color=[max(cola),1000+min(cola)],
                                featureidkey="properties.District",
                                mapbox_style="carto-positron",
                                center={"lat": 22.5937, "lon": 82.9629},
                                animation_frame=ani,
                                zoom=3.5,
                                opacity=1.0)
    fig.update_layout(autosize=False,
                        height=700,
                        width=600,
                        margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
    st.write("----")

    st.markdown('<p class="font">Crop Map</p>', unsafe_allow_html=True)
    with st.form(key='crop_rainfall'):
        st.markdown('<p style="font-family:sans-serif; color:red; font-size: 15px;">***These input fields are required***</p>', unsafe_allow_html=True)
        col0, col01 = st.columns([1, 1])
        with col0:
            Crop = st.selectbox('Crop', cr_list, index=0, help='Choose the crop whose map you desire')
        with col01:
            submitted_crop = st.form_submit_button('Submit')

    st.write("----")

    if submitted_crop:
        if Crop == '-':
            st.warning("You must complete the required fields")
        else:
            st.markdown('<p class="font">Generating your crop map!</p>', unsafe_allow_html=True)  
            crop_file = f'Crops/crop_{Crop}.csv' if Crop != 'Arhar/Tur' else 'Crops/crop_Arhar.csv'
            df = pd.read_csv(crop_file)
            fig = px.choropleth_mapbox(
                                df, 
                                geojson = geodata, 
                                locations = df.Districts, 
                                color = df["Production"], 
                                color_continuous_scale = "YlGn",
                                range_color = [max(df["Production"]),min(df["Production"])],
                                featureidkey = "properties.District",
                                mapbox_style = "carto-positron",
                                center = {"lat": 22.5937, "lon": 82.9629},
                                hover_data=['STATE'],
                                animation_frame = df["Crop_Year"],
                                zoom = 3.5,
                                opacity = 1.0
                                )
            fig.update_layout(autosize=False,
                        height=700,
                        width=600,
                        margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)



    
   
        
      
               
