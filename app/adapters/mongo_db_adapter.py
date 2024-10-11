from http.client import HTTPException
from typing import List, Optional, Dict
from app.core import ports, models
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId


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

    #----------------------------------------------------------Metodos--------------------------------------------------


    #Metodo para obtener un usuario por su id
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        try:
            user = self.collection.find_one({"_id": ObjectId(user_id)})
            return user
        except PyMongoError as e:
            print(f"Error getting user: {e}")
            return None


    #Metodo para crear
    def save_user(self, user: models.User) -> Optional[models.User]:
        try:
            user_data = user.dict(by_alias=True)
            result = self.collection.insert_one(user_data)
            if result.inserted_id:
                return user
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Error saving user: {e}")

    #Metodo para eliminar usuario
    def delete_user(self, user_id: str) -> bool:
        try:
            if not ObjectId.is_valid(user_id):
                raise ValueError("Invalid ID format")
            result = self.collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"Error deleting user: {e}")
            return False
        except ValueError as e:
            print(f"Invalid ID format: {e}")
            return False

    #Metodo para actualizar usuario
    def update_user(self, user_id: str, update_data: dict) -> Optional[models.User]:
        try:
            result = self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
            if result.modified_count > 0:
                return self.collection.find_one({"_id": ObjectId(user_id)})
        except PyMongoError as e:
            print(f"Error updating user: {e}")
        return None

    #Metodo para listar usuarios
    def list_users(self) -> List[Dict[str, str]]:
        try:
            # Realiza la búsqueda y selecciona solo los campos 'name' y 'email'
            users = self.collection.find(
                {"name": {"$ne": None}, "email": {"$ne": None}},  # Filtra usuarios donde 'name' y 'email' no sean null
                {"name": 1, "email": 1}  # Solo selecciona 'name' y 'email'
            )

            # Convierte el cursor a una lista de diccionarios
            user_list = []
            for user in users:
                # MongoDB siempre incluye el campo '_id', lo eliminamos manualmente si no lo necesitas
                user.pop('_id', None)
                user_list.append(user)

            return user_list

        except PyMongoError as e:
            print(f"Error listing users: {e}")
            return []


        except PyMongoError as e:
            print(f"Error listing users: {e}")
            return []

    #Metodo para actualizar rol

    def login_user(self, email: str, password: str) -> models.User:
        try:
            print(f"Intentando iniciar sesión con email: {email}")
            usuario_data = self.collection.find_one({"email": email})

            if usuario_data is None:
                print("Usuario no encontrado")
                return None

            if usuario_data["password"] != password:
                print("Contraseña incorrecta")
                return None

            usuario = models.User(**usuario_data)
            print("Inicio de sesión exitoso")
            return usuario

        except PyMongoError as e:
            print(f"Error de base de datos: {e}")
            raise


