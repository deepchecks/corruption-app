"""Python file to serve as the frontend"""
import streamlit as st
from utils.config import load_config
from utils.general_utils import initialize_app, initialize_session_state
from menu.corrupt import create_corrupt_data_page
from menu.settings import create_settings
import asyncio

try:
    loop = asyncio.get_event_loop()
except RuntimeError as e:
    if str(e).startswith('There is no current event loop in thread'):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    else:
        raise

# Render the sidebar on the UI and add the styling to various components
initialize_app()

# Load the configuration
config = load_config()

# Initialize the session states
initialize_session_state()

# Render the page according to current page
if st.session_state.current_page == 'Settings':
    create_settings(config)
else:
    asyncio.run(create_corrupt_data_page(config))
