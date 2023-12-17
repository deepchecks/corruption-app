from algo.prompts import CORRUPT_RELEVANCE_PROMPT
from utils.openai_utils import get_answers_with_backoff


def corrupt_relevance(input, output):

    async def _process(input, output):

        corrupt_relevance_prompt = CORRUPT_RELEVANCE_PROMPT.format(number_of_words=len(output.split()))

        response = await get_answers_with_backoff(corrupt_relevance_prompt)
        return response.strip()

    return _process(input, output)

