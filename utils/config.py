import os

from dotenv import dotenv_values


def load_config():
    """Load all the required credentials from the .env file or streamlit cloud.

    Returns
    -------
    OrderDict containing all the variables from the .env file.
    """
    if os.path.exists('.env'):
        config = dotenv_values(".env")
        os.environ['OPENAI_API_KEY'] = config["OPENAI_API_KEY"]
