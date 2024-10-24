from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv('.env.test')



class Configs(BaseSettings):
    openai_api_key: str
    model: str
    max_tokens: int
    temperature: float

    class Config:
        env_file = ".env.test"

# Cargar la configuración
config = Configs()

# Comprobar que las variables se cargan correctamente

