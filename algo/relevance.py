import openai
from utils.openai_utils import get_answers_with_backoff

openai.api_key = "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"

def corrupt_relevance(model_response, difference = 15, max_iter = 3):

    async def _process(model_response, difference, max_iter):

        corrupt_relevance_prompt = f"""Generate a random piece of text having around {len(model_response.split())} words."""

        response = await get_answers_with_backoff(corrupt_relevance_prompt)
        return response.strip()

    return _process(model_response, difference, max_iter)

