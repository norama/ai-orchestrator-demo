from app.application.services.probabilistic.llm.client.llm_client import LLMClient
from app.application.services.probabilistic.llm.client.openai_client import OpenAIClient

_client = OpenAIClient()


def get_llm_client() -> LLMClient:
    return _client
