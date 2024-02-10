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
        plot_name = st.radio("Choose a plot", ("scatter", "line", "bar"), horizontal=True)
    with col2:
        # plot the selected plot
        fig = plot.get_plot(plot_name, column_x, column_y)
        st.write(fig)

def about_page():
    st.title('About us')
    # Our mission is to make a simple and awesome dashboard for data analysis
    st.markdown("""
                **FLICI Syrine** an algerian data enthousiast.\nI mainly work on data analysis and data mining.\
             \nThis dashboard is a simple and awesome example of how I usually present my work.
                """)
    # add a link to the github repository
    st.markdown("""
                **Github repository**\n
                The link to the github repository is: [House sales dashboard](https://github.com/Syrina-Akai/house_sales_dashboard)\
                """)
    # add contact me buttons with linkdin and mail 
    st.markdown("""
                **Contact me**\n
                 [![Linkedin](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/syrine-mahdia-flici-6b8774201/)
                 [![Mail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:syrine.flici@gmail.com)
                """)

# add a menu on the left side
with st.sidebar:
    selected = option_menu("Main Menu", ["Home", 'Analyse', 'About'], 
        icons=['house', 'clipboard2-pulse', 'info-circle'], menu_icon="cast", default_index=0)
    
if selected == 'Home':
    home_page()
if selected == 'Analyse':
    analyse_page()

if selected == 'About':
    about_page()
    


