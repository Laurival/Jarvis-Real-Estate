import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title = "Forms",   
    page_icon = "📝",
    layout = "wide",
    initial_sidebar_state = "collapsed"
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

# Features
def plot_map():
    st.session_state["df"]  = load_data( worksheet = 'Assets')
    st.map(st.session_state["df"].set_index('Imovel')[['LAT', 'LON']].dropna())

# Page layout
st.title('Forms 📝')
tab1, tab2, tab3 = st.tabs(["New Asset", "New Lease Contract", "To be Continued"])

# New Asset - Tab1
with tab1:
    col1, col2= st.columns(2, vertical_alignment="top", border= True)

    with col1:
        # Plot map
        plot_map()

    with col2:
        formtab1_values = {
            "Imovel": None,
            "LAT": None,
            "LON": None,
            "Estrategia": None,
            "UF": None,
            "Cidade": None,
            "Classificacao": None,
            "Valor Patrimonial": None,
        }
        
        with st.form(key='my_formtab1'):
            formtab1_values['Imovel'] = st.text_input(label='Imovel')
            formtab1_values['LAT'] = st.number_input(label='LAT', min_value=-100.000000, max_value=100.000000, format="%0.6f", value= 0.00000)
            formtab1_values['LON'] = st.number_input(label='LON', min_value=-100.000000, max_value=100.000000, format="%0.6f", value= 0.00000)        
            formtab1_values['Estrategia'] = st.selectbox('Estrategia', ['Logistico', 'Escritorio', 'Varejo', 'Educacional',  'Residencial', 'Outros'])
            formtab1_values['UF'] = st.selectbox('UF', ['SP', 'RJ', 'MG', 'ES', 'BA', 'CE', 'PE', 'RN', 'PB', 'AL', 'SE', 'PI', 'MA', 'PA', 'AP', 'AM', 'RR', 'AC', 'RO', 'MT', 'MS', 'GO', 'DF', 'PR', 'SC', 'RS'])
            formtab1_values['Cidade'] = st.text_input(label='Cidade')
            formtab1_values['Classificacao'] = st.selectbox('Classificacao', ['AAA', 'AA', 'A', 'B', 'C'])
            formtab1_values['Valor Patrimonial'] = st.number_input(label='Valor Patrimonial', min_value=0, max_value=10000000000)  

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
            
            