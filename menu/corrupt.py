import streamlit as st
import asyncio
import pandas as pd
import time
from st_aggrid import AgGrid, GridOptionsBuilder
from deepchecks.nlp.utils.text_properties import readability_score, sentiment, text_length, toxicity

from utils.corrupt_dataset import preprocess_dataset, randomize_dataset, generate_data_for_corrupt_dataframe, generate_dataset_to_download, generate_corrupted_dataframe_to_display
from algo.readability import corrupt_readability
from algo.relevance import corrupt_relevance
from algo.sentiment import corrupt_sentiment
from algo.text_length import corrupt_text_length
from algo.toxicity import corrupt_toxicity


async def create_corrupt_data_page():

    st.header('Corrupt Data')

    st.markdown("""You can upload your data as csv or excel files and corrupt the data according to the properties in the Settings section""")
    cols = st.columns([0.7, 0.3])
    with cols[0]:
        upload_file = st.file_uploader("Upload CSV", type=['csv','xls','xlsx'], label_visibility="hidden")
    with cols[1]:
        st.markdown('<div style="padding:23px;">',unsafe_allow_html=True)
        st.download_button(label='Example dataset',
                           help='''A csv file with the following columns:\n- user_interaction_id - unique acorss the version (optional) \
                            \n- input - the input to the pipeline \
                            \n- information_retrieval - the information supplied as context to the llm \
                            \n- full_prompt - the full text sent to the LLM \
                            \n- output - the pipeline final output \
                            \n- annotation - either good/bad/empty''',
                           data='hello',
                           file_name='corrupted_dataset.csv')
        st.markdown('</div>',unsafe_allow_html=True)

    if upload_file is not None:
        with st.spinner('Uploading dataset...'):
            dataframe = pd.read_csv(upload_file, encoding='latin-1') if upload_file.type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' else pd.read_excel(upload_file)
            is_valid_dataframe = True
            cols_to_check = ['input', 'information_retrieval', 'full_prompt', 'output', 'annotation']
            for col in cols_to_check:
                if col not in dataframe.columns:
                    is_valid_dataframe = False
                    break
            if not is_valid_dataframe:
                st.warning('The uploaded CSV does not contain all the required columns!!')
                return
            if len(dataframe) > 1000:
                st.warning('Only the first 1000 rows will be considered for corrupting the properties!!')
            if is_valid_dataframe:
                st.session_state.dataset = dataframe.iloc[0: 1000]
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

            corrupt_data = st.button(label='Corrupt Dataset',
                                     key='corrupt_data_button',
                                     help='Corrupt dataset basaed on the percentage of data selected for each property in settings section')
            if corrupt_data:
                st.session_state.readability = int(readability_percent)
                st.session_state.relevance = int(relevance_percent)
                st.session_state.sentiment = int(sentiment_percent)
                st.session_state.text_length = int(text_length_percent)
                st.session_state.hallucination = int(hallucination_percent)
                st.session_state.toxicity = int(toxicity_percent)

                progress_text = "Corrupting the data. Please wait."
                percent_complete = 0
                corruption_progress_bar = st.progress(0, text=progress_text)
                corrupted_data = []
                try:
                    preprocessed_data = preprocess_dataset(st.session_state.dataset)
                    random_data = randomize_dataset(model_responses=preprocessed_data['output'], 
                                                    readability_percent=st.session_state.readability,
                                                    relevance_percent=st.session_state.relevance,
                                                    sentiment_precent=st.session_state.sentiment,
                                                    text_length_percent=st.session_state.text_length,
                                                    toxicity_percent=st.session_state.toxicity)
                    time.sleep(1)
                    percent_complete += 5
                    progress_text = 'Corrupting readability property...' if st.session_state.readability > 0 else progress_text
                    corruption_progress_bar.progress(percent_complete, text=progress_text)
                    readability_api_response = await asyncio.gather(*[corrupt_readability(model_response.strip(), readability_score(model_response.strip())) for model_response in random_data['Readability']['data']])
                    percent_complete += 15
                    progress_text = 'Corrupted readability property successfully...' if st.session_state.readability > 0 else progress_text
                    corruption_progress_bar.progress(percent_complete, text=progress_text)

                    time.sleep(1)
                    percent_complete += 5
                    progress_text = 'Corrupting sentiment property...' if st.session_state.sentiment > 0 else progress_text
                    corruption_progress_bar.progress(percent_complete, text=progress_text)
                    sentiment_api_response = await asyncio.gather(*[corrupt_sentiment(model_response.strip(), sentiment(model_response.strip())) for model_response in random_data['Sentiment']['data']])
                    percent_complete += 15
                    progress_text = 'Corrupted sentiment property successfully...' if st.session_state.sentiment > 0 else progress_text
                    corruption_progress_bar.progress(percent_complete, text=progress_text)

                    time.sleep(1)
                    percent_complete += 5
                    progress_text = 'Corrupting text length property...' if st.session_state.text_length > 0 else progress_text
                    corruption_progress_bar.progress(percent_complete, text=progress_text)
                    text_length_api_response = await asyncio.gather(*[corrupt_text_length(model_response.strip(), text_length(model_response.strip())) for model_response in random_data['Text Length']['data']])
                    percent_complete += 15
                    progress_text = 'Corrupted text length property successfully...' if st.session_state.text_length > 0 else progress_text
                    corruption_progress_bar.progress(percent_complete, text=progress_text)

                    time.sleep(1)
                    percent_complete += 5
                    progress_text = 'Corrupting relevance property...' if st.session_state.relevance > 0 else progress_text
                    corruption_progress_bar.progress(percent_complete, text=progress_text)
                    relevance_api_response = await asyncio.gather(*[corrupt_relevance(model_response.strip()) for model_response in random_data['Relevance']['data']])
                    percent_complete += 15
                    progress_text = 'Corrupted relevance property successfully...' if st.session_state.relevance > 0 else progress_text
                    corruption_progress_bar.progress(percent_complete, text=progress_text)

                    time.sleep(1)
                    percent_complete += 5
                    progress_text = 'Corrupting toxicity property...' if st.session_state.toxicity > 0 else progress_text
                    corruption_progress_bar.progress(percent_complete, text=progress_text)
                    toxicity_api_response = await asyncio.gather(*[corrupt_toxicity(model_response.strip(), toxicity([model_response.strip()], models_storage=st.session_state.toxicity_model_path)[0]) for model_response in random_data['Toxicity']['data']])
                    percent_complete += 10
                    progress_text = 'Corrupted toxicity property successfully...' if st.session_state.toxicity > 0 else progress_text
                    corruption_progress_bar.progress(percent_complete, text=progress_text)

                    time.sleep(1)
                    percent_complete += 3
                    progress_text = 'Generating the corrupted dataset...'
                    corruption_progress_bar.progress(percent_complete, text=progress_text)
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
                    corrupted_data.extend(generate_data_for_corrupt_dataframe(random_data=random_data,
                                                                              corrupted_response=toxicity_api_response,
                                                                              corrupted_property='Toxicity'))
                    corrupted_dataset = pd.DataFrame(corrupted_data, columns=['input', 'original_output', 'corrupted_output', 'corrupted_property'])
                    time.sleep(1)
                    percent_complete += 2
                    progress_text = 'Corrupted dataset generated successfully!!'
                    corruption_progress_bar.progress(percent_complete, text=progress_text)
                    time.sleep(1)
                    corruption_progress_bar.empty()
                    st.session_state.corrupted_dataset = corrupted_dataset
                except Exception as e:
                    corruption_progress_bar.empty()
                    st.write(e)
            if len(st.session_state.corrupted_dataset) > 0:
                dataframe_to_display = generate_corrupted_dataframe_to_display(st.session_state.corrupted_dataset, 2)
                gb = GridOptionsBuilder()
                gb.configure_column('input', 'Input', width=100, wrapText=True, autoHeight=True)
                gb.configure_column('original_output', 'Original Output', wrapText=True, autoHeight=True)
                gb.configure_column('corrupted_output', 'Corrupted Output', wrapText=True, autoHeight=True)
                gb.configure_column('corrupted_property', 'Corruption Type', width=80, wrapText=True, autoHeight=True)
                AgGrid(dataframe_to_display, height = 350, fit_columns_on_grid_load=True, gridOptions=gb.build())
                # st.dataframe(dataframe_to_display,
                #              hide_index=True,
                #              column_config={
                #                  'input': st.column_config.TextColumn("Input"),
                #                  'original_output': st.column_config.TextColumn("Original Output"),
                #                  'corrupted_output': st.column_config.TextColumn("Corrupted Output"),
                #                  'corrupted_property': st.column_config.TextColumn("Corruption Type")
                #             })
                merged_dataset = generate_dataset_to_download(st.session_state.dataset, st.session_state.corrupted_dataset)
                st.download_button(label='Download corrupted dataset',
                                   data=merged_dataset.to_csv(index=False).encode('utf-8'),
                                   file_name='corrupted_dataset.csv')


