from app.adapters.openai_adapter import OpenAIAdapter
from app.adapters.chroma_db_adapter import ChromaDocumentAdapter
from app.adapters.mongo_db_adapter import MongoDbAdapter
from app import usecases
from app import configurations
import chromadb

class RAGServiceSingleton:
    _instance = None

    @classmethod
    def get_instance(cls) -> usecases.RAGService:
        if cls._instance is None:
            configs = configurations.Configs()  # Crea una instancia de Configs

            # Inicializa OpenAIAdapter pasando la configuración completa
            openai_adapter = OpenAIAdapter(configs)  # Pasar la instancia de Configs

            # Inicializa el cliente ChromaDB
            chroma_client = chromadb.Client()  # Asegúrate de usar la forma correcta de inicializar el cliente

            # Pasar el cliente y la configuración a ChromaDocumentAdapter
            chroma_adapter = ChromaDocumentAdapter(
                chroma_client=chroma_client,
                openai_adapter=openai_adapter,  # Pasar el adaptador de OpenAI
                config=configs  # Asegúrate de pasar la instancia de configuración
            )

            # Inicializa MongoDbAdapter
            mongo_adapter = MongoDbAdapter()

            # Crea la instancia de RAGService
            cls._instance = usecases.RAGService(
                chroma_adapter=chroma_adapter,
                openai_adapter=openai_adapter,
                mongo_adapter=mongo_adapter
            )
        return cls._instance
