from typing import Optional

import pydantic
import uuid

#En esta archivo se definen los modelos de datos que se tendran en cuenta al momento de la persistencia

def generate_uuid() -> str:
    return str(uuid.uuid4())

#Clase de para documento
class Document(pydantic.BaseModel):
    id: str = pydantic.Field(default_factory=generate_uuid)
    content: str

#Clase para usuario
class User(pydantic.BaseModel):
    #Campos opcionales para el momento de actualizar
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    age: Optional[int] = None