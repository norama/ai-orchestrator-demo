from app.application.registry import create_llm_client
from app.application.services.probabilistic.llm.client.llm_client import LLMClient

_client = create_llm_client()


def get_llm_client() -> LLMClient:
    return _client
