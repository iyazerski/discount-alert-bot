import time

from openai import OpenAI, RateLimitError
from openai.types.chat import ChatCompletion


class PriceChecker:
    def __init__(self, openai_api_token: str, openai_model: str) -> None:
        self._openai_client = OpenAI(api_key=openai_api_token)
        self._openai_model = openai_model

    def _make_openai_request(
        self,
        user_message: str,
        system_message: str,
        retry_count: int = 3,
    ) -> ChatCompletion:
        try:
            return self._openai_client.chat.completions.create(
                model=self._openai_model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ],
            )
        except RateLimitError as exc:
            if retry_count > 0:
                time.sleep(5)
                return self._make_openai_request(user_message, system_message, retry_count - 1)
            else:
                raise exc

    @property
    def check_price_prompt(self) -> str:
        return """
        Provide the current price (with currency) from the given product sale page link. Respond with only the price.
        """.strip()

    def check_price(self, product_link: str) -> str:
        response = self._make_openai_request(user_message=product_link, system_message=self.check_price_prompt)
        return response.choices[0].message.content.strip()
