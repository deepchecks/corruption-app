from deepchecks.nlp.utils.text_properties import toxicity
from utils.openai_utils import get_answers_with_backoff
from algo.prompts import CORRUPT_TOXICITY_PROMPT
import streamlit as st

def corrupt_toxicity(model_response, model_response_toxicity_score, difference = 0.5, max_iter = 3):

    async def _process(model_response, model_response_toxicity_score, difference, max_iter):
        if max_iter == 0:
            return model_response.strip()
        increase_toxicity_prompt = CORRUPT_TOXICITY_PROMPT.format(output=model_response)

        response = await get_answers_with_backoff(increase_toxicity_prompt)
        modified_response_toxicity_score = toxicity([response], models_storage=st.session_state.toxicity_model_path)[0]
        if abs(modified_response_toxicity_score - model_response_toxicity_score) >= difference:
            return response.strip()
        return await _process(response, model_response_toxicity_score, difference - difference * 0.2, max_iter - 1)

    return _process(model_response, model_response_toxicity_score, difference, max_iter)