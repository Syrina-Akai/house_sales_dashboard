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


def datascience_page():
    st.title("Comparing trained models")
    st.markdown(f"""
                **Trained data**
                \nWe used mainly the following parameters as Input : {', '.join(plot.df.columns)} 
                \n**Training**
                \nFor a simple data as we have in our case, we used simple models to predict the *mortgage* of a house.\
                \nWe've mainly used *Random Forest* and *Linear Regression* models.
            """)
    
    # 2 columns to show the roc curve and the confusion matrix
    col1, col2 = st.columns(2)
    with col1:
        st.title("Random Forest")
        # draw the confusion matrix and the roc curve
        fig1 = plot.plot_roc_curve('Random Forest')
        st.write(fig1)
        fig2 = plot.plot_confusion_matrix('Random Forest')
        st.write(fig2)
    with col2:
        st.title("Logistic Regression")
        # draw the confusion matrix and the roc curve
        fig3 = plot.plot_roc_curve('Logistic Regression')
        st.write(fig3)
        fig4 = plot.plot_confusion_matrix('Logistic Regression')
        st.write(fig4)


def about_page():
    st.title('About us')
    # Our mission is to make a simple and awesome dashboard for data analysis
    st.markdown("""
                **Meet Syrine FLICI, Your Algerian Data Enthusiast!**\n
                Diving deep into the world of data, I thrive on unraveling insights and uncovering hidden gems.\
                 Specializing in data analysis and mining, I craft meaningful narratives from complex datasets.\n
                Welcome to my world! This dashboard serves as a glimpse into my passion and expertise, showcasing just a taste of how I bring data to life.
                """)
    # add contact me buttons with linkdin and mail 
    st.markdown("""
                **Contact me**\n
                 [![Linkedin](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/syrine-mahdia-flici-6b8774201/)
                 [![Mail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:syrine.flici@gmail.com)
                 [![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Syrina-Akai)
                """)
    
    
if __name__ == '__main__' :
    # add a menu on the left side
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", 'Analyse', 'Data Science', 'About'], 
            icons=['house', 'clipboard2-pulse', 'clipboard2-data', 'info-circle'], menu_icon="cast", default_index=0)
        
    if selected == 'Home':
        home_page()
    if selected == 'Analyse':
        analyse_page()

    if selected == 'Data Science':
        datascience_page()

    if selected == 'About':
        about_page()


