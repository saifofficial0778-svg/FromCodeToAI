from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.services.chat_service import ask_candidate
from app.services.pdf_service import read_pdf
from app.services.resume_service import parse_resume

from pathlib import Path


router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):

    project_root = Path(__file__).resolve().parents[3]

    resume_path = project_root / "data" / "Mohd_Saif_Main_00.pdf"

    resume_text = read_pdf(resume_path)

    resume = parse_resume(resume_text)

    return StreamingResponse(
        ask_candidate(request.question, resume),
        media_type="text/plain"
    )