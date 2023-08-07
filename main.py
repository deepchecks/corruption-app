"""Python file to serve as the frontend"""
import streamlit as st
# from utils.config import load_config
from utils.general_utils import initialize_app, initialize_session_state
from menu.corrupt import create_ask_deepy_bot
from menu.settings import create_settings
# from utils.api_call import fetch_application_names_with_versions

# Render the sidebar on the UI and add the styling to various components
initialize_app()

# Load the configuration
# config = load_config()

initialize_session_state()

# deepchecks_llm_app_name = config['DEEPCHECKS_LLM_APP_NAME']
# deepchecks_llm_version_name = config['DEEPCHECKS_LLM_APP_VERSION_NAME']
# response = fetch_application_names_with_versions(config)

# if (deepchecks_llm_app_name not in list(response['application_details'].keys()) or deepchecks_llm_version_name not in response['application_details'][deepchecks_llm_app_name]) and st.session_state.current_page != 'Settings':
#     st.header('Q&A HR Chatbot')
#     st.error('Your Deepchecks LLM app name and version names are not correct. Please update it from the Settings section.')
# elif response['status_code'] != 200:
#     st.error({'status_code': response['status_code'], 'text': response['text'], 'solution': 'Make sure that your API keys are correct.'})
# else:
#     if dc_client.api is None:
#         initialize_deepchecks_client(config)

if st.session_state.current_page == 'Settings':
    st.session_state.is_annotated = False
    st.session_state.annotation_message = ""
    st.session_state.llm_response = ""
    st.session_state.ext_interaction_id = ""
    create_settings()
else:
    create_ask_deepy_bot()
