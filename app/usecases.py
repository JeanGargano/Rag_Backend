from app.core.models import Document, User
from app.core import ports

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

    # Metodo para guardar un usuario
    def save_user(self, user: User) -> str:
        self.mongo_adapter.save_user(user)
        return "El usuario se ha guardado exitosamente"

    # Metodo para eliminar un usuario
    def delete_user(self, user_id: str) -> str:
        result = self.mongo_adapter.delete_user(user_id)
        return result

    # Metodo para actualizar un usuario
    def update_user(self, user: User) -> str:
        result = self.mongo_adapter.update_user(user)
        return result

    # Metodo para listar todos los usuarios
    def list_users(self) -> str:
        result = self.mongo_adapter.list_users()
        return result
