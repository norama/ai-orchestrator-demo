from fastapi import FastAPI

from app.logging_utils import get_logger, setup_logging

setup_logging()

app = FastAPI(title="AI Orchestrator Demo")

logger = get_logger(__name__)


@app.get("/health")
def health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}
