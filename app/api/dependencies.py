from app.adapters.openai_adapter import OpenAIAdapter
from app.adapters.chroma_db_adapter import ChromaDBAdapter
from app.adapters.mongo_db_adapter import MongoDbAdapter
from app import usecases
from app import configurations

#Esta clase utiliza el patron singleton
#Asegura que solo se creee una instacia de Rag Service y se use en todo el flujo

class RAGServiceSingleton:
    _instance = None

    @classmethod
    def get_instance(cls) -> usecases.RAGService:
        if cls._instance is None:
            configs = configurations.Configs()
            openai_adapter = OpenAIAdapter(api_key=configs.openai_api_key, model=configs.model,
                                      max_tokens=configs.max_tokens, temperature=configs.temperature)
            chroma_adapter = ChromaDBAdapter()
            mongo_adapter = MongoDbAdapter()
            cls._instance = usecases.RAGService(
                chroma_adapter=chroma_adapter,
                openai_adapter=openai_adapter,
                mongo_adapter=mongo_adapter
            )
        return cls._instance
