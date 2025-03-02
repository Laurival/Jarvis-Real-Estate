import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 


st.set_page_config(
    page_title="Data Entry",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title('Data Entry')


if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

my_input = st.text_input('Enter a value', value=st.session_state["my_input"])
st.session_state["my_input"] = my_input
submit_button = st.button('Submit')
if submit_button:
    st.session_state["my_input"] = my_input
    st.write(f'Input value: {my_input}')

