from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api import routers

app = FastAPI()

# Configuración CORS: permite solicitudes desde http://127.0.0.1:5500
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.rag_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)