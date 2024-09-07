from typing import List, Optional

from pyasn1.compat.octets import null

from app.core.models import Document, User
from app.core import ports, models


# Implementación de los métodos definidos en las clases abstractas
class RAGService:

    # Instanciando objetos
    def __init__(self, chroma_adapter: ports.DocumentRepositoryPort, openai_adapter: ports.LlmPort, mongo_adapter: ports.UserRepositoryPort):
        self.chroma_adapter = chroma_adapter
        self.openai_adapter = openai_adapter
        self.mongo_adapter = mongo_adapter

    # Metodo para generar respuesta
    def generate_answer(self, query: str) -> str:
        documents = self.chroma_adapter.get_documents(query)
        print(f"Documents: {documents}")
        context = " ".join([doc.content for doc in documents])
        return self.openai_adapter.generate_text(prompt=query, retrieval_context=context)

    #-----------------------------------------Métodos para documento---------------------------------------------

    # Método para crear documento
    def save_document(self, content: str) -> None:
        document = Document(content=content)
        self.chroma_adapter.save_document(document)

    #------------------------------------------Métodos para usuario-------------------------------------------------

    #Metodo para obtener un usuario por su id, sirve para el actualizar
    def get_user_by_id(self, user_id: str) -> Optional[models.User]:
        """Obtiene un usuario por su ID"""
        user = self.mongo_adapter.get_user(user_id)
        if user:
            return models.User(**user)
        return None

    # Metodo para guardar un usuario
    def save_user(self, user: User) -> str:
        saved_user = self.mongo_adapter.save_user(user)
        if (saved_user == null):
            return "Los campos no pueden ser nulos"
        if saved_user:
            return "El usuario se ha guardado exitosamente"
        return "Error al guardar el usuario"

    # Metodo para eliminar un usuario
    def delete_user(self, user_id: str) -> str:
        success = self.mongo_adapter.delete_user(user_id)
        if success:
            return "Usuario eliminado exitosamente"
        return "Usuario no encontrado"

    # Metodo para actualizar un usuario
    def update_user(self, user_id: str, update_data: dict) -> str:
        try:
            result = self.mongo_adapter.update_user(user_id, update_data)
            if result:
                return "Usuario actualizado exitosamente"
            return "Usuario no encontrado"
        except Exception as e:
            print(f"Error updating user: {e}")
            return "Error al actualizar el usuario"

    # Metodo para listar todos los usuarios
    def list_users(self) -> List[User]:
        users = self.mongo_adapter.list_users()
        return users
