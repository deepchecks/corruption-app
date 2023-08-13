import streamlit as st
import pandas as pd
from utils.general_utils import preprocess_dataset, randomize_dataset, generate_data_for_corrupt_dataframe
from deepchecks.nlp.utils.text_properties import readability_score
from algo.readability import corrupt_readability
from algo.relevance import corrupt_relevance
import asyncio

async def create_corrupt_data_page(config):

    st.header('Corrupt Data')

    st.markdown("""You can upload your data as csv or excel files and corrupt the data according to the properties in the Settings section""")
    upload_file = st.file_uploader("Upload CSV", type=['csv','xls','xlsx'])
    if upload_file is not None:
        with st.spinner('Uploading dataset...'):
            dataframe = pd.read_csv(upload_file, encoding='latin-1') if upload_file.type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' else pd.read_excel(upload_file)
            st.session_state.dataset = dataframe
    if len(st.session_state.dataset) > 0:
        st.write(st.session_state.dataset)
        corrupt_data = st.button('Corrupt Dataset', help='Corrupt dataset basaed on the percentage of data selected for each property in settings section', use_container_width=True)
        if corrupt_data:
            with st.spinner('Calculating the properties'):
                corrupted_data = []
                preprocessed_data = preprocess_dataset(st.session_state.dataset)
                random_data = randomize_dataset(preprocessed_data['response'], config)
                readability_api_response = await asyncio.gather(*[corrupt_readability(model_response.strip(), readability_score(model_response)) for model_response in random_data['Readability']['data']])
                relevance_api_response = await asyncio.gather(*[corrupt_relevance(model_response.strip()) for model_response in random_data['Relevance']['data']])
                corrupted_data.extend(generate_data_for_corrupt_dataframe(random_data, readability_api_response, 'Readability'))
                corrupted_data.extend(generate_data_for_corrupt_dataframe(random_data, relevance_api_response, 'Relevance'))
                st.write(pd.DataFrame(corrupted_data, columns=['user_input', 'original_response', 'corrupted_response', 'corrupted_property']))
