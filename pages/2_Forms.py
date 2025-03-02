import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title = "Forms",   
    page_icon = "📝",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

# Data management
def load_data(worksheet):
    # Establish connection to Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    st.session_state["df"] = conn.read(worksheet=worksheet,ttl=10)
    st.session_state["df"] = st.session_state["df"].dropna(how='all')
    return st.session_state["df"]

def update_data(data, worksheet):
    conn = st.connection("gsheets", type=GSheetsConnection)
    conn.update(worksheet=worksheet, data = data)
    st.session_state["df"] = conn.read(worksheet=worksheet)
    st.session_state["df"] = st.session_state["df"].dropna(how='all')
    return st.session_state["df"]

if "df" not in st.session_state:
    st.session_state["df"] = None


# Page layout
st.title('Forms')
tab1, tab2, tab3 = st.tabs(["New Asset", "New Lease Contract", "New Lease"])

# New Asset - Tab1
with tab1:
    formtab1_values = {
        "Imovel": None,
        "Lagitude": None,
        "Longitude": None,
        "Estrategia": None,
    }
    with st.form(key='my_formtab1'):
        formtab1_values['Imovel'] = st.text_input(label='Imovel')
        formtab1_values['Lagitude'] = st.number_input(label='Lagitude', min_value=0.00000, max_value=1000.00000, format="%0.00000f")
        formtab1_values['Longitude'] = st.number_input(label='Longitude', min_value=0.00000, max_value=1000.00000, format="%0.00000f")        
        formtab1_values['Estrategia'] = st.selectbox('Estrategia', ['Logistico', 'Escritorio', 'Varejo', 'Educacional',  'Residencial', 'Outros'])  

        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            if not all(formtab1_values.values()):
                st.warning('Please fill all the fields')
            else:
                st.balloons()
                dfnew = pd.DataFrame([formtab1_values])
                st.session_state["df"]  = load_data(worksheet = 'Assets')
                df = st.session_state["df"]
                updated_df = pd.concat([df, dfnew], ignore_index=True)
                st.session_state["df"] = update_data(updated_df, worksheet = 'Assets')
                st.success('New asset added successfully')
                st.write(st.session_state["df"])

# New Lease Contract (Forms) - Tab2 
with tab2:
    formtab2_values = {
        "Imovel": None,
        "Inquilino": None,  
        "ABL": None,
        "Aluguel": None,
        "Data Inicio": None,
        "Data Fim": None,
    }
    with st.form(key='my_formtab2'):
        st.session_state["df"]  = load_data( worksheet = 'Assets')
        formtab2_values['Imovel'] = st.selectbox('Imovel', filter(None, st.session_state["df"]['Imovel'].unique()))
        formtab2_values['Inquilino'] = st.text_input(label='Inquilino')
        formtab2_values['ABL'] = st.number_input(label='ABL', min_value=0, max_value=1000000000, format="%0i")
        formtab2_values['Aluguel'] = st.number_input(label='Aluguel', min_value=0, max_value=1000000000)
        formtab2_values['Data Inicio'] = st.date_input(label='Data Inicio')
        formtab2_values['Data Fim'] = st.date_input(label='Data Fim')

        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            if not all(formtab2_values.values()):
                st.warning('Please fill all the fields')
            else:
                st.balloons()
                dfnew = pd.DataFrame([formtab2_values])
                st.session_state["df"]  = load_data( worksheet = 'Rentroll')
                df = st.session_state["df"]
                updated_df = pd.concat([df, dfnew], ignore_index=True)
                st.session_state["df"] = update_data(updated_df, worksheet = 'Rentroll')
                st.success('New lease contract added successfully')
                st.write(st.session_state["df"])
            
            