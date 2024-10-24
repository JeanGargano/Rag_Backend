import pytest
from unittest.mock import MagicMock
import os
from pathlib import Path

from app.core.models import User
from app.usecases import RAGService
from app.core import ports
from app.configurations import get_configs

# Asegurarse de que el archivo .env.test existe y tiene las variables correctas
@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Crear archivo .env.test temporal para las pruebas"""
    env_test_path = Path('.env.test')
    env_content = """
OPENAI_API_KEY=test-key
MODEL=gpt-4
MAX_TOKENS=80
TEMPERATURE=0.7
"""
    env_test_path.write_text(env_content.strip())
    yield
    # Limpieza después de las pruebas
    if env_test_path.exists():
        env_test_path.unlink()

@pytest.fixture(scope="session")
def app_config(setup_test_env):
    """Fixture para cargar la configuración de test."""
    return get_configs('.env.test')

@pytest.fixture
def mock_mongo_adapter():
    """Fixture para crear un mock del MongoDbAdapter."""
    return MagicMock(spec=ports.UserRepositoryPort)

@pytest.fixture
def rag_service(mock_mongo_adapter, app_config):
    """Fixture para crear una instancia de RAGService con el mock del adaptador."""
    chroma_adapter = MagicMock()
    openai_adapter = MagicMock()
    return RAGService(chroma_adapter, openai_adapter, mock_mongo_adapter)

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


def test_get_user_by_id_not_found(rag_service, mock_mongo_adapter):
    """Prueba de get_user_by_id cuando el usuario no es encontrado."""
    mock_mongo_adapter.get_user_by_id.return_value = None

    user = rag_service.get_user_by_id("123")
    assert user is None


def test_save_user_success(rag_service, mock_mongo_adapter):
    """Prueba de save_user cuando el usuario es guardado exitosamente."""
    user = User(id="123", name="John Doe", email="john@example.com", password="hashed_password")
    mock_mongo_adapter.save_user.return_value = True

    result = rag_service.save_user(user)
    assert result == "El usuario se ha guardado exitosamente."


def test_save_user_null_fields(rag_service, mock_mongo_adapter):
    """Prueba de save_user cuando los campos del usuario son nulos."""
    user = User(id=None, name=None, email=None, password=None)
    mock_mongo_adapter.save_user.return_value = None

    result = rag_service.save_user(user)
    assert result == "Los campos no pueden ser nulos."


def test_delete_user_success(rag_service, mock_mongo_adapter):
    """Prueba de delete_user cuando el usuario es eliminado exitosamente."""
    mock_mongo_adapter.delete_user.return_value = True

    result = rag_service.delete_user("123")
    assert result == "Usuario eliminado exitosamente."


def test_delete_user_not_found(rag_service, mock_mongo_adapter):
    """Prueba de delete_user cuando el usuario no es encontrado."""
    mock_mongo_adapter.delete_user.return_value = False

    result = rag_service.delete_user("123")
    assert result == "Usuario no encontrado."


def test_update_user_success(rag_service, mock_mongo_adapter):
    """Prueba de update_user cuando el usuario es actualizado exitosamente."""
    mock_mongo_adapter.update_user.return_value = True
    update_data = {"name": "John Updated"}

    result = rag_service.update_user("123", update_data)
    assert result == "Usuario actualizado exitosamente."


def test_update_user_not_found(rag_service, mock_mongo_adapter):
    """Prueba de update_user cuando el usuario no es encontrado."""
    mock_mongo_adapter.update_user.return_value = False
    update_data = {"name": "John Updated"}

    result = rag_service.update_user("123", update_data)
    assert result == "Usuario no encontrado."


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


def test_login_user_fail(rag_service, mock_mongo_adapter):
    """Prueba de login_user cuando las credenciales son incorrectas."""
    mock_mongo_adapter.login_user.return_value = None

    user = rag_service.login_user("john@example.com", "wrong_password")
    assert user is None


