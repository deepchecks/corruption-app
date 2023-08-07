import platform
import pathlib
from PIL import Image
from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu

if platform.system() == 'Windows':
    pathlib.PosixPath = pathlib.WindowsPath


def initialize_app():
    with Image.open('./assets/favicon.ico') as icon:
        icon.load()
    logo = Path('./assets/dc-llm-logo.svg').read_text()
    logo_with_link = f'<a href="https://deepchecks.com/get-early-access-deepchecks-llm-evaluation/" target="_blank">{logo}</a>'

    st.set_page_config(page_title="Q&A HR Chatbot", page_icon=icon, layout='wide')
    st.sidebar.markdown(logo_with_link, unsafe_allow_html=True)
    with st.sidebar:
        page = option_menu(
                    "",  # empty title
                    ["Ask Deepy", "Settings"],
                    icons=['robot', 'gear-fill'],
                    # https://icons.getbootstrap.com/
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
        st.session_state.current_page = page
    st.markdown("""
        <style>
            /* Sidebar */
            [data-testid=stSidebar] {
                background-color: #D8DDE1;
            }

            /* Submit Form button */
            [data-testid=stFormSubmitButton]>button {
                background-color: #7964FF;
                border: 1px solid #7964FF;
            }
            [data-testid=stFormSubmitButton]>button:hover,
            [data-testid=stFormSubmitButton]>button:active {
                background-color: #7964FF;
                opacity: 90%;
                color: white;
                border: 1px solid #7964FF;
            }

            /* Good annotation button */    
            [data-testid=column]:nth-child(1) button {
                color: white;
                background-color: #37A862;
            }
            [data-testid=column]:nth-child(1) button:hover,
            [data-testid=column]:nth-child(1) button:active,
            [data-testid=column]:nth-child(1) button:focus:not(:active) {
                color: white;
                background-color: #37A862;
                opacity: 95%;
                border: 1px solid #37A862;
            }

            /* Bad annotation button */    
            [data-testid=stVerticalBlock]>div>div:nth-child(2) button{
                color: white;
                background-color: #FC636B;
            }
            [data-testid=stVerticalBlock]>div>div:nth-child(2) button:hover,
            [data-testid=stVerticalBlock]>div>div:nth-child(2)  button:active,
            [data-testid=stVerticalBlock]>div>div:nth-child(2)  button:focus:not(:active) {
                color: white;
                background-color: #FC636B;
                opacity: 95%;
                border: 1px solid #FC636B;
            }

            /* Both annotation buttons*/
            [data-testid=stVerticalBlock]>div>div>button {
                background-color: white;
                border-radius: 1.0rem;
            }
                
            /* Update settings button*/
            [data-testid=stVerticalBlock]>div>div>button {
                background-color: #7964FF;
                border: 1px solid #7964FF;
                color: white;
            }
            
            [data-testid=stVerticalBlock]>div>div>button:hover,
            [data-testid=stVerticalBlock]>div>div>button:focus:not(:active),
            [data-testid=stVerticalBlock]>div>div>button:active {
                background-color: #7964FF;
                opacity: 90%;
                color: white;
                border: 1px solid #7964FF;
            }
        </style>
        """, unsafe_allow_html=True)    


def initialize_session_state():
    if "is_annotated" not in st.session_state:
        st.session_state.is_annotated = False
    if "annotation_message" not in st.session_state:
        st.session_state.annotation_message = ""
    if "llm_response" not in st.session_state:
        st.session_state.llm_response = ""
    if "ext_interaction_id" not in st.session_state:
        st.session_state.ext_interaction_id = ""
    if "reload_settings_form" not in st.session_state:
        st.session_state.reload_settings_form = False
    if "current_page" not in  st.session_state:
        st.session_state.current_page = ""
    if "application_details" not in st.session_state:
        st.session_state.application_details = {}