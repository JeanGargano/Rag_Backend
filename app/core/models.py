import pydantic
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())

#Clase de persistencia para documento
class Document(pydantic.BaseModel):
    id: str = pydantic.Field(default_factory=generate_uuid)
    content: str

#Clase de persistencia para usuario
class User(pydantic.BaseModel):
    id: str = pydantic.Field(default_factory=generate_uuid)
    name: str
    email: str
    password: str
    age: int

