from deepchecks.nlp.utils.text_properties import readability_score
from utils.openai_utils import get_answers_with_backoff
from algo.prompts import CORRUPT_READABILITY_PROMPT

def corrupt_readability(model_response, model_response_readability_score, difference = 15, max_iter = 3):

    async def _process(model_response, model_response_readability_score, difference, max_iter):
        if max_iter == 0:
            return model_response.strip()
        decrease_readability_prompt = CORRUPT_READABILITY_PROMPT.format(output=model_response)

        response = await get_answers_with_backoff(decrease_readability_prompt)
        modified_response_readability_score = readability_score(response)
        if abs(modified_response_readability_score - model_response_readability_score) >= difference:
            return response.strip()
        return await _process(response, model_response_readability_score, difference - difference * 0.2, max_iter - 1)

    return _process(model_response, model_response_readability_score, difference, max_iter)

