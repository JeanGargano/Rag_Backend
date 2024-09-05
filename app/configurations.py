import pydantic_settings


class Configs(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    openai_api_key: str
    model: str
    max_tokens: int
    temperature: float
