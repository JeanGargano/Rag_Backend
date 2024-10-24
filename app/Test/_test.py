import pytest
from unittest.mock import MagicMock, patch
from app.core.models import User
from app.usecases import RAGService

@pytest.fixture
def mock_mongo_adapter():
    """Fixture para crear un mock del MongoDbAdapter."""
    return MagicMock()

@pytest.fixture
def rag_service(mock_mongo_adapter):
    """Fixture para crear una instancia de RAGService con los adaptadores mockeados."""
    chroma_adapter = MagicMock()
    openai_adapter = MagicMock()
    return RAGService(chroma_adapter, openai_adapter, mock_mongo_adapter)

@pytest.fixture
def mock_configs():
    """Fixture para mockear la clase Configs y sus propiedades."""
    with patch("app.configurations.config") as mock_configs_class:
        mock_instance = mock_configs_class.return_value
        mock_instance.openai_api_key = "mocked_key"
        mock_instance.model = "mocked_model"
        mock_instance.max_tokens = 100
        mock_instance.temperature = 0.5
        yield mock_instance

@pytest.mark.usefixtures("mock_configs")
def test_get_user_by_id_found(rag_service, mock_mongo_adapter):
    """Prueba de get_user_by_id cuando el usuario es encontrado."""
    mock_user_data = {
        "id": "123",
        "name": "John Doe",
        "email": "john@example.com",
        "password": "hashed_password"
    }
    mock_mongo_adapter.get_user_by_id.return_value = mock_user_data

    user = rag_service.get_user_by_id("123")
    assert user is not None
    assert user.id == "123"
    assert user.name == "John Doe"
    assert user.email == "john@example.com"

@pytest.mark.usefixtures("mock_configs")
def test_get_user_by_id_not_found(rag_service, mock_mongo_adapter):
    """Prueba de get_user_by_id cuando el usuario no es encontrado."""
    mock_mongo_adapter.get_user_by_id.return_value = None

    user = rag_service.get_user_by_id("123")
    assert user is None

@pytest.mark.usefixtures("mock_configs")
def test_save_user_success(rag_service, mock_mongo_adapter):
    """Prueba de save_user cuando el usuario es guardado exitosamente."""
    user = User(id="123", name="John Doe", email="john@example.com", password="hashed_password")
    mock_mongo_adapter.save_user.return_value = True

    result = rag_service.save_user(user)
    assert result == "El usuario se ha guardado exitosamente."

@pytest.mark.usefixtures("mock_configs")
def test_save_user_null_fields(rag_service, mock_mongo_adapter):
    """Prueba de save_user cuando los campos del usuario son nulos."""
    user = User(id=None, name=None, email=None, password=None)
    mock_mongo_adapter.save_user.return_value = None

    result = rag_service.save_user(user)
    assert result == "Los campos no pueden ser nulos."

@pytest.mark.usefixtures("mock_configs")
def test_delete_user_success(rag_service, mock_mongo_adapter):
    """Prueba de delete_user cuando el usuario es eliminado exitosamente."""
    mock_mongo_adapter.delete_user.return_value = True

    result = rag_service.delete_user("123")
    assert result == "Usuario eliminado exitosamente."

@pytest.mark.usefixtures("mock_configs")
def test_delete_user_not_found(rag_service, mock_mongo_adapter):
    """Prueba de delete_user cuando el usuario no es encontrado."""
    mock_mongo_adapter.delete_user.return_value = False

    result = rag_service.delete_user("123")
    assert result == "Usuario no encontrado."

@pytest.mark.usefixtures("mock_configs")
def test_update_user_success(rag_service, mock_mongo_adapter):
    """Prueba de update_user cuando el usuario es actualizado exitosamente."""
    mock_mongo_adapter.update_user.return_value = True
    update_data = {"name": "John Updated"}

    result = rag_service.update_user("123", update_data)
    assert result == "Usuario actualizado exitosamente."

@pytest.mark.usefixtures("mock_configs")
def test_update_user_not_found(rag_service, mock_mongo_adapter):
    """Prueba de update_user cuando el usuario no es encontrado."""
    mock_mongo_adapter.update_user.return_value = False
    update_data = {"name": "John Updated"}

    result = rag_service.update_user("123", update_data)
    assert result == "Usuario no encontrado."

@pytest.mark.usefixtures("mock_configs")
def test_login_user_success(rag_service, mock_mongo_adapter):
    """Prueba de login_user cuando el login es exitoso."""
    mock_user_data = {
        "id": "123",
        "name": "John Doe",
        "email": "john@example.com",
        "password": "hashed_password"
    }
    mock_mongo_adapter.login_user.return_value = mock_user_data

    user = rag_service.login_user("john@example.com", "password")
    assert user is not None
    assert user['id'] == "123"

@pytest.mark.usefixtures("mock_configs")
def test_login_user_fail(rag_service, mock_mongo_adapter):
    """Prueba de login_user cuando las credenciales son incorrectas."""
    mock_mongo_adapter.login_user.return_value = None

    user = rag_service.login_user("john@example.com", "wrong_password")
    assert user is None
