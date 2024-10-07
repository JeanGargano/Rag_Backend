from app.adapters.openai_adapter import OpenAIAdapter
from app.adapters.chroma_db_adapter import ChromaDocumentAdapter
from app.adapters.mongo_db_adapter import MongoDbAdapter
from app import usecases
from app import configurations

# Esta clase utiliza el patrón Singleton
# Asegura que solo se cree una instancia de RAGService y se use en todo el flujo

class RAGServiceSingleton:
    _instance = None

    @classmethod
    def get_instance(cls) -> usecases.RAGService:
        if cls._instance is None:
            # Cargar las configuraciones
            configs = configurations.Configs()

            # Inicializar adaptadores con sus respectivos parámetros
            openai_adapter = OpenAIAdapter(api_key=configs.openai_api_key, model=configs.model,
                                           max_tokens=configs.max_tokens, temperature=configs.temperature)

            # Aquí debes inicializar `chroma_client` antes de pasarlo a ChromaDocumentAdapter
            chroma_client = ...  # Aquí debes inicializar tu cliente Chroma (según cómo lo crees en tu código)
            chroma_adapter = ChromaDocumentAdapter()

            mongo_adapter = MongoDbAdapter()

            # Crear la instancia de RAGService
            cls._instance = usecases.RAGService(
                chroma_adapter=chroma_adapter,
                openai_adapter=openai_adapter,
                mongo_adapter=mongo_adapter
            )
        return cls._instance
