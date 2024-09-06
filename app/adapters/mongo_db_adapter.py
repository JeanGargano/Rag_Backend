from typing import List, Optional
from app.core import ports, models
from pymongo import MongoClient
from pymongo.errors import PyMongoError


class MongoDbAdapter(ports.UserRepositoryPort):

    #Creando conexion a la BD
    def __init__(self):
        try:
            self.client = MongoClient("mongodb+srv://jean:root@bd2.evaabnw.mongodb.net/")
            self.db = self.client['Rag_System']
            self.collection = self.db['User']
        except PyMongoError as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    #Cerrando la conexion
    def __del__(self):
        if hasattr(self, 'client'):
            self.client.close()

    #Metodo para crear
    def save_user(self, user: models.User) -> Optional[models.User]:
        try:
            user_data = user.dict()
            result = self.collection.insert_one(user_data)
            if result.inserted_id:
                return user
        except PyMongoError as e:
            print(f"Error saving user: {e}")
        return None

    #Metodo para eliminar
    def delete_user(self, user_id: str) -> bool:
        try:
            result = self.collection.delete_one({"id": user_id})
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"Error deleting user: {e}")
        return False

    #Metodo para actualizar
    def update_user(self, user: models.User) -> Optional[models.User]:
        try:
            update_data = {"$set": user.dict()}
            result = self.collection.update_one({"id": user.id}, update_data)
            if result.modified_count > 0:
                return user
        except PyMongoError as e:
            print(f"Error updating user: {e}")
        return None

    #Metodo para listar
    def list_users(self) -> List[models.User]:
        try:
            users = self.collection.find()
            return [models.User(**user) for user in users]
        except PyMongoError as e:
            print(f"Error listing users: {e}")
        return []