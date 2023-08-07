import requests as req
import streamlit as st

def fetch_application_names_with_versions(config):
    """Fetches the application details from Deepechecks' LLM service via the API.

    Parameters
    ----------
    config : Dict
        A dictonary containing the config object having DEEPCHECKS_LLM_API_KEY and
        DEEPCHECKS_LLM_HOST_URL key-values.

    Returns
    -------
    Dictionary
        A dictionary containing the status code, the response text from the API, and the
        application details (application name and version names).
    
    """
    headers = {'Authorization': f'Basic {config["DEEPCHECKS_LLM_API_KEY"]}'}
    response = req.get(f'{config["DEEPCHECKS_LLM_HOST_URL"]}api/v1/applications', headers=headers)
    if response.status_code != 200:
        return response.status_code, response.text, {}

    json_response = response.json()
    if st.session_state.application_details:
        result = {
            'status_code': 200,
            'text': 'Success',
            'application_details': st.session_state.application_details
        }
        return result

    application_details = {}
    for item in json_response:
        if item["name"] not in application_details:
            application_details[item["name"]] = []
        for version in item["versions"]:
            application_details[item["name"]].append(version["name"])
    st.session_state.application_details = application_details

    result = {
        'status_code': response.status_code,
        'text': response.text,
        'application_details': application_details
    }
    return result