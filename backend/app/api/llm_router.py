from fastapi import APIRouter, Depends

from app.api.llm_dependencies import get_llm_client
from app.application.services.probabilistic.llm.client.llm_client import LLMClient
from app.domain.response import LLMResponse

llm_router = APIRouter(prefix="/llm", tags=["LLM"])


@llm_router.get("", response_model=LLMResponse)
def llm_call(
    prompt: str = "Say hello in JSON format",
    client: LLMClient = Depends(get_llm_client),
):
    response_json = client.complete_json(prompt)

    return LLMResponse(
        response_json=response_json,
        status="ok",
    )
