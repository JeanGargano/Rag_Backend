from fastapi import APIRouter, Depends, HTTPException
from app import usecases
from app.api import dependencies
from app.core import models
from typing import List

rag_router = APIRouter()

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
        user_model = usecases.User(id=None, name=user.name, email=user.email, age=user.age)
        result = rag_service.save_user(user_model)
        if result:
            return {"status": "User saved successfully", "user": result}
        raise HTTPException(status_code=400, detail="Failed to save user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

#Eliminar usuario
@rag_router.delete("/delete-user/{user_id}", status_code=200)
async def delete_user(user_id: str, rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    try:
        result = rag_service.delete_user(user_id)
        if result:
            return {"status": "User deleted successfully"}
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

#Actualizar usuario
@rag_router.put("/update-user/{user_id}", status_code=200)
async def update_user(user_id: str, user: models.User, rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    try:
        user_model = usecases.User(id=user_id, name=user.name, email=user.email, age=user.age)
        result = rag_service.update_user(user_model)
        if result:
            return {"status": "User updated successfully", "user": result}
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

#Listar usuarios
@rag_router.get("/list-users/", response_model=List[models.User])
async def list_users(rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    try:
        result = rag_service.list_users()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")