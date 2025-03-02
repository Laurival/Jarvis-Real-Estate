import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title('CSV Input')

uploaded_file = st.file_uploader("Choose a CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.subheader('Data Preview')
    st.write(df.head())

    st.subheader('Filter Data')
    columns = df.columns.tolist()
    selected_columns = st.selectbox('Select column', columns)
    unique_values = df[selected_columns].unique()
    selected_value = st.selectbox('Select value', unique_values)

    filtered_df = df[df[selected_columns] == selected_value]
    st.write(filtered_df)

    st.subheader('Data Visualization')
    x_column = st.selectbox('X axis', columns)
    y_column = st.selectbox('Y axis', columns)

    if st .button('Generate Plot'):
        st.line_chart(df.set_index(x_column)[y_column])
    else:
        st.write('Click on the button to generate the plot')    