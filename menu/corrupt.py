import streamlit as st
import asyncio
import pandas as pd

from utils.general_utils import preprocess_dataset, randomize_dataset, generate_data_for_corrupt_dataframe
from deepchecks.nlp.utils.text_properties import readability_score, sentiment, text_length
from algo.readability import corrupt_readability
from algo.relevance import corrupt_relevance
from algo.sentiment import corrupt_sentiment
from algo.text_length import corrupt_text_length

async def create_corrupt_data_page():

    st.header('Corrupt Data')

    st.markdown("""You can upload your data as csv or excel files and corrupt the data according to the properties in the Settings section""")
    cols = st.columns([0.7, 0.3])
    with cols[0]:
        upload_file = st.file_uploader("Upload CSV", type=['csv','xls','xlsx'], label_visibility="hidden")
    with cols[1]:
        st.markdown('<div style="padding:23px;">',unsafe_allow_html=True)
        st.download_button(label='Example dataset',
                           help='''A csv file with the following columns:\n- user_input - the input to the pipeline \
                            \n- information_retrieval - the information supplied as context to the llm \
                            \n- full_prompt - the full text sent to the LLM \
                            \n- response - the pipeline final output \
                            \n- annotation - either good/bad/empty''',
                           data='hello',
                           file_name='corrupted_dataset.csv')
        st.markdown('</div>',unsafe_allow_html=True)

    if upload_file is not None:
        with st.spinner('Uploading dataset...'):
            dataframe = pd.read_csv(upload_file, encoding='latin-1') if upload_file.type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' else pd.read_excel(upload_file)
            st.session_state.dataset = dataframe
        if len(st.session_state.dataset) > 0:
            row_one = st.columns(3)
            row_two = st.columns(3)
            with row_one[0]:
                readability_percent = st.slider("Readability", 0, 5, st.session_state.readability)
            with row_one[1]:
                sentiment_percent = st.slider("Sentiment", 0, 5, st.session_state.sentiment)
            with row_one[2]:
                text_length_percent = st.slider("Text Length", 0, 5, st.session_state.text_length)
            with row_two[0]:
                toxicity_percent = st.slider("Toxicity", 0, 5, st.session_state.toxicity)
            with row_two[1]:
                relevance_percent = st.slider("Relevance", 0, 5, st.session_state.relevance)
            with row_two[2]:
                hallucination_percent = st.slider("Hallucination", 0, 5, st.session_state.hallucination)

            corrupt_data = st.button('Corrupt Dataset', help='Corrupt dataset basaed on the percentage of data selected for each property in settings section')
            if corrupt_data:
                st.session_state.readability = int(readability_percent)
                st.session_state.relevance = int(relevance_percent)
                st.session_state.sentiment = int(sentiment_percent)
                st.session_state.text_length = int(text_length_percent)

                st.session_state.hallucination = int(hallucination_percent)
                st.session_state.toxicity = int(toxicity_percent)

                with st.spinner('Corrupting the data...'):
                    corrupted_data = []
                    preprocessed_data = preprocess_dataset(st.session_state.dataset)
                    random_data = randomize_dataset(model_responses=preprocessed_data['response'], 
                                                    readability_percent=st.session_state.readability,
                                                    relevance_percent=st.session_state.relevance,
                                                    sentiment_precent=st.session_state.sentiment,
                                                    text_length_percent=st.session_state.text_length)
                    readability_api_response = await asyncio.gather(*[corrupt_readability(model_response.strip(), readability_score(model_response.strip())) for model_response in random_data['Readability']['data']])
                    relevance_api_response = await asyncio.gather(*[corrupt_relevance(model_response.strip()) for model_response in random_data['Relevance']['data']])
                    sentiment_api_response = await asyncio.gather(*[corrupt_sentiment(model_response.strip(), sentiment(model_response.strip())) for model_response in random_data['Sentiment']['data']])
                    text_length_api_response = await asyncio.gather(*[corrupt_text_length(model_response.strip(), text_length(model_response.strip())) for model_response in random_data['Text Length']['data']])
                    corrupted_data.extend(generate_data_for_corrupt_dataframe(random_data=random_data,
                                                                              corrupted_response=readability_api_response,
                                                                              corrupted_property='Readability'))
                    corrupted_data.extend(generate_data_for_corrupt_dataframe(random_data=random_data,
                                                                              corrupted_response=relevance_api_response,
                                                                              corrupted_property='Relevance'))
                    corrupted_data.extend(generate_data_for_corrupt_dataframe(random_data=random_data,
                                                                              corrupted_response=sentiment_api_response,
                                                                              corrupted_property='Sentiment'))
                    corrupted_data.extend(generate_data_for_corrupt_dataframe(random_data=random_data,
                                                                              corrupted_response=text_length_api_response,
                                                                              corrupted_property='Text Length'))
                    corrupted_dataset = pd.DataFrame(corrupted_data, columns=['user_input', 'original_response', 'corrupted_response', 'original_property_value', 'corrupted_property_value', 'corrupted_property'])
                    st.session_state.corrupted_dataset = corrupted_dataset
            if len(st.session_state.corrupted_dataset) > 0:
                st.write(st.session_state.corrupted_dataset)
                st.download_button(label='Download corrupted dataset',
                                   data=st.session_state.corrupted_dataset.to_csv(index=False).encode('utf-8'),
                                   file_name='corrupted_dataset.csv')
