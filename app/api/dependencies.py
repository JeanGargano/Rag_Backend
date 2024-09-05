from app.adapters.openai_adapter import OpenAIAdapter
from app.adapters.chroma_db_adapter import ChromaDBAdapter
from app import usecases
from app import configurations


class RAGServiceSingleton:
    _instance = None

    @classmethod
    def get_instance(cls) -> usecases.RAGService:
        if cls._instance is None:
            configs = configurations.Configs()
            openai_adapter = OpenAIAdapter(api_key=configs.openai_api_key, model=configs.model,
                                           max_tokens=configs.max_tokens, temperature=configs.temperature)
            document_repo = ChromaDBAdapter()
            cls._instance = usecases.RAGService(document_repo=document_repo, openai_adapter=openai_adapter)
        return cls._instance
