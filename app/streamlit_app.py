import streamlit as st
from streamlit_option_menu import option_menu
from app_functions import *
from page_infos import display_informations
from page_interactive_plots import interactive_plots
from page_download_plots import download_plots


def navigation_bar():

    styles_settings = {'icon': {"color": "#223170"},
                       'nav-link': {"--hover-color": "#edf0fa"},
                       'nav-link-selected': {'background-color': '#edf0fa', "color": '#223170'}}

    with st.sidebar:

        st.markdown('<div style="font-size: 24px; color:#223170"><b>Navigation:<b></div>', unsafe_allow_html=True)

        page = option_menu('', menu_icon='', options=['Informations', 'Interactive plot', 'Download plot(s)'],
                           icons=['info-circle-fill', 'card-image', 'file-earmark-arrow-down-fill'],
                           styles=styles_settings)

    return page


def app_settings():

    st.set_page_config(layout="wide", page_title='C.elegans trans-splicing', page_icon='🔬')

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                .css-1d391kg {padding-top: 4rem; padding-bottom: 1rem}
                .css-18e3th9 {padding-top: 3rem; padding-bottom: 1rem}
                .appview-container .main .block-container {max-width: 1000px; padding-top: 0.5rem; padding-right: 1.5rem; padding-left: 1.5rem; padding-bottom: 2rem;}
                </style>
                """

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def main():

    # general settings
    app_settings()

    # choose page to show
    page = navigation_bar()

    # display selected page
    if page == 'Informations':
        display_informations()

    elif page == 'Interactive plot':
        interactive_plots()

    elif page == 'Download plot(s)':
        download_plots()


if __name__ == '__main__':
    main()