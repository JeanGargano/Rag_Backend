import logging
from typing import List, Optional

from app.adapters.chroma_db_adapter import ChromaDocumentAdapter
from app.adapters.mongo_db_adapter import MongoDbAdapter
from app.adapters.openai_adapter import OpenAIAdapter
from app.api.Strategy import PDFExtractionStrategy, DocxExtractionStrategy
from app.core import models
from app.core.models import Document, User

#Estrategias para guardar documento
tipo = {
        "pdf": PDFExtractionStrategy(),
        "docx": DocxExtractionStrategy()
    }

class RAGService:
    def __init__(self, chroma_adapter: ChromaDocumentAdapter, openai_adapter: OpenAIAdapter, mongo_adapter: MongoDbAdapter):
        self.chroma_adapter = chroma_adapter
        self.openai_adapter = openai_adapter
        self.mongo_adapter = mongo_adapter


#--------------------------------------------Metodo de OPENAi------------------------------------------------

    def generate_answer(self, query: str) -> str:
        documents = self.chroma_adapter.get_documents(query)
        print(f"Documents: {documents}")
        context = " ".join([doc.content for doc in documents])
        return self.openai_adapter.generate_text(prompt=query, retrieval_context=context)


#----------------------------------------------Metodos para documentos---------------------------------------

    def chunk_content(self, content: str, chunk_size: int = 512) -> List[str]:
        """Divide el contenido en chunks de tamaño especificado."""
        return [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

    def prepare_documents(self, content: str, file_type: str, chunk_size: int = 512) -> List[Document]:
        """Prepara una lista de documentos chunked basados en el contenido y tipo de archivo."""
        chunks = self.chunk_content(content, chunk_size)
        documents = [Document(file="", content=chunk, file_type=file_type) for chunk in chunks]
        return documents

    def save_document(self, file_path: str, file_type: str) -> str:
        """Extrae el contenido usando la estrategia, lo divide en chunks y lo almacena."""
        try:
            # Obtener la estrategia del diccionario
            strategy = tipo.get(file_type)
            if not strategy:
                raise ValueError(f"Tipo de archivo no soportado: {file_type}")

            # Extraer contenido usando la estrategia
            content = strategy.extract_content(file_path)

            # Preparar y almacenar los chunks
            documents = self.prepare_documents(content, file_type)
            for doc in documents:
                self.chroma_adapter.save_document(doc)  # Cambiar 'self.ChromaDocumentAdapter' a 'self.chroma_adapter'

            return "Documento guardado exitosamente."
        except Exception as e:
            logging.error(f"Error al guardar el documento: {e}")
            return "Error al guardar el documento."


    # ------------------------------------------ Métodos para usuarios ---------------------------------------------

    def get_user_by_id(self, user_id: str) -> Optional[models.User]:
        """Obtiene un usuario por su ID"""
        user = self.mongo_adapter.get_user_by_id(user_id)
        if user:
            return models.User(**user)
        return None

    def save_user(self, user: User) -> str:
        saved_user = self.mongo_adapter.save_user(user)
        if saved_user is None:
            return "Los campos no pueden ser nulos."
        if saved_user:
            return "El usuario se ha guardado exitosamente."
        return "Error al guardar el usuario."


    def delete_user(self, user_id: str) -> str:
        success = self.mongo_adapter.delete_user(user_id)
        if success:
            return "Usuario eliminado exitosamente."

        return "Usuario no encontrado."

    def update_user(self, user_id: str, update_data: dict) -> str:
        try:
            result = self.mongo_adapter.update_user(user_id, update_data)
            if result:
                return "Usuario actualizado exitosamente."
            return "Usuario no encontrado."
        except Exception as e:
            logging.error(f"Error al actualizar el usuario: {e}")
            return "Error al actualizar el usuario."

    def list_users(self) -> List[User]:
        return self.mongo_adapter.list_users()


    def login_user(self, email: str, password: str) -> Optional[User]:
        """Método para validar usuario en la BD."""
        try:
            user = self.mongo_adapter.login_user(email, password)
            return user
        except Exception as e:
            logging.error(f"Error durante el login: {e}")
            return None