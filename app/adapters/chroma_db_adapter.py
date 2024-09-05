import chromadb
from typing import List
from app.core import ports
from app.core import models


class ChromaDBAdapter(ports.DocumentRepositoryPort):
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("documents")

    def save_document(self, document: models.Document) -> None:
        print(f"Document: {document}")
        self.collection.add(
            ids=[document.id],
            documents=[document.content]
        )

    def get_documents(self, query: str, n_results: int = 2) -> List[models.Document]:
        results = self.collection.query(query_texts=[query], n_results=n_results)
        print(query)
        print(f"Results: {results}")
        documents = []
        for i, doc_id_list in enumerate(results['ids']):
            for doc_id in doc_id_list:
                documents.append(models.Document(id=doc_id, content=results['documents'][i][0]))
        return documents
