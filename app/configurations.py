import pydantic_settings

class Configs(pydantic_settings.BaseSettings):
    openai_api_key: str
    model: str
    max_tokens: int
    temperature: float

    class Config:
        env_file = ".env"
