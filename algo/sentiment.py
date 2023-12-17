from deepchecks.nlp.utils.text_properties import sentiment

from algo.prompts import CORRUPT_SENTIMENT_PROMPT
from utils.openai_utils import get_answers_with_backoff


def corrupt_sentiment(output, model_output_sentiment_score, difference = 0.5, max_iter = 3):

    async def _process(output, model_output_sentiment_score, difference, max_iter):
        if max_iter == 0:
            return output.strip()
        decrease_sentiment_prompt = CORRUPT_SENTIMENT_PROMPT.format(output=output)

        response = await get_answers_with_backoff(decrease_sentiment_prompt)
        modified_output_sentiment_score = sentiment(response)
        if modified_output_sentiment_score < model_output_sentiment_score and (model_output_sentiment_score - modified_output_sentiment_score) >= difference:
            return response.strip()
        return await _process(response, model_output_sentiment_score, difference - difference * 0.2, max_iter - 1)

    return _process(output, model_output_sentiment_score, difference, max_iter)

