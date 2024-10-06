from abc import ABC, abstractmethod
from typing import List

from app.core import models
from app.core.models import Document


#--------------------------------Clase abstracta de documento y sus metodos---------------------------------------------

class DocumentStorageStrategy(ABC):
    @abstractmethod
    def store_document(self, document: Document) -> None:
        pass

    @abstractmethod
    def get_documents(self, query: str) -> List[Document]:
        pass

    @abstractmethod
    def update_document(self, doc_id: str, document: Document) -> str:
        pass

    @abstractmethod
    def delete_document_by_id(self, doc_id: str) -> str:
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

    @abstractmethod
    def login_user(self, email: str, password: str):
        pass







