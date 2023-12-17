from deepchecks.nlp.utils.text_properties import text_length

from algo.prompts import CORRUPT_TEXT_LENGTH_PROMPT
from utils.openai_utils import get_answers_with_backoff


def corrupt_text_length(output, model_output_text_length_score, difference = 250, max_iter = 3):

    async def _process(output, model_output_text_length_score, difference, max_iter):
        if max_iter == 0:
            return output.strip()
        decrease_text_length_prompt = CORRUPT_TEXT_LENGTH_PROMPT.format(output=output,
                                                                        min_number_of_words=len(output.split()),
                                                                        max_number_of_words=len(output.split()) + difference)

        response = await get_answers_with_backoff(decrease_text_length_prompt)
        modified_output_text_length_score = text_length(response)
        if modified_output_text_length_score > model_output_text_length_score and (modified_output_text_length_score - model_output_text_length_score) >= difference:
            return response.strip()
        return await _process(response, model_output_text_length_score, difference - 50, max_iter - 1)

    return _process(output, model_output_text_length_score, difference, max_iter)

