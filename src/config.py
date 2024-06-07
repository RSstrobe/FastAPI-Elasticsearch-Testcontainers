from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra="ignore")

    app_host: str
    app_port: int
    elastic_host: str
    elastic_port: int

    @computed_field
    @property
    def elastic_url(self) -> str:
        return f"{self.elastic_host}:{self.elastic_port}"


settings = Settings(_env_file="../.env")
