from utils.openai_utils import get_answers_with_backoff


def corrupt_relevance(model_response):

    async def _process(model_response):

        corrupt_relevance_prompt = f"""Generate a random piece of text having around {len(model_response.split())} words."""

        response = await get_answers_with_backoff(corrupt_relevance_prompt)
        return response.strip()

    return _process(model_response)

