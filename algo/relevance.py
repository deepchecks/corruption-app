from utils.openai_utils import get_answers_with_backoff
from algo.prompts import CORRUP_RELEVANCE_PROMPT

def corrupt_relevance(model_response):

    async def _process(model_response):

        corrupt_relevance_prompt = CORRUP_RELEVANCE_PROMPT.format(number_of_words=len(model_response.split()))

        response = await get_answers_with_backoff(corrupt_relevance_prompt)
        return response.strip()

    return _process(model_response)

