from deepchecks.nlp.utils.text_properties import sentiment
from utils.openai_utils import get_answers_with_backoff
from algo.prompts import CORRUPT_SENTIMENT_PROMPT

def corrupt_sentiment(model_response, model_response_sentiment_score, difference = 0.5, max_iter = 3):

    async def _process(model_response, model_response_sentiment_score, difference, max_iter):
        if max_iter == 0:
            return model_response.strip()
        decrease_sentiment_prompt = CORRUPT_SENTIMENT_PROMPT.format(output=model_response)

        response = await get_answers_with_backoff(decrease_sentiment_prompt)
        modified_response_sentiment_score = sentiment(response)
        if modified_response_sentiment_score < model_response_sentiment_score and (model_response_sentiment_score - modified_response_sentiment_score) >= difference:
            return response.strip()
        return await _process(response, model_response_sentiment_score, difference - difference * 0.2, max_iter - 1)

    return _process(model_response, model_response_sentiment_score, difference, max_iter)

