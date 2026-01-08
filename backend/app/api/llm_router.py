from fastapi import APIRouter, Depends

from app.api.llm_dependencies import get_llm_client
from app.api.response import LLMResponse
from app.application.services.probabilistic.llm.client.json_utils import extract_json
from app.application.services.probabilistic.llm.client.llm_client import LLMClient

llm_router = APIRouter(prefix="/llm", tags=["LLM"])


@llm_router.get("", response_model=LLMResponse)
def llm_call(
    prompt: str = "Say hello in JSON format",
    client: LLMClient = Depends(get_llm_client),
):
    response = client.complete_text(prompt)

    response_json = extract_json(response)

    return LLMResponse(
        response_json=response_json,
        status="ok",
    )
