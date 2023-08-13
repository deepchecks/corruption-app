import openai
from deepchecks.nlp.utils.text_properties import readability_score
from utils.openai_utils import get_answers_with_backoff

openai.api_key = "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"

def corrupt_readability(model_response, model_response_readability_score, difference = 15, max_iter = 3):

    async def _process(model_response, model_response_readability_score, difference, max_iter):
        if max_iter == 0:
            return model_response.strip()
        decrease_readability_prompt = f"""You are given a piece of text. You need to rewrite the text in such a way that the readability of the text is low or it is very hard to understand the text. Make sure that the generated text is in valid English:

        "{model_response}" 

        Your response should only contain the modified text."""

        response = await get_answers_with_backoff(decrease_readability_prompt)
        modified_response_readability_score = readability_score(response)
        if abs(modified_response_readability_score - model_response_readability_score) >= difference:
            return response.strip()
        return await _process(response, model_response_readability_score, difference - difference * 0.2, max_iter - 1)

    return _process(model_response, model_response_readability_score, difference, max_iter)

