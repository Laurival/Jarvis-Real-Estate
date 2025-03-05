import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
import altair as alt
import numpy as np
import plotly.express as px

# Pages configuration
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state= "collapsed",
)

# Data management
if "df" not in st.session_state:
    st.session_state["df"] = None
def load_data(worksheet):
    conn = st.connection("gsheets", type=GSheetsConnection)
    st.session_state["df"] = conn.read(worksheet= worksheet,ttl=10)
    st.session_state["df"] = st.session_state["df"].dropna(how='all')
    return st.session_state["df"]

# Features
def plot_map():
    st.session_state["df"]  = load_data( worksheet = 'Assets')
    map = folium.Map(location=[-23.587461222039746, -46.67960737644582])
    for i in range(0, len(st.session_state["df"])):
        location = [st.session_state["df"].iloc[i]['LAT'], st.session_state["df"].iloc[i]['LON']]
        folium.Marker(location, tooltip= st.session_state["df"].iloc[i]['Imovel']).add_to(map) 
    st_folium(map, width=1500, height=400, center=[-23.3, -45.0] ,zoom=8)

# Home page
st.title('Welcome to Jarvis')
st.markdown('A platform to manage your real estate properties')
st.session_state["df"] = load_data( worksheet = 'Assets')

# Dashboard
with st.container(border=True):
    columns = st.session_state["df"].columns.tolist()
    selected_columns = st.selectbox('Select column', columns)
    unique_values = st.session_state["df"][selected_columns].unique()
    selected_value = st.selectbox('Select value', unique_values)

    filtered_df = st.session_state["df"][st.session_state["df"][selected_columns] == selected_value]
    col1, col2= st.columns(2, vertical_alignment="bottom", border= True)
with col1:
        chart_data = pd.DataFrame({
            "Classificacao": filtered_df["Classificacao"],
            "Valor Patrimonial": filtered_df["Valor Patrimonial"]
        })
        fig = px.pie(chart_data, values='Valor Patrimonial', names='Classificacao' , height=360) 
        st.plotly_chart(fig, use_container_width=True)
with col2:
        chart_data = pd.DataFrame({
            "UF": filtered_df["UF"],
            "Classificao": filtered_df["Classificacao"],
            "Valor Patrimonial": filtered_df["Valor Patrimonial"]
        })
        st.bar_chart(chart_data, x='UF', y='Valor Patrimonial', color='Classificao', use_container_width=True)

# Assets
with st.expander('Asset'): 
    plot_map()   
    st.session_state["df"] = load_data( worksheet = 'Assets')
    st.write(st.session_state["df"])    
       
# Rent Roll
with st.expander('Rent Roll'): 
    st.session_state["df"] = load_data( worksheet = 'Rentroll')
    st.write(st.session_state["df"])


# Generate Plot
with st.expander('Generate Plot'): 
    st.session_state["df"] = load_data( worksheet = 'Rentroll')
    x_column = st.selectbox('X axis', st.session_state["df"].columns)
    y_column = st.selectbox('Y axis', st.session_state["df"].columns)

    plot_data_button = st.button('Generate Plot')
    if plot_data_button:
        st.bar_chart(st.session_state["df"].set_index(x_column)[y_column])
    else:
        st.write('Click on the button to generate the plot')

