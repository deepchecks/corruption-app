from deepchecks.nlp.utils.text_properties import text_length
from utils.openai_utils import get_answers_with_backoff


def corrupt_text_length(model_response, model_response_text_length_score, difference = 250, max_iter = 3):

    async def _process(model_response, model_response_text_length_score, difference, max_iter):
        if max_iter == 0:
            return model_response.strip()
        decrease_text_length_prompt = f"""You are given a piece of text. You need to rewrite the text in such a way that the number of words in the generated text is more than {len(model_response.split())} words and less than {len(model_response.split()) + difference} words. Make sure that the generated text is in valid English:

        "{model_response}" 

        Your response should only contain the modified text."""

        response = await get_answers_with_backoff(decrease_text_length_prompt)
        modified_response_text_length_score = text_length(response)
        if modified_response_text_length_score > model_response_text_length_score and (modified_response_text_length_score - model_response_text_length_score) >= difference:
            return response.strip()
        return await _process(response, model_response_text_length_score, difference - 50, max_iter - 1)

    return _process(model_response, model_response_text_length_score, difference, max_iter)

