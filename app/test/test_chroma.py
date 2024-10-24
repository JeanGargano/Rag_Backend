import pytest
from unittest.mock import MagicMock, patch
from app.adapters.chroma_db_adapter import ChromaDocumentAdapter
from app.core.models import Document
from app.configurations import Configs


@pytest.fixture
def mock_config():
    config = MagicMock(spec=Configs)
    # Añadir el atributo openai_api_key al mock
    config.openai_api_key = "test-api-key"
    return config


@pytest.fixture
def mock_openai_adapter():
    return MagicMock()


@pytest.fixture
def mock_chroma_client():
    return MagicMock()


@pytest.fixture
def chroma_adapter(mock_chroma_client, mock_openai_adapter, mock_config):
    return ChromaDocumentAdapter(
        mock_chroma_client,
        mock_openai_adapter,
        mock_config,
        collection_name="test_collection"
    )


@pytest.mark.asyncio
async def test_save_documents_success(chroma_adapter):
    """Test successful document saving"""
    # Preparar los documentos de prueba
    documents = [
        Document(content="Test content 1", file_type="txt"),
        Document(content="Test content 2", file_type="pdf")
    ]

    mock_collection = MagicMock()
    chroma_adapter.chroma_client.get_or_create_collection.return_value = mock_collection

    embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    chroma_adapter.embedding_function.generate_embeddings_parallel.return_value = embeddings

    await chroma_adapter.save_documents(documents)

    chroma_adapter.chroma_client.get_or_create_collection.assert_called_once_with(name="documents")
    mock_collection.add.assert_called_once()

    args = mock_collection.add.call_args[1]  # Obtener kwargs
    assert "embeddings" in args
    assert "documents" in args
    assert "metadatas" in args
    assert len(args["embeddings"]) == 2
    assert len(args["documents"]) == 2

def test_get_documents_success(chroma_adapter):
    """Test successful document retrieval"""
    mock_collection = MagicMock()
    chroma_adapter.chroma_client.get_or_create_collection.return_value = mock_collection
    chroma_adapter.embedding_function.create_embedding.return_value = [0.1, 0.2, 0.3]

    mock_collection.query.return_value = {
        'metadatas': [[{
            'content': 'Test content',
            'file_type': 'txt'
        }]]
    }

    results = chroma_adapter.get_documents("test query")

    assert len(results) > 0
    assert isinstance(results[0], Document)
    assert results[0].content == "Test content"
    assert results[0].file_type == "txt"


def test_get_documents_no_embedding(chroma_adapter):
    """Test document retrieval when embedding creation fails"""
    chroma_adapter.embedding_function.create_embedding.return_value = None

    results = chroma_adapter.get_documents("test query")
    assert len(results) == 0


def test_get_document_by_id_success(chroma_adapter):
    """Test successful document retrieval by ID"""
    mock_doc = {
        "content": "Test document content",
        "file_type": "txt"
    }
    chroma_adapter.chroma_client.get_document.return_value = mock_doc

    result = chroma_adapter.get_document_by_id("test_id")
    assert result is not None
    assert isinstance(result[0], Document)
    assert result[0].content == mock_doc["content"]
    assert result[0].file_type == mock_doc["file_type"]


def test_get_document_by_id_not_found(chroma_adapter):
    """Test document retrieval when document doesn't exist"""
    chroma_adapter.chroma_client.get_document.return_value = None

    result = chroma_adapter.get_document_by_id("test_id")
    assert result is None


def test_delete_document_success(chroma_adapter):
    """Test successful document deletion"""
    chroma_adapter.chroma_client.delete_document.return_value = True

    result = chroma_adapter.delete_document_by_id("test_id")
    assert result is True


def test_delete_document_failure(chroma_adapter):
    """Test failed document deletion"""
    chroma_adapter.chroma_client.delete_document.return_value = False

    result = chroma_adapter.delete_document_by_id("test_id")
    assert result is False