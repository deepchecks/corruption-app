import streamlit as st
from deepchecks.nlp.utils.text_properties import toxicity

from algo.prompts import CORRUPT_TOXICITY_PROMPT
from utils.openai_utils import get_answers_with_backoff


def corrupt_toxicity(output, model_output_toxicity_score, difference = 0.5, max_iter = 3):

    async def _process(output, model_output_toxicity_score, difference, max_iter):
        if max_iter == 0:
            return output.strip()
        increase_toxicity_prompt = CORRUPT_TOXICITY_PROMPT.format(output=output)

        response = await get_answers_with_backoff(increase_toxicity_prompt)
        modified_output_toxicity_score = toxicity([response], models_storage=st.session_state.toxicity_model_path)[0]
        if abs(modified_output_toxicity_score - model_output_toxicity_score) >= difference:
            return response.strip()
        return await _process(response, model_output_toxicity_score, difference - difference * 0.2, max_iter - 1)

    return _process(output, model_output_toxicity_score, difference, max_iter)