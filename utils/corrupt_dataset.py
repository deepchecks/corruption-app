import pandas as pd
import numpy as np
import streamlit as st


def preprocess_dataset(dataset: pd.DataFrame):
    preprocessed_data = dataset[['input', 'output']]
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
    for idx in range(len(dataset)):
        data = []
        input = dataset.iloc[idx]['input']
        information_retrieval = dataset.iloc[idx]['information_retrieval']
        full_prompt = dataset.iloc[idx]['full_prompt']
        response = dataset.iloc[idx]['output']
        annotation = dataset.iloc[idx]['annotation'] if "annotation" in dataset.columns else ""
        corrupted_record = corrupted_dataset[corrupted_dataset['input'] == input]
        if len(corrupted_record) > 0:
            response = corrupted_record.iloc[0]['corrupted_response']
            annotation = ""
        data.append(input)
        data.append(information_retrieval)
        data.append(full_prompt)
        data.append(response)
        data.append(annotation)
        dataset_to_download.append(data)
    return pd.DataFrame(dataset_to_download, columns=['input', 'information_retrieval', 'full_prompt', 'output', 'annotation'])


def generate_corrupted_dataframe_to_display(corrupted_dataset: pd.DataFrame, MAX_ROWS_PER_PROP: int):

    corrupted_property_count = {prop: 0 for prop in set(corrupted_dataset['corrupted_property'])}
    dataframe_to_display = pd.DataFrame(columns=['input', 'original_response', 'corrupted_response', 'corrupted_property'])
    for idx in range(len(corrupted_dataset)):
        if corrupted_property_count[corrupted_dataset.iloc[idx]['corrupted_property']] >= MAX_ROWS_PER_PROP:
            continue
        corrupted_property_count[corrupted_dataset.iloc[idx]['corrupted_property']] += 1
        df = pd.DataFrame({'input': corrupted_dataset.iloc[idx]['input'],
                           'original_response': corrupted_dataset.iloc[idx]['original_response'],
                           'corrupted_response': corrupted_dataset.iloc[idx]['corrupted_response'],
                           'corrupted_property': corrupted_dataset.iloc[idx]['corrupted_property']})
        dataframe_to_display = pd.concat([dataframe_to_display, df], ignore_index=True)
    return dataframe_to_display
