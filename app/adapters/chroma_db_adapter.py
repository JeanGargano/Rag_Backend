import chromadb
from typing import List
from app.core import ports
from app.core import models


class ChromaDBAdapter(ports.DocumentRepositoryPort):

    #Conexion a la base de datos
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("documents")

#--------------------------------------#Metodos para la clase documento-------------------------------------------------

    #Metodos para crear documento
    def save_document(self, document: models.Document) -> None:
        print(f"Document: {document}")
        self.collection.add(
            ids=[document.id],
            documents=[document.content]
        )
    #metodo para listar documento
    def get_documents(self, query: str, n_results: int = 2) -> List[models.Document]:
        results = self.collection.query(query_texts=[query], n_results=n_results)
        print(query)
        print(f"Results: {results}")
        documents = []
        for i, doc_id_list in enumerate(results['ids']):
            for doc_id in doc_id_list:
                documents.append(models.Document(id=doc_id, content=results['documents'][i][0]))
        return documents

    # Método para listar documento por ID

    def get_document_id(self, doc_id: str) -> List[models.Document]:
        try:
            # Buscar el documento por su ID
            result = self.collection.get(ids=[doc_id])

            # Si hay resultados y contienen documentos, devolver el documento como lista
            if result and 'documents' in result and result['documents']:
                return [models.Document(id=doc_id, content=result['documents'][0][0])]

            # Si no se encuentra el documento, devolver una lista vacía
            return []
        except Exception as e:
            print(f"Error al intentar obtener el documento con ID {doc_id}: {e}")
            return []



    # Método para actualizar un documento

    def update_document(self, doc_id: str, document: models.Document) -> str:
        try:
            # Primero eliminamos el documento existente por su ID
            self.collection.delete(ids=[doc_id])

            # Luego insertamos el nuevo documento con el mismo ID
            self.collection.add(ids=[doc_id], documents=[document.content])

            print(f"Documento con ID {doc_id} actualizado correctamente.")
            return "Documento actualizado con éxito"
        except Exception as e:
            print(f"Error al intentar actualizar el documento con ID {doc_id}: {e}")
            return "Error no se pudo actualizar el documento"

    # Método para borrar un documento

    def delete_document_by_id(self, doc_id: str) -> str:
        try:
            # Asumimos que collection.delete existe y acepta una lista de IDs
            self.collection.delete(ids=[doc_id])
            print(f"Documento con ID {doc_id} eliminado correctamente.")
            return "Documento Eliminado con éxito de la base de datos."
        except Exception as e:
            print(f"Error al intentar eliminar el documento con ID {doc_id}: {e}")
            return "Error al intentar eliminar el documento con ID: " + doc_id












