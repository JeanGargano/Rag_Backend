import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form
from app import usecases
from app.api import dependencies
from app.core import models
from typing import List, Optional

from app.core.models import LoginRequest
from app.usecases import RAGService
from fastapi import File, UploadFile
from pydantic import BaseModel


rag_router = APIRouter()

# Definir el esquema para el cuerpo de la solicitud
class QueryRequest(BaseModel):
    query: str

#----------------------------------------------------Endpoint para OpenAI-----------------------------------------------
# Generar respuesta
@rag_router.post("/generate-answer/")
def generate_answer(request: QueryRequest, rag_service: RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    query = request.query
    answer = rag_service.generate_answer(query)
    return {"answer": answer}

ADMIN_CODE = "5admin89x"

# Función para validar el código de administrador
def validate_admin_code(admin_code: str) -> bool:
    return admin_code == ADMIN_CODE
#----------------------------------------------------Endpoints para documentos------------------------------------------


@rag_router.post("/save-document/")
async def save_document(file: UploadFile = File(...), rag_service: RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    file_content = await file.read()

    # Definir la ruta donde se guardará el archivo
    save_path = os.path.join(os.getcwd(), file.filename)

    # Escribir el contenido en el disco duro
    with open(save_path, "wb") as f:
        f.write(file_content)

    # Obtener la extensión del archivo y convertirla a minúsculas
    file_extension = file.filename.split('.')[-1].lower()

    # Llamamos al método para guardar el documento
    result = rag_service.save_document(file_path=save_path, file_type=file_extension)

    if "Error" in result:
        return {"message": "Error al guardar el documento."}

    return {"message": "Documento guardado exitosamente."}
# Listar documentos general
@rag_router.get("/get-documents", response_model=List[models.Document])
def get_documents(rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    try:
        documents = rag_service.get_documents()
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Problemas al devolver los documentos: {str(e)}")

# Listar documento ID

@rag_router.get("/get-document/{doc_id}", response_model=List[models.Document])
async def get_document_id(doc_id: str ,rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    try:
        document = rag_service.get_document_id(doc_id)
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Problemas al devolver el documento: {str(e)}")

# Actualizar documento por ID

@rag_router.put("/update-document/{doc_id}", response_model=str)
async def update_document(doc_id: str, document: models.Document ,rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    try:
        response = rag_service.update_document(doc_id, content= document.content)
        if "Error" in response:
            raise HTTPException(status_code=404, detail=f"No encontrado el documento {doc_id}")
        return {"status": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Eliminar documento por ID

#-----------------------------------------------------Endpoints para usuarios-------------------------------------------

#Guardar usuario
@rag_router.post("/save-user/", status_code=201)
async def save_user(user: models.User, admin_code: Optional[str] = None,
                    rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    try:
        if user.rol == "Administrador" and not validate_admin_code(admin_code):
            raise HTTPException(status_code=403, detail="Código de administrador incorrecto")

        result = rag_service.save_user(user)
        if "Error" in result:
            raise HTTPException(status_code=400, detail=result)
        return {"status": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


#Eliminar usuario
@rag_router.delete("/delete-user/{user_id}", status_code=200)
async def delete_user(user_id: str, rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    try:
        result = rag_service.delete_user(user_id)
        if "Error" in result:
            raise HTTPException(status_code=404, detail=result)
        return {"status": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


#Actualizar usuario
@rag_router.put("/update-rol/{user_id}", status_code=200)
async def update_user(user_id: str, user: models.User, rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    try:
        # Obtener el usuario existente para asegurarse de que el usuario exista
        existing_user = rag_service.get_user_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Actualiza solo los campos proporcionados
        update_data = user.dict(exclude_unset=True)  # Solo incluye los campos que se han proporcionado
        result = rag_service.update_user(user_id, update_data)
        if "Error" in result:
            raise HTTPException(status_code=404, detail=result)
        return {"status": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Listar usuario by ID
@rag_router.get("/get-user/{user_id}", response_model=models.User)
async def get_user_by_id( user_id: str ,rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    try:
        user = rag_service.get_user_by_id(user_id)
        return user

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Usuario con id: {str(user_id)} no encontrado. Error: {str(e)}")

#Listar usuarios
@rag_router.get("/list-users/", response_model=List[models.User])
async def list_users(rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    try:
        users = rag_service.list_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

#Actualizar Rol
@rag_router.put("/update-user/{user_id}", status_code=200)
async def update_user(user_id: str, user: models.User, rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    try:
        # Obtener el usuario existente para asegurarse de que el usuario exista
        existing_user = rag_service.get_user_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Actualiza solo los campos proporcionados
        update_data = user.dict(exclude_unset=True)  # Solo incluye los campos que se han proporcionado
        print(update_data)
        result = rag_service.update_user(user_id, update_data)
        if "Error" in result:
            raise HTTPException(status_code=404, detail=result)
        return {"status": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

#Validar Usuario
@rag_router.post("/user/validate")
async def validar_usuario(login_request: models.LoginRequest, rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    try:
        user = rag_service.login_user(login_request.email, login_request.password)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado o contraseña incorrecta")

        # Si el login es exitoso, devolvemos los detalles del usuario (incluyendo su rol)
        return {"name": user.name, "email": user.email, "rol": user.rol}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

