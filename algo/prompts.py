CORRUPT_READABILITY_PROMPT = """You are given a piece of text. You need to rewrite the text in such a way that the readability of the text is low or it is very hard to understand the text. Make sure that the generated text is in valid English:

        "{model_response}" 

        Your response should only contain the modified text."""


CORRUPT_TEXT_LENGTH_PROMPT = """You are given a piece of text. You need to rewrite the text in such a way that the number of words in the generated text is more than {min_number_of_words} words and less than {max_number_of_words} words. Make sure that the generated text is in valid English:

        "{model_response}" 

        Your response should only contain the modified text."""

CORRUPT_SENTIMENT_PROMPT = """You are given a piece of text. You need to rewrite the text in such a way that sentiment of the below text becomes more negative in sentiment. Make sure that the generated text is in valid English:

        "{model_response}" 

        Your response should only contain the modified text."""


CORRUP_RELEVANCE_PROMPT = """Generate a random piece of text having around {number_of_words} words."""
