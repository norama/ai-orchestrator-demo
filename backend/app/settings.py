from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    app_name: str = "ai-orchestrator-demo"
    log_level: str = "WARNING"
    cors_origins: str = ""  # Comma-separated list of allowed CORS origins

    class Config:
        env_file = ".env"

    @property
    def cors_origins_list(self):
        return self.cors_origins.split(",") if self.cors_origins else []


env_settings = EnvSettings()
