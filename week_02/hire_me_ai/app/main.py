from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.chat import router as chat_router


app = FastAPI()

# Allows the React frontend (running on a different origin/port) to call
# this API from the browser. Vite's default dev port is 5173; 3000 and
# 4173 (vite preview) are included too. Add your deployed frontend's URL
# here as well once you host it.
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
    "https://my-portfolio-ebon-three-87.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


@app.get("/")
def home():
    return {
        "message": "Backend is running"
    }
