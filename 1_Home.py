import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt

# Pages configuration
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Data management
if "df" not in st.session_state:
    st.session_state["df"] = None
def load_data(worksheet):
    conn = st.connection("gsheets", type=GSheetsConnection)
    st.session_state["df"] = conn.read(worksheet= worksheet,ttl=10)
    st.session_state["df"] = st.session_state["df"].dropna(how='all')
    return st.session_state["df"]

# Home page
st.title('Welcome to Jarvis')
st.markdown('A platform to manage your real estate properties')


# Assets
with st.expander('Asset'): 
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

