import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from pymongo.errors import PyMongoError
from app.adapters.mongo_db_adapter import MongoDbAdapter
from app.core.models import User


@pytest.fixture
def mock_collection():
    return MagicMock()


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_client():
    with patch('pymongo.MongoClient') as mock:
        client = MagicMock()
        client.Rag_System = MagicMock()
        client.Rag_System.User = MagicMock()
        mock.return_value = client
        yield mock


@pytest.fixture
def mongo_adapter(mock_client, mock_db, mock_collection):
    with patch.object(MongoDbAdapter, '__init__', return_value=None):
        adapter = MongoDbAdapter()
        adapter.client = mock_client
        adapter.db = mock_db
        adapter.collection = mock_collection
        return adapter


def test_init_success():
    """Test successful initialization of MongoDbAdapter"""
    with patch('pymongo.MongoClient') as mock_client:
        mock_client.return_value.Rag_System.User = MagicMock()
        adapter = MongoDbAdapter()
        assert adapter.client is not None
        assert adapter.db is not None
        assert adapter.collection is not None


def test_get_user_by_id_success(mongo_adapter):
    """Test successful user retrieval by ID"""
    mock_id = str(ObjectId())
    expected_user = {
        "_id": ObjectId(mock_id),
        "name": "Test User",
        "email": "test@test.com"
    }
    mongo_adapter.collection.find_one.return_value = expected_user

    result = mongo_adapter.get_user_by_id(mock_id)

    assert result is not None
    assert result["name"] == "Test User"
    assert result["email"] == "test@test.com"
    assert "id" in result
    assert "_id" not in result


def test_get_user_by_id_not_found(mongo_adapter):
    """Test user retrieval when user doesn't exist"""
    mongo_adapter.collection.find_one.return_value = None
    result = mongo_adapter.get_user_by_id(str(ObjectId()))
    assert result is None


def test_save_user_success(mongo_adapter):
    """Test successful user creation"""
    user = User(
        id="507f1f77bcf86cd799439011",
        name="Test User",
        email="test@test.com",
        password="password123"
    )
    mongo_adapter.collection.insert_one.return_value.inserted_id = ObjectId()

    result = mongo_adapter.save_user(user)
    assert result is not None
    assert isinstance(result, User)


def test_save_user_failure(mongo_adapter):
    """Test failed user creation"""
    user = User(
        id="507f1f77bcf86cd799439011",
        name="Test User",
        email="test@test.com",
        password="password123"
    )
    mongo_adapter.collection.insert_one.side_effect = PyMongoError()

    with pytest.raises(Exception):
        mongo_adapter.save_user(user)


def test_delete_user_success(mongo_adapter):
    """Test successful user deletion"""
    mock_id = str(ObjectId())
    mongo_adapter.collection.delete_one.return_value.deleted_count = 1

    result = mongo_adapter.delete_user(mock_id)
    assert result is True


def test_delete_user_not_found(mongo_adapter):
    """Test deletion of non-existent user"""
    mock_id = str(ObjectId())
    mongo_adapter.collection.delete_one.return_value.deleted_count = 0

    result = mongo_adapter.delete_user(mock_id)
    assert result is False


def test_delete_user_invalid_id(mongo_adapter):
    """Test deletion with invalid ID format"""
    result = mongo_adapter.delete_user("invalid_id")
    assert result is False


def test_update_user_success(mongo_adapter):
    """Test successful user update"""
    mock_id = str(ObjectId())
    update_data = {"name": "Updated Name"}
    mongo_adapter.collection.update_one.return_value.modified_count = 1
    mongo_adapter.collection.find_one.return_value = {
        "_id": ObjectId(mock_id),
        "name": "Updated Name"
    }

    result = mongo_adapter.update_user(mock_id, update_data)
    assert result is not None


def test_update_user_not_found(mongo_adapter):
    """Test update of non-existent user"""
    mock_id = str(ObjectId())
    update_data = {"name": "Updated Name"}
    mongo_adapter.collection.update_one.return_value.modified_count = 0

    result = mongo_adapter.update_user(mock_id, update_data)
    assert result is None


def test_list_users_success(mongo_adapter):
    """Test successful retrieval of user list"""
    mock_users = [
        {
            "_id": ObjectId(),
            "name": "User 1",
            "email": "user1@test.com",
            "rol": "admin",
            "password": "pass123"
        },
        {
            "_id": ObjectId(),
            "name": "User 2",
            "email": "user2@test.com",
            "rol": "user",
            "password": "pass456"
        }
    ]
    mongo_adapter.collection.find.return_value = mock_users

    result = mongo_adapter.list_users()
    assert len(result) == 2
    assert all(isinstance(user["id"], str) for user in result)
    assert all("_id" not in user for user in result)


def test_list_users_empty(mongo_adapter):
    """Test retrieval of empty user list"""
    mongo_adapter.collection.find.return_value = []
    result = mongo_adapter.list_users()
    assert len(result) == 0


def test_login_user_success(mongo_adapter):
    """Test successful user login"""
    mock_user = {
        "_id": ObjectId(),
        "email": "test@test.com",
        "password": "password123",
        "name": "Test User"
    }
    mongo_adapter.collection.find_one.return_value = mock_user

    result = mongo_adapter.login_user("test@test.com", "password123")
    assert result is not None
    assert isinstance(result, User)


def test_login_user_invalid_credentials(mongo_adapter):
    """Test login with invalid credentials"""
    mock_user = {
        "_id": ObjectId(),
        "email": "test@test.com",
        "password": "password123",
        "name": "Test User"
    }
    mongo_adapter.collection.find_one.return_value = mock_user

    result = mongo_adapter.login_user("test@test.com", "wrongpassword")
    assert result is None


def test_login_user_not_found(mongo_adapter):
    """Test login with non-existent user"""
    mongo_adapter.collection.find_one.return_value = None
    result = mongo_adapter.login_user("nonexistent@test.com", "password123")
    assert result is None