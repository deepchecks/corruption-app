import platform
import pathlib
from PIL import Image
from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import numpy as np
from deepchecks.nlp.utils.text_properties import sentiment, readability_score, text_length

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
                

            /* Corrupt Dataset button */
            [data-testid=tooltipHoverTarget]>button,
            [data-testid=tooltipHoverTarget]>button:focus:not(:active) {
                background-color: #7964FF;
                color: white;
                border: 1px solid #7964FF;
            }
            [data-testid=tooltipHoverTarget]>button:hover,
            [data-testid=tooltipHoverTarget]>button:active {
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


def preprocess_dataset(dataset: pd.DataFrame):
    preprocessed_data = dataset[['user_input', 'response']]
    return preprocessed_data

def randomize_dataset(model_responses: pd.Series,
                      readability_percent: int,
                      relevance_percent: int,
                      sentiment_precent: int,
                      text_length_percent: int):
    percentages = {
        'Readability': readability_percent,
        'Relevance': relevance_percent,
        'Sentiment': sentiment_precent,
        'Text Length': text_length_percent
    }
    total_size = len(model_responses)

    # Generate random indices for the combined sample
    sample_size = int(total_size * (readability_percent + relevance_percent + sentiment_precent + text_length_percent) / 100)
    random_indices = np.random.choice(total_size, size=sample_size, replace=False)

    # Create a dictionary to store the random responses
    random_responses = {}
    start = 0
    for prop in percentages:
        # Calculate the sample size for the current property
        prop_sample_size = int(total_size * percentages[prop] / 100)
        # Use iloc to get the random responses for the current property
        random_responses[prop] = {
            'indices' : list(model_responses.iloc[random_indices[start: start + prop_sample_size]].index),
            'data' : list(model_responses.iloc[random_indices[start: start + prop_sample_size]])
        }
        start += prop_sample_size

    return random_responses


def generate_data_for_corrupt_dataframe(random_data, corrupted_response, corrupted_property):
    corrupted_data_info = []
    for idx, response in enumerate(corrupted_response):
        data = []
        user_input = st.session_state.dataset.iloc[random_data[corrupted_property]['indices'][idx]]['user_input']
        original_response = random_data[corrupted_property]['data'][idx]
        data.append(user_input)
        data.append(original_response)
        data.append(response)
        if corrupted_property == 'Readability':
            data.append(readability_score(original_response))
            data.append(readability_score(response))
        elif corrupted_property == 'Relevance':
            data.append('')
            data.append('')
        elif corrupted_property == 'Sentiment':
            data.append(sentiment(original_response))
            data.append(sentiment(response))
        elif corrupted_property == 'Text Length':
            data.append(text_length(original_response))
            data.append(text_length(response))
        data.append(corrupted_property)
        corrupted_data_info.append(data)
    return corrupted_data_info
