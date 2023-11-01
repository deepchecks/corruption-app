import streamlit as st
import pandas as pd
import time


def create_settings():
    st.session_state.corrupted_dataset = pd.DataFrame()
    st.session_state.dataset = pd.DataFrame()
    st.header('Settings')
    st.markdown("""Update your OpenAI API key below:""")
    with st.form('config update'):
        submit_form = st.form_submit_button("Update")
        if submit_form:
            with st.spinner('Updating the settings'):
                time.sleep(2)

