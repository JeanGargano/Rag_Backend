from pydantic_settings import BaseSettings
from functools import lru_cache

class Configs(BaseSettings):
    openai_api_key: str
    model: str
    max_tokens: int
    temperature: float

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

@lru_cache()
def get_configs(env_file: str = '.env') -> Configs:
    """
    Obtiene la configuración desde un archivo .env específico.
    Si no se especifica, usa .env por defecto.
    """
    return Configs(_env_file=env_file)