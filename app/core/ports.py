from abc import ABC, abstractmethod
from typing import List

from app.core import models

#--------------------------------Clase abstracta de documento y sus metodos---------------------------------------------

class DocumentRepositoryPort(ABC):

    #Metodo para crear
    @abstractmethod
    def save_document(self, document: models.Document) -> None:
        pass

    #Metodo para listar
    @abstractmethod
    def get_documents(self, query: str) -> List[models.Document]:
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
    def update_user(self, user: models.User) -> str:
        pass

    #Listar Usuario
    @abstractmethod
    def list_users(self) -> str:
        pass
