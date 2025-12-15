from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    app_name: str = "ai-orchestrator-demo"
    log_level: str = "WARNING"

    class Config:
        env_file = ".env"


env_settings = EnvSettings()
