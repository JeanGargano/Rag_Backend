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

    def save_document(self, document: Document) -> None:
        """Guarda el documento en ChromaDB tras generar su embedding."""
        try:
            if not document.id or not document.content:
                raise ValueError("El documento debe tener un ID y contenido válido.")

            collection = self.chroma_client.get_or_create_collection(self.collection_name)

            # Generar embedding para el contenido del documento usando el adaptador de OpenAI
            embedding = self.embedding_function.create_embedding(document.content)
            if embedding is None:
                raise ValueError("El embedding no se generó correctamente.")

            logging.info(f"Embedding generado para el documento {document.id}: {embedding}")

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

    def get_documents(self, query: str):
        collection = self.chroma_client.get_or_create_collection(self.collection_name)
        embedding = self.embedding_function.create_embedding(query)
        if embedding:
            print("Embedding generado correctamente")

        results = collection.query(
            query_embeddings=[embedding],
            n_results=5
        )

        print(f"Resultados completos de ChromaDB: {results}")

        documents = []
        if 'metadatas' in results and results['metadatas']:
            for metadata in results['metadatas'][0]:  # Accede al primer elemento de la lista
                if isinstance(metadata, dict):
                    content = metadata.get('content', '')
                    file_type = metadata.get('file_type', '')
                    documents.append(Document(content=content, file_type=file_type))

        print(f"Documentos encontrados: {len(documents)}")

        if not documents:
            logging.warning("No se encontraron documentos para la consulta.")

        return documents

    def get_document_by_id(self, doc_id: str) -> Optional[List[Document]]:
        """Obtiene un documento específico por su ID."""
        # Lógica para obtener un documento por ID desde ChromaDB
        result = self.chroma_client.get_document(doc_id)
        return [Documento(content=result)] if result else None

    def delete_document_by_id(self, doc_id: str) -> bool:
        """Elimina un documento específico por su ID."""
        # Lógica para eliminar un documento de ChromaDB
        return self.chroma_client.delete_document(doc_id)