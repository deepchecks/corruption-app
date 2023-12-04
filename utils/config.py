from dotenv import dotenv_values
import os

def load_config():
    """Load all the required credentials from the .env file or streamlit cloud.

    Returns
    -------
    OrderDict containing all the variables from the .env file.
    """
    env = dotenv_values(".env")
    os.environ['OPENAI_API_KEY'] = env["OPENAI_API_KEY"]

