from deepchecks.nlp.utils.text_properties import readability_score

from algo.prompts import CORRUPT_READABILITY_PROMPT
from utils.openai_utils import get_answers_with_backoff


def corrupt_readability(output, model_output_readability_score, difference = 30, max_iter = 3):

    async def _process(ouptut, model_output_readability_score, difference, max_iter):
        if max_iter == 0:
            return ouptut.strip()
        decrease_readability_prompt = CORRUPT_READABILITY_PROMPT.format(output=ouptut)

        response = await get_answers_with_backoff(decrease_readability_prompt)
        modified_output_readability_score = readability_score(response)
        if abs(modified_output_readability_score - model_output_readability_score) >= difference:
            return response.strip()
        return await _process(response, model_output_readability_score, difference - difference * 0.2, max_iter - 1)

    return _process(output, model_output_readability_score, difference, max_iter)

