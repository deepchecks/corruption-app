from deepchecks.nlp.utils.text_properties import text_length
from utils.openai_utils import get_answers_with_backoff
from algo.prompts import CORRUPT_TEXT_LENGTH_PROMPT

def corrupt_text_length(model_response, model_response_text_length_score, difference = 250, max_iter = 3):

    async def _process(model_response, model_response_text_length_score, difference, max_iter):
        if max_iter == 0:
            return model_response.strip()
        decrease_text_length_prompt = CORRUPT_TEXT_LENGTH_PROMPT.format(model_response=model_response,
                                                                        min_number_of_words=len(model_response.split()),
                                                                        max_number_of_words=len(model_response.split()) + difference)

        response = await get_answers_with_backoff(decrease_text_length_prompt)
        modified_response_text_length_score = text_length(response)
        if modified_response_text_length_score > model_response_text_length_score and (modified_response_text_length_score - model_response_text_length_score) >= difference:
            return response.strip()
        return await _process(response, model_response_text_length_score, difference - 50, max_iter - 1)

    return _process(model_response, model_response_text_length_score, difference, max_iter)

