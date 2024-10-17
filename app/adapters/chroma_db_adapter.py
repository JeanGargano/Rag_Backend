import uuid

from app.core.models import Document
import logging
from typing import Optional, List
from app.configurations import Configs  # Asegúrate de importar tu clase de configuración
from app.adapters.openai_adapter import OpenAIAdapter  # Asegúrate de importar el adaptador

class ChromaDocumentAdapter:
    def __init__(self, chroma_client, openai_adapter: OpenAIAdapter, config: Configs, collection_name="documents"):
        self.chroma_client = chroma_client
        self.collection_name = collection_name
        self.embedding_function = openai_adapter  # Usar el adaptador de OpenAI directamente
        self.api_key = config.openai_api_key  # Almacena la clave API si necesitas usarla más tarde

    async def save_documents(self, documents: List[Document]) -> None:
        try:
            collection = self.chroma_client.get_or_create_collection(self.collection_name)
            ids = [str(uuid.uuid4()) for _ in documents]
            embeddings = await self.embedding_function.generate_embeddings_parallel([doc.content for doc in documents])
            metadatas = [{"file_type": doc.file_type, "content": doc.content} for doc in documents]

            collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas
            )
            logging.info(f"{len(documents)} documentos almacenados exitosamente en ChromaDB.")
        except Exception as e:
            logging.error(f"Error al almacenar documentos en ChromaDB: {e}", exc_info=True)

    def get_documents(self, query: str):
        collection = self.chroma_client.get_or_create_collection(self.collection_name)
        embedding = self.embedding_function.create_embedding(query)
        if embedding:
            results = collection.query(
                query_embeddings=[embedding],
                n_results=1
            )

            documents = []
            if 'metadatas' in results and results['metadatas']:
                for metadata in results['metadatas'][0]:
                    if isinstance(metadata, dict):
                        content = metadata.get('content', '')
                        file_type = metadata.get('file_type', '')
                        documents.append(Document(content=content, file_type=file_type))

            return documents
        else:
            print("No se pudo generar el embedding para la consulta.")
            return []

    def get_document_by_id(self, doc_id: str) -> Optional[List[Document]]:
        """Obtiene un documento específico por su ID."""
        # Lógica para obtener un documento por ID desde ChromaDB
        result = self.chroma_client.get_document(doc_id)
        return [Document(content=result)] if result else None

    def delete_document_by_id(self, doc_id: str) -> bool:
        """Elimina un documento específico por su ID."""
        # Lógica para eliminar un documento de ChromaDB
        return self.chroma_client.delete_document(doc_id)