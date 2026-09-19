from fastapi import FastAPI

from modules.notes.notes_routes import router as notes_router


app = FastAPI(
    title="Personal Notes RAG"
)


app.include_router(notes_router)


@app.get("/")
def root():
    return {
        "message": "Personal Notes RAG API"
    }