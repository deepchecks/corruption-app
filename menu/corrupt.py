import pandas as pd
import streamlit as st

from algo.corrupt_properties import apply_corruption
from utils.corrupt_dataset import (display_corrupted_data,
                                   generate_dataset_to_download)
from utils.general_utils import display_slider

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


