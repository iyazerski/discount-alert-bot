from pydantic import SecretStr
from pydantic_settings import BaseSettings


class OpenAISettings(BaseSettings):
    OPENAI_API_KEY: SecretStr
    OPENAI_MODEL: str = "gpt-4o-mini"
