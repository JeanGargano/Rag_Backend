import os
from app.core.models import Document
from chromadb.utils import embedding_functions
import logging
from typing import Optional, List

class ChromaDocumentAdapter:
    def _init_(self, chroma_client, collection_name="documents", api_key=None):
        self.chroma_client = chroma_client
        self.collection_name = collection_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(api_key=self.api_key)

    def save_document(self, document: Document) -> None:
        """Guarda el documento en ChromaDB tras generar su embedding."""
        try:
            if not document.id or not document.content:
                raise ValueError("El documento debe tener un ID y contenido válido.")

            collection = self.chroma_client.get_or_create_collection(self.collection_name)

            # Generar embedding para el contenido del documento
            embedding = self.embedding_function.create_embedding(document.content)

            # Añadir el documento a la colección de ChromaDB
            collection.add(
                ids=[document.id],
                embeddings=[embedding],
                metadatas=[{"file_type": document.file_type, "content": document.content}]
            )
            logging.info(f"Documento {document.id} almacenado exitosamente en ChromaDB.")
        except ValueError as ve:
            logging.error(f"Error de validación en el documento: {ve}")
        except Exception as e:
            logging.error(f"Error al almacenar el documento en ChromaDB: {e}", exc_info=True)

    def get_documents(self, query: str) -> List[Document]:
        """Obtiene documentos que coinciden con la consulta."""
        # Buscar documentos en ChromaDB basado en la consulta
        results = self.chroma_client.query_documents(query)
        return [Documento(content=doc) for doc in results]

    def get_document_by_id(self, doc_id: str) -> Optional[List[Document]]:
        """Obtiene un documento específico por su ID."""
        # Lógica para obtener un documento por ID desde ChromaDB
        result = self.chroma_client.get_document(doc_id)
        return [Documento(content=result)] if result else None

    def update_document(self, doc_id: str, document: Document) -> bool:
        """Actualiza un documento existente en ChromaDB."""
        # Lógica para actualizar el documento en ChromaDB
        return self.chroma_client.update_document(doc_id, document.content)

    def delete_document_by_id(self, doc_id: str) -> bool:
        """Elimina un documento específico por su ID."""
        # Lógica para eliminar un documento de ChromaDB
        return self.chroma_client.delete_document(doc_id)