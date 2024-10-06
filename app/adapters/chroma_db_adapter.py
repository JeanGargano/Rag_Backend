import chromadb
from typing import List, Optional
from app.core import ports
from app.core.models import Document


class ChromaDocumentAdapter(ports.DocumentStorageStrategy):
    def __init__(self, chroma_client):
        self.chroma_client = chroma_client  # Cliente de ChromaDB para realizar operaciones

    def store_document(self, document: Document) -> None:
        """Almacena un documento en ChromaDB."""
        # Convertir el documento a un formato compatible con ChromaDB y guardarlo
        self.chroma_client.add_document(document.content)

    def get_documents(self, query: str) -> List[Document]:
        """Obtiene documentos que coinciden con la consulta."""
        # Buscar documentos en ChromaDB basado en la consulta
        results = self.chroma_client.query_documents(query)
        return [Document(content=doc) for doc in results]

    def get_document_by_id(self, doc_id: str) -> Optional[List[Document]]:
        """Obtiene un documento específico por su ID."""
        # Lógica para obtener un documento por ID desde ChromaDB
        result = self.chroma_client.get_document(doc_id)
        return [Document(content=result)] if result else None

    def update_document(self, doc_id: str, document: Document) -> bool:
        """Actualiza un documento existente en ChromaDB."""
        # Lógica para actualizar el documento en ChromaDB
        return self.chroma_client.update_document(doc_id, document.content)

    def delete_document_by_id(self, doc_id: str) -> bool:
        """Elimina un documento específico por su ID."""
        # Lógica para eliminar un documento de ChromaDB
        return self.chroma_client.delete_document(doc_id)