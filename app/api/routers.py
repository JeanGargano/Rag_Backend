from fastapi import APIRouter, Depends, HTTPException
from app import usecases
from app.api import dependencies
from app.core import models
from typing import List

rag_router = APIRouter()
#La linea anterior sirve para configurar rutas para cada uno de los metodos de rag service

#----------------------------------------------------Endpoint para OpenAi-----------------------------------------------
#Generar respuesta
@rag_router.post("/generate-answer/")
def generate_answer(query: str, rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    return {"answer": rag_service.generate_answer(query)}

#----------------------------------------------------Endpoints para documentos------------------------------------------
#Guardar documento
@rag_router.post("/save-document/")
def save_document(document: models.Document, rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    rag_service.save_document(content=document.content)
    return {"status": "Document saved successfully"}, 201

#Faltan los de listar y eliminar


#-----------------------------------------------------Endpoints para usuarios-------------------------------------------

#Guardar usuario
@rag_router.post("/save-user/", status_code=201)
async def save_user(user: models.User, rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    try:
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
@rag_router.put("/update-user/{user_id}", status_code=200)
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


#Listar usuarios
@rag_router.get("/list-users/", response_model=List[models.User])
async def list_users(rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    try:
        users = rag_service.list_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


