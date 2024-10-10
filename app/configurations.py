from pydantic_settings import BaseSettings

class Configs(BaseSettings):
    openai_api_key: str
    model: str
    max_tokens: int
    temperature: float

    class Config:
        env_file = ".env"

# Cargar la configuración
config = Configs()

# Comprobar que las variables se cargan correctamente

