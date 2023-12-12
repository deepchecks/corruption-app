import platform
import pathlib
from PIL import Image
from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd

if platform.system() == 'Windows':
    pathlib.PosixPath = pathlib.WindowsPath


def initialize_app():
    with Image.open('./assets/favicon.ico') as icon:
        icon.load()
    logo = Path('./assets/dc-llm-logo.svg').read_text()
    logo_with_link = f'<a href="https://deepchecks.com/get-early-access-deepchecks-llm-evaluation/" target="_blank">{logo}</a>'

    st.set_page_config(page_title="Corrupt Dataset", page_icon=icon, layout='wide')
    st.sidebar.markdown(logo_with_link, unsafe_allow_html=True)
    with st.sidebar:
        page = option_menu(
                    "",  # empty title
                    ["Corrupt Data"],
                    icons=['robot'],
                    default_index=0,
                    styles={
                        "container": {"border-radius": "1"},
                        "icon": {"color": "black", "font-size": "25px"},
                        "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee",
                                    "color": "black"},
                        "nav-link-selected": {"background-color": "rgba(0, 0, 0, 0.1)", "border-radius": "10px",
                                            "color": "black"}
            }
        )
    st.markdown("""
        <style>
            /* Sidebar */
            [data-testid=stSidebar] {
                background-color: #D8DDE1;
            }

            /* Upload dataset button */
            [data-testid=stFileUploadDropzone]>button,
            [data-testid=stFileUploadDropzone]>button:focus:not(:active) {
                background-color: #7964FF;
                color: white;
                border: 1px solid #7964FF;
            }
            [data-testid=stFileUploadDropzone]>button:hover,
            [data-testid=stFileUploadDropzone]>button:active {
                background-color: #7964FF;
                color: white;
                opacity: 90%;
                border: 1px solid #7964FF;
            }
                

            /* Corrupt dataset and download corrupted dataset button */
            [data-testid=tooltipHoverTarget]>button,
            [data-testid=stDownloadButton]>button,
            [data-testid=stDownloadButton]>button:focus:not(:active),
            [data-testid=tooltipHoverTarget]>button:focus:not(:active) {
                background-color: #7964FF;
                color: white;
                border: 1px solid #7964FF;
            }
            [data-testid=tooltipHoverTarget]>button:hover,
            [data-testid=tooltipHoverTarget]>button:active,
            [data-testid=stDownloadButton]>button:hover,
            [data-testid=stDownloadButton]>button:active {
                background-color: #7964FF;
                color: white;
                opacity: 90%;
                border: 1px solid #7964FF;
            }

        </style>
        """, unsafe_allow_html=True)    


def initialize_session_state():
    if "dataset" not in st.session_state:
        st.session_state.dataset = pd.DataFrame()
    if "corrupted_dataset" not in st.session_state:
        st.session_state.corrupted_dataset = pd.DataFrame()
    if "relevance" not in st.session_state:
        st.session_state.relevance = 0
    if "readability" not in st.session_state:
        st.session_state.readability = 0
    if "sentiment" not in st.session_state:
        st.session_state.sentiment = 0
    if "text_length" not in st.session_state:
        st.session_state.text_length = 0
    if "text_style" not in st.session_state:
        st.session_state.text_style = 0
    if "toxicity" not in st.session_state:
        st.session_state.toxicity = 0
    if "hallucination" not in st.session_state:
        st.session_state.hallucination = 0

