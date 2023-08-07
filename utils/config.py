from dotenv import dotenv_values
import os
from configparser import ConfigParser 

def load_config():
    """Load all the required credentials from the .env file or streamlit cloud.

    Returns
    -------
    OrderDict containing all the variables from the .env file.
    """
    if os.path.exists('.env'):
        config = dotenv_values(".env")
        os.environ['OPENAI_API_KEY'] = config["OPENAI_API_KEY"]

    cp = ConfigParser()
    cp.read('./config.ini')
    config['TOXICITY'] = cp.get('CORRUPT_PROPERTIES', 'TOXICITY')
    config['AVOIDANCE'] = cp.get('CORRUPT_PROPERTIES', 'AVOIDANCE')
    config['RELEVANCE'] = cp.get('CORRUPT_PROPERTIES', 'RELEVANCE')
    config['READABILITY'] = cp.get('CORRUPT_PROPERTIES', 'READABILITY')
    config['HALLUCINATIONS'] = cp.get('CORRUPT_PROPERTIES', 'HALLUCINATIONS')
    return config

def update_config(toxicity_percent, avoidance_percent, relevance_percent, readability_percent, hallucinations_percent):
    # Write the updated environment variables to the .env file
    cp = ConfigParser()
    cp.read('./config.ini')
    cp.set('CORRUPT_PROPERTIES', 'TOXICITY', str(toxicity_percent))
    cp.set('CORRUPT_PROPERTIES', 'AVOIDANCE', str(avoidance_percent))
    cp.set('CORRUPT_PROPERTIES', 'RELEVANCE', str(relevance_percent))
    cp.set('CORRUPT_PROPERTIES', 'READABILITY', str(readability_percent))
    cp.set('CORRUPT_PROPERTIES', 'HALLUCINATIONS', str(hallucinations_percent))
    with open('config.ini', 'w') as configfile:
        cp.write(configfile)
