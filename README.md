# Deepchecks Corruption App

<img src="./assets/deepchecks_llm_app.svg">

🤖 Corrupt text properties and utilize the corrupted dataset with Deepchecks LLM Evaluation app 🤖

- [Corruption App description](#corruption-app-description)
- [Environment Setup](#environment-setup)
- [How to use the application?](#how-to-use-the-application)
- [Deploy the app to Streamlit](#deploy-the-app-to-streamlit)


# Corruption App description
This application helps you to corrupt your LLM dataset containing at least the user input and the LLM model output according to the following text properties: readability, sentiment, text length, toxicity, relevance, and hallucination. The application utilized GPT-3.5 model to corrupt the LLM responses and the properties selected for corruption.


# Environment Setup

The application works on Windows, Linux, and Mac. In order to set up your environment, you can create a virtual environment and install all requirements:

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then rename the `.env.example` file to `.env` and update the following keys as follows:

```python
# Get the OpenAI API key
OPENAI_API_KEY='<YOUR_OPENAI_API_KEY>'
```

Now, you are ready to start the streamlit app locally by running the following command:
```python
streamlit run main.py
```

# How to use the application?
You can follow the steps mentioned below:
1. Upload the LLM dataset as per the given format. You can download the sample dataset and make sure that your dataset has at least two columns: `input` and `output`. 
> If your dataset contains more than 1000 rows, only the first 1000 rows will be considered.
2. After you upload the dataset, you can select the number of samples per property that needs to be corrupted and click on the "Corrupt Dataset" button.
3. Wait for the process to finish and view the corrupted samples. If all looks good, you can download the corrupted dataset and upload it to the Deepchecks LLM evaluation app.

# Deploy the app to Streamlit
The code to run the StreamLit app is in `main.py`. Note that when setting up your StreamLit app you should make sure to add all the environment variables in your `.env` file as a secret environment variable as Secrets in Settings of your deployed Streamlit app.
