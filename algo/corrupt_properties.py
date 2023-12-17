import asyncio
import time

import pandas as pd
import streamlit as st
from deepchecks.nlp.utils.text_properties import (readability_score, sentiment,
                                                  text_length, toxicity)

from algo.hallucination import corrupt_hallucination
from algo.readability import corrupt_readability
from algo.relevance import corrupt_relevance
from algo.sentiment import corrupt_sentiment
from algo.text_length import corrupt_text_length
from algo.toxicity import corrupt_toxicity
from utils.corrupt_dataset import (generate_data_for_corrupt_dataframe,
                                   preprocess_dataset, randomize_dataset)


# Function to apply the corruption to samples as per each of the property selected
async def apply_corruption(percent_complete, corruption_progress_bar, num_properties_to_corrupt):

    preprocessed_data = preprocess_dataset(st.session_state.dataset)

    random_data = randomize_dataset(model_responses=preprocessed_data['output'], 
                                    num_readability_samples=st.session_state.readability,
                                    num_relevance_samples=st.session_state.relevance,
                                    num_sentiment_samples=st.session_state.sentiment,
                                    num_text_length_samples=st.session_state.text_length,
                                    num_toxicity_samples=st.session_state.toxicity,
                                    num_hallucination_samples=st.session_state.hallucination)
    corrupted_data = []

    if st.session_state.readability:
        time.sleep(1)
        percent_complete += int(100 * 0.5/num_properties_to_corrupt)
        corruption_progress_bar.progress(percent_complete, text='Corrupting readability property...')
        readability_api_response = await asyncio.gather(*[corrupt_readability(model_response.strip(), readability_score(model_response.strip())) for model_response in random_data['Readability']['data']])
        percent_complete += int(100 * 0.5/num_properties_to_corrupt)
        corruption_progress_bar.progress(percent_complete, text='Corrupted readability property successfully...')
        corrupted_data.extend(generate_data_for_corrupt_dataframe(random_data=random_data,
                                                                  corrupted_response=readability_api_response,
                                                                  corrupted_property='Readability'))

    if st.session_state.sentiment:
        time.sleep(1)
        percent_complete += int(100 * 0.5/num_properties_to_corrupt)
        corruption_progress_bar.progress(percent_complete, text='Corrupting sentiment property...')
        sentiment_api_response = await asyncio.gather(*[corrupt_sentiment(model_response.strip(), sentiment(model_response.strip())) for model_response in random_data['Sentiment']['data']])
        percent_complete += int(100 * 0.5/num_properties_to_corrupt)
        corruption_progress_bar.progress(percent_complete, text='Corrupted sentiment property successfully...')
        corrupted_data.extend(generate_data_for_corrupt_dataframe(random_data=random_data,
                                                                  corrupted_response=sentiment_api_response,
                                                                  corrupted_property='Sentiment'))

    if st.session_state.text_length:
        time.sleep(1)
        percent_complete += int(100 * 0.5/num_properties_to_corrupt)
        corruption_progress_bar.progress(percent_complete, text='Corrupting text length property...')
        text_length_api_response = await asyncio.gather(*[corrupt_text_length(model_response.strip(), text_length(model_response.strip())) for model_response in random_data['Text Length']['data']])
        percent_complete += int(100 * 0.5/num_properties_to_corrupt)
        corruption_progress_bar.progress(percent_complete, text='Corrupted text length property successfully...')
        corrupted_data.extend(generate_data_for_corrupt_dataframe(random_data=random_data,
                                                                  corrupted_response=text_length_api_response,
                                                                  corrupted_property='Text Length'))

    if st.session_state.relevance:
        time.sleep(1)
        percent_complete += int(100 * 0.5/num_properties_to_corrupt)
        corruption_progress_bar.progress(percent_complete, text='Corrupting relevance property...')
        relevance_api_response = await asyncio.gather(*[corrupt_relevance(model_response.strip()) for model_response in random_data['Relevance']['data']])
        percent_complete += int(100 * 0.5/num_properties_to_corrupt)
        corruption_progress_bar.progress(percent_complete, text='Corrupted relevance property successfully...')
        corrupted_data.extend(generate_data_for_corrupt_dataframe(random_data=random_data,
                                                                  corrupted_response=relevance_api_response,
                                                                  corrupted_property='Relevance'))

    if st.session_state.toxicity:
        time.sleep(1)
        percent_complete += int(100 * 0.5/num_properties_to_corrupt)
        corruption_progress_bar.progress(percent_complete, text='Corrupting toxicity property...')
        toxicity_api_response = await asyncio.gather(*[corrupt_toxicity(model_response.strip(), toxicity([model_response.strip()], models_storage=st.session_state.toxicity_model_path)[0]) for model_response in random_data['Toxicity']['data']])
        percent_complete += int(100 * 0.5/num_properties_to_corrupt)
        corruption_progress_bar.progress(percent_complete, text='Corrupted toxicity property successfully...')
        corrupted_data.extend(generate_data_for_corrupt_dataframe(random_data=random_data,
                                                                  corrupted_response=toxicity_api_response,
                                                                  corrupted_property='Toxicity'))

    if st.session_state.hallucination:
        time.sleep(1)
        percent_complete += int(100 * 0.5/num_properties_to_corrupt)
        corruption_progress_bar.progress(percent_complete, text='Corrupting hallucination property...')
        hallucination_api_response = await asyncio.gather(*[corrupt_hallucination(preprocessed_data.iloc[random_data['Hallucination']['indices'][idx]]['input'], model_response.strip()) for idx, model_response in enumerate(random_data['Hallucination']['data'])])
        percent_complete += int(100 * 0.5/num_properties_to_corrupt)
        corruption_progress_bar.progress(percent_complete, text='Corrupted hallucination property successfully...')
        corrupted_data.extend(generate_data_for_corrupt_dataframe(random_data=random_data,
                                                                  corrupted_response=hallucination_api_response,
                                                                  corrupted_property='Hallucination'))

    time.sleep(1)
    percent_complete += int(100 * 0.5/num_properties_to_corrupt)
    corruption_progress_bar.progress(percent_complete, text='Generating the corrupted dataset...')
    corrupted_dataset = pd.DataFrame(corrupted_data, columns=['input', 'original_output', 'corrupted_output', 'corrupted_property'])
    time.sleep(1)
    percent_complete = 100
    corruption_progress_bar.progress(percent_complete, text='Corrupted dataset generated successfully...')
    time.sleep(1)
    corruption_progress_bar.empty()
    return corrupted_dataset

