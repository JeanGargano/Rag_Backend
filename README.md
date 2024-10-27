# Rag_Backend

In this repository, there is a Rag() system connected to the OpenAI API. Its operation is based on document loading, where the documents are vectorized in the backend using the chunking technique and stored in the ChromaDB vector database. Once the documents have been successfully saved, the OpenAI API queries the database to find vectors related to the context of the prompt.
