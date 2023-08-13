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
            with st.spinner('Updating the settings'):
                update_config(toxicity, avoided_answer, relevance, readability, hallucination)
                time.sleep(2)

