import streamlit as st
from utils.config import update_config
import time


def create_settings(config):
    st.header('Settings')
    st.markdown("""Update your Deepchecks LLM application name and version name below:""")
    with st.form('config update'):
        toxicity = st.slider("Toxicity", 0, 10, int(config['TOXICITY']))
        avoided_answer = st.slider("Avoided Answer", 0, 10, int(config['AVOIDANCE']))
        relevance = st.slider("Relevance", 0, 10, int(config['RELEVANCE']))
        readability = st.slider("Readability", 0, 10, int(config['READABILITY']))
        hallucination = st.slider("Hallucination", 0, 10, int(config['HALLUCINATIONS']))

        submit_form = st.form_submit_button("Update")
        if submit_form:
            update_config(toxicity, avoided_answer, relevance, readability, hallucination)
    # columns = st.columns(2, gap='large')
    # if config['DEEPCHECKS_LLM_APP_NAME'] not in application_details.keys():
    #     app_names = list(application_details.keys())
    # else:
    #     app_names = [config['DEEPCHECKS_LLM_APP_NAME'], *[key for key in application_details.keys() if key != config['DEEPCHECKS_LLM_APP_NAME']]]

    # with columns[0]:
    #     app_name = st.selectbox('Deepchecks LLM Application Name:', (tuple(app_names)))
    #     if app_name == config['DEEPCHECKS_LLM_APP_NAME']:
    #         app_version = [config['DEEPCHECKS_LLM_APP_VERSION_NAME'], *[key for key in application_details[app_name] if key != config['DEEPCHECKS_LLM_APP_VERSION_NAME']]]
    #     else:
    #         app_version = application_details[app_name]

    # with columns[1]:
    #     version = st.selectbox('Deepchecks LLM Version Name:', (tuple(app_version)))

    # submit_button = st.button('Update', use_container_width=True)
    # if submit_button:
    #     with st.spinner('Updating the app name and version'):
    #         update_config(app_name, version)
    #         dc_client.api = None
    #         time.sleep(2)
