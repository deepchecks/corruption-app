import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder


def preprocess_dataset(dataset: pd.DataFrame):
    preprocessed_data = dataset[['input', 'output']]
    return preprocessed_data

def randomize_dataset(model_responses: pd.Series,
                      num_readability_samples: int,
                      num_relevance_samples: int,
                      num_sentiment_samples: int,
                      num_text_length_samples: int,
                      num_toxicity_samples: int,
                      num_hallucination_samples: int):
    percentages = {
        'Readability': num_readability_samples,
        'Relevance': num_relevance_samples,
        'Sentiment': num_sentiment_samples,
        'Text Length': num_text_length_samples,
        'Toxicity': num_toxicity_samples,
        'Hallucination': num_hallucination_samples,
    }
    total_size = len(model_responses)

    # Generate random indices for the combined sample
    sample_size = num_readability_samples + num_relevance_samples + num_sentiment_samples + num_text_length_samples + num_toxicity_samples + num_hallucination_samples
    random_indices = np.random.choice(total_size, size=sample_size, replace=False)

    # Create a dictionary to store the random responses
    random_responses = {}
    start = 0
    for prop in percentages:
        # Calculate the sample size for the current property
        prop_sample_size = percentages[prop]
        # Use iloc to get the random responses for the current property
        random_responses[prop] = {
            'indices' : list(model_responses.iloc[random_indices[start: start + prop_sample_size]].index),
            'data' : list(model_responses.iloc[random_indices[start: start + prop_sample_size]])
        }
        start += prop_sample_size

    return random_responses

def generate_data_for_corrupt_dataframe(random_data: dict, corrupted_response: pd.DataFrame, corrupted_property: str):
    corrupted_data_info = []

    for idx, response in enumerate(corrupted_response):
        data = []
        input = st.session_state.dataset.iloc[random_data[corrupted_property]['indices'][idx]]['input']
        original_response = random_data[corrupted_property]['data'][idx]
        data.append(input)
        data.append(original_response)
        data.append(response)
        data.append(corrupted_property)
        corrupted_data_info.append(data)
    return corrupted_data_info

def generate_dataset_to_download(dataset: pd.DataFrame, corrupted_dataset: pd.DataFrame):

    dataset_to_download = []
    if 'annotation' not in list(dataset.columns):
        dataset['annotation'] = [''] * len(dataset)
    all_cols = list(dataset.columns)
    for idx in range(len(dataset)):
        data = []
        corrupted_record = corrupted_dataset[corrupted_dataset['input'] == dataset.iloc[idx]['input']]
        for col in all_cols:
            if len(corrupted_record) > 0 and col == 'output':
                data.append(corrupted_record.iloc[0]['corrupted_output'])
            elif len(corrupted_record) > 0 and col == 'annotation':
                data.append('Bad')
            else:
                data.append(dataset.iloc[idx][col])
        dataset_to_download.append(data)
    return pd.DataFrame(dataset_to_download, columns=all_cols)


def generate_corrupted_dataframe_to_display(corrupted_dataset: pd.DataFrame):

    dataframe_to_display = pd.DataFrame(columns=['input', 'original_output', 'corrupted_output', 'corrupted_property'])
    for idx in range(len(corrupted_dataset)):
        df = pd.DataFrame({'input': [corrupted_dataset.iloc[idx]['input']],
                           'original_output': [corrupted_dataset.iloc[idx]['original_output']],
                           'corrupted_output': [corrupted_dataset.iloc[idx]['corrupted_output']],
                           'corrupted_property': [corrupted_dataset.iloc[idx]['corrupted_property']]})
        dataframe_to_display = pd.concat([dataframe_to_display, df], ignore_index=True)
    return dataframe_to_display


def display_corrupted_data():
    dataframe_to_display = generate_corrupted_dataframe_to_display(st.session_state.corrupted_dataset)
    gb = GridOptionsBuilder()
    gb.configure_column('input', 'Input', width=100, wrapText=True, autoHeight=True)
    gb.configure_column('original_output', 'Original Output', wrapText=True, autoHeight=True)
    gb.configure_column('corrupted_output', 'Corrupted Output', wrapText=True, autoHeight=True)
    gb.configure_column('corrupted_property', 'Corruption Type', width=80, wrapText=True, autoHeight=True)
    AgGrid(dataframe_to_display, height=350, fit_columns_on_grid_load=True, gridOptions=gb.build(), enable_enterprise_modules=False)

