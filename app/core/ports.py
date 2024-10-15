from abc import ABC, abstractmethod
from typing import List

from app.core import models

# Interfaz del puerto (estrategia abstracta)
class DocumentExtractorStrategy(ABC):
    @abstractmethod
    def extract_content(self, file_path: str) -> str:
        """Extrae el contenido del documento."""
        pass



#---------------------------------Clase abstracta para openAi y sus metodos---------------------------------------------

class LlmPort(ABC):

    #Metodo para generar texto
    @abstractmethod
    def generate_text(self, prompt: str, retrieval_context: str) -> str:
        pass

#----------------------------------Clase abstracta para usuario y sus metodos-------------------------------------------

class UserRepositoryPort(ABC):

    #Guardar usuario
    @abstractmethod
    def save_user(self, user: models.User) -> None:
        pass

    #Eliminar usuario
    @abstractmethod
    def delete_user(self, user_id: str) -> str:
        pass

    #Actualizar usuario
    @abstractmethod
    def update_user(self, user_id: str, update_data: dict) -> str:
        pass

    # Listar Usuario

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> models.User:
        pass

    #Listar Usuarios

    @abstractmethod
    def list_users(self) -> str:
        pass

    @abstractmethod
    def login_user(self, email: str, password: str):
        pass