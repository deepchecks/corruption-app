import streamlit as st
import asyncio
import pandas as pd
import time
from deepchecks.nlp.utils.text_properties import readability_score, sentiment, text_length, toxicity

from utils.corrupt_dataset import preprocess_dataset, randomize_dataset, generate_data_for_corrupt_dataframe, generate_dataset_to_download, display_corrupted_data
from utils.general_utils import display_slider
from algo.readability import corrupt_readability
from algo.relevance import corrupt_relevance
from algo.sentiment import corrupt_sentiment
from algo.text_length import corrupt_text_length
from algo.toxicity import corrupt_toxicity
from algo.hallucination import corrupt_hallucination

# Maximum percentage of samples that can be corrupted per property. This value
# will be used to calculate the range shown on the slider for each property. The range
# displayed denotes the number of samples to corrupt for a given property. 
MAX_PERCENT_OF_SAMPLES_TO_CORRUPT_PER_PROP = 0.05

# Function to reset the session state when the user uploads a new dataset
def reset_session_state():
    st.session_state.corrupted_dataset = pd.DataFrame()

# Function to create the corruption app page
async def create_corrupt_data_page():

    st.header('Corrupt Data')
    st.markdown("""You can upload your data as csv or excel files and corrupt the number of samples per text property.""")

    # Display the upload file and download sample file buttons in a single row
    cols = st.columns([0.7, 0.3])
    with cols[0]:
        upload_file = st.file_uploader("Upload CSV", type=['csv','xls','xlsx'], label_visibility="hidden", on_change=reset_session_state)
    with cols[1]:
        st.markdown('<div style="padding:23px;">',unsafe_allow_html=True)
        st.download_button(label='Example dataset',
                           help='''A csv file with the following columns:\n- user_interaction_id - unique acorss the version (optional) \
                            \n- input - the input to the pipeline \
                            \n- information_retrieval - the information supplied as context to the llm \
                            \n- full_prompt - the full text sent to the LLM \
                            \n- output - the pipeline final output \
                            \n- annotation - either good/bad/empty (optional)''',
                           data = pd.DataFrame(data=[['Input 1', 'IR 1', 'Prompt 1', 'Output 1', 'Good'],
                                                     ['Input 2', 'IR 2', 'Prompt 2', 'Output 2', ''],
                                                     ['Input 3', 'IR 3', 'Prompt 3', 'Output 3', 'Bad']],
                                               columns=['input', 'information_retrieval', 'full_prompt', 'output', 'annotation']).to_csv(index=False).encode('utf-8'),
                           file_name='sample_dataset.csv')
        st.markdown('</div>',unsafe_allow_html=True)

    if upload_file is not None:
        with st.spinner('Uploading dataset...'):
            dataframe = pd.read_csv(upload_file, encoding='latin-1') if upload_file.type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' else pd.read_excel(upload_file)
            is_valid_dataframe = True
            cols_to_check = ['input', 'output']
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
            readability_percent, sentiment_percent, text_length_percent, toxicity_percent, relevance_percent, hallucination_percent = display_slider(MAX_PERCENT_OF_SAMPLES_TO_CORRUPT_PER_PROP)
            corrupt_data = st.button(label='Corrupt Dataset',
                                     key='corrupt_data_button',
                                     help='Corrupt dataset based on the number of samples selected for each property.')
            if corrupt_data:
                st.session_state.readability = int(readability_percent)
                st.session_state.relevance = int(relevance_percent)
                st.session_state.sentiment = int(sentiment_percent)
                st.session_state.text_length = int(text_length_percent)
                st.session_state.hallucination = int(hallucination_percent)
                st.session_state.toxicity = int(toxicity_percent)

                progress_text = "Corrupting the data. Please wait..."
                percent_complete = 0
                corruption_progress_bar = st.progress(0, text=progress_text)
                num_properties_to_corrupt = 1 + (st.session_state.readability and 1) + (st.session_state.relevance and 1) + (st.session_state.sentiment and 1) + \
                                            (st.session_state.text_length and 1) + (st.session_state.toxicity and 1) + (st.session_state.hallucination and 1)
                try:
                    corrupted_dataset = await apply_corruption(percent_complete, corruption_progress_bar, num_properties_to_corrupt)
                    st.session_state.corrupted_dataset = corrupted_dataset
                except Exception as e:
                    corruption_progress_bar.empty()
                    st.write(e)
            if len(st.session_state.corrupted_dataset) > 0:
                display_corrupted_data()
                merged_dataset = generate_dataset_to_download(st.session_state.dataset, st.session_state.corrupted_dataset)
                st.download_button(label='Download corrupted dataset',
                                   data=merged_dataset.to_csv(index=False).encode('utf-8'),
                                   file_name='corrupted_dataset.csv',
                                   help='Download the corrupted dataset ready to upload for LLM evaluation app.')

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

