from deepchecks.nlp.utils.text_properties import sentiment
from utils.openai_utils import get_answers_with_backoff


def corrupt_sentiment(model_response, model_response_sentiment_score, difference = 0.5, max_iter = 3):

    async def _process(model_response, model_response_sentiment_score, difference, max_iter):
        if max_iter == 0:
            return model_response.strip()
        decrease_sentiment_prompt = f"""You are given a piece of text. You need to rewrite the text in such a way that sentiment of the below text becomes more negative in sentiment. Make sure that the generated text is in valid English:

        "{model_response}" 

        Your response should only contain the modified text."""

        response = await get_answers_with_backoff(decrease_sentiment_prompt)
        modified_response_sentiment_score = sentiment(response)
        if modified_response_sentiment_score < model_response_sentiment_score and (model_response_sentiment_score - modified_response_sentiment_score) >= difference:
            return response.strip()
        return await _process(response, model_response_sentiment_score, difference - difference * 0.2, max_iter - 1)

    return _process(model_response, model_response_sentiment_score, difference, max_iter)

