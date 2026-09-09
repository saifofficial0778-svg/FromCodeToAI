from fastapi import FastAPI

from app.api.routes.chat import router as chat_router


app = FastAPI()

app.include_router(chat_router)


@app.get("/")
def home():
    return {
        "message": "Backend is running"
    }