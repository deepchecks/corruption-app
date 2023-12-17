import os

import openai
from tenacity import (retry, stop_after_attempt, stop_after_delay,
                      wait_random_exponential)


@retry(wait=wait_random_exponential(min=1, max=30), stop=stop_after_attempt(5) | stop_after_delay(60))
async def get_answers_with_backoff(user_message, system_message = None, max_tokens=1024, temperature = 0.7):

        if system_message:
            messages = [{"role": "system", "content": system_message}, {"role": "user", "content": user_message}]
        else:
            messages = [{"role": "user", "content": user_message}]

        response = await openai.ChatCompletion.acreate(model='gpt-3.5-turbo', max_tokens=max_tokens,
                                                       api_key=os.environ['OPENAI_API_KEY'],
                                                       messages=messages, temperature=temperature)
        response = response['choices'][0]['message']['content']
        return response