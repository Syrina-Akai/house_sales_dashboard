import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from modules import *

DATA = pd.read_csv('data/Real_es.csv')
plot = Plot(DATA)


st.set_page_config(
    page_title = 'House sales Dashboard',
    page_icon = '🔎',
    layout = 'wide'
)



def home_page():
    # make a title
    
    st.title('Analysing House sales data')
    # 2 columns 
    col1, col2 = st.columns(2)
    # first column
    with col1:
        fig1 = plot.get_plot("quantitatif_qualitatif_pie")
        st.write(fig1)
    # second column
    with col2:
        fig2 = plot.get_plot("correlation_matrix")
        st.write(fig2)
    

    st.dataframe(DATA.head(), hide_index=True)


def analyse_page():
    st.title('Customized analysis')
    col1, col2 = st.columns(2)
    plot_name, column_x, column_y = 'scatter', 'Area (ft.)', 'Price'
    with col1:
        # make 2 input to choose a column and a plot
        column_x = st.selectbox('Choose a column for X', sorted(set(plot.df.columns)))
        column_y = st.selectbox('Choose a column for Y', sorted(list(set(plot.df.columns) - {column_x})))
        plot_name = st.selectbox('Choose a plot', ["scatter", "line", "bar"])
    with col2:
        # plot the selected plot
        fig = plot.get_plot(plot_name, column_x, column_y)
        st.write(fig)

# column_x = st.selectbox('Choose a column for X', DATA.columns, index=DATA.columns.get_loc(default_column) if default_column in DATA.columns else 0)



# add a menu on the left side
with st.sidebar:
    selected = option_menu("Main Menu", ["Home", 'Analyse', 'About'], 
        icons=['house', 'clipboard2-pulse', 'info-circle'], menu_icon="cast", default_index=0)
    
if selected == 'Home':
    home_page()
if selected == 'Analyse':
    analyse_page()

if selected == 'About':
    st.title('About the project')
    st.write('This is a simple dashboard to analyse house sales data')
    st.write('It is made using streamlit and plotly')
    st.write('The link to the github repository is: https://github.com/siddharthbhansali/HouseSalesAnalysis')


