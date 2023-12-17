from algo.prompts import CORRUPT_HALLUCINATION_PROMPT
from utils.openai_utils import get_answers_with_backoff


def corrupt_hallucination(input, output):

    async def _process(input, output):

        corrupt_hallucination_prompt = CORRUPT_HALLUCINATION_PROMPT.format(input=input, output=output)

        response = await get_answers_with_backoff(corrupt_hallucination_prompt)
        return response.strip()

    return _process(input, output)

