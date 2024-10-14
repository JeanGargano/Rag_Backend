from typing import Optional

import pydantic
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())

#Clase de para documento
class Document(pydantic.BaseModel):
    id: str = pydantic.Field(default_factory=generate_uuid)
    content: str
    file_type: str

#Clase para usuario
class User(pydantic.BaseModel):
    #Campos opcionales para el momento de actualizar
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None
    rol: str = "Usuario"

class LoginRequest(pydantic.BaseModel):
    email: str
    password: str