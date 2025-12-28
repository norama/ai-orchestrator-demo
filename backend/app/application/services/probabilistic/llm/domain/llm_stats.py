from pydantic import BaseModel


class LLMUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    model: str
