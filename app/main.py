# app/main.py
from fastapi import FastAPI
from app.api import routers

app = FastAPI()

app.include_router(routers.rag_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)