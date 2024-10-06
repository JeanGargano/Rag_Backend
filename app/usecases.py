from http.client import HTTPException
from typing import List, Optional
from app.core.models import Document, User
from app.core import ports, models


class RAGService:
    # Instanciando objetos
    def __init__(self, storage_strategy: ports.DocumentStorageStrategy,
                 openai_adapter: ports.LlmPort,
                 mongo_adapter: ports.UserRepositoryPort):
        self.storage_strategy = storage_strategy  # Estrategia para documentos
        self.openai_adapter = openai_adapter  # Adaptador para OpenAI
        self.mongo_adapter = mongo_adapter  # Adaptador para MongoDB

    # Método para generar respuesta
    def generate_answer(self, query: str) -> str:
        documents = self.storage_strategy.get_documents(query)
        context = " ".join([doc.content for doc in documents])
        return self.openai_adapter.generate_text(prompt=query, retrieval_context=context)

    # ----------------------------------------- Métodos para documentos ---------------------------------------------

    def chunk_content(self, content: str, chunk_size: int = 512) -> List[str]:
        """Divide el contenido en chunks de tamaño especificado."""
        return [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

    def save_document(self, content: str) -> str:
        try:
            chunks = self.chunk_content(content)  # Divide el contenido en chunks
            for chunk in chunks:
                document = Document(content=chunk)
                self.storage_strategy.store_document(document)  # Almacena cada chunk
            return "Documento guardado exitosamente."
        except Exception as e:
            print(f"Error al guardar el documento: {e}")
            return "Error al guardar el documento."

    # Método para obtener todos los documentos
    def get_documents(self, query: Optional[str] = None) -> List[Document]:
        try:
            return self.storage_strategy.get_documents(query or "")
        except Exception as e:
            print(f"Error al obtener documentos: {e}")
            return []

    # Método para obtener documento por ID
    def get_document_by_id(self, doc_id: str) -> Optional[Document]:
        try:
            documents = self.storage_strategy.get_document_by_id(doc_id)
            return documents[0] if documents else None
        except Exception as e:
            print(f"Error al obtener el documento con ID {doc_id}: {e}")
            return None

    # Método para actualizar el documento
    def update_document(self, doc_id: str, content: str) -> str:
        try:
            document = Document(content=content)
            result = self.storage_strategy.update_document(doc_id, document)
            if result:
                return "Documento actualizado con éxito."
            return "Error: no se pudo actualizar el documento."
        except Exception as e:
            print(f"Error al actualizar el documento con ID {doc_id}: {e}")
            return "Error al actualizar el documento."

    # Método para eliminar el documento
    def delete_document_by_id(self, doc_id: str) -> str:
        try:
            success = self.storage_strategy.delete_document_by_id(doc_id)
            if success:
                return "Documento eliminado exitosamente."
            return "Documento no encontrado."
        except Exception as e:
            print(f"Error al eliminar el documento con ID {doc_id}: {e}")
            return "Error al eliminar el documento."

    # ------------------------------------------ Métodos para usuarios ---------------------------------------------

    # Método para obtener un usuario por su ID, sirve para actualizar
    def get_user_by_id(self, user_id: str) -> Optional[models.User]:
        user = self.mongo_adapter.get_user(user_id)
        if user:
            return models.User(**user)
        return None

    # Método para guardar un usuario
    def save_user(self, user: User) -> str:
        saved_user = self.mongo_adapter.save_user(user)
        if saved_user is None:
            return "Los campos no pueden ser nulos."
        if saved_user:
            return "El usuario se ha guardado exitosamente."
        return "Error al guardar el usuario."

    # Método para eliminar un usuario
    def delete_user(self, user_id: str) -> str:
        success = self.mongo_adapter.delete_user(user_id)
        if success:
            return "Usuario eliminado exitosamente."
        return "Usuario no encontrado."

    # Método para actualizar un usuario
    def update_user(self, user_id: str, update_data: dict) -> str:
        try:
            result = self.mongo_adapter.update_user(user_id, update_data)
            if result:
                return "Usuario actualizado exitosamente."
            return "Usuario no encontrado."
        except Exception as e:
            print(f"Error al actualizar el usuario: {e}")
            return "Error al actualizar el usuario."

    # Método para listar todos los usuarios
    def list_users(self) -> List[User]:
        return self.mongo_adapter.list_users()

    # Método para validar usuario en la BD
    def login_user(self, email: str, password: str) -> User:
        try:
            user = self.mongo_adapter.login_user(email, password)
            return user or None
        except Exception as e:
            print(f"Error durante el login: {e}")
            raise e
