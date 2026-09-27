import inspect
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from starlette.concurrency import run_in_threadpool

from app.schemas.chat import ChatRequest
from app.services.chat_service import ask_candidate
from app.services.pdf_service import read_pdf
from app.services.resume_service import parse_resume
from supabase_client import log_chat


router = APIRouter()


def get_client_ip(http_request: Request) -> str | None:
    forwarded = http_request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return http_request.client.host if http_request.client else None


@router.post("/chat")
def chat(request: ChatRequest, http_request: Request):

    project_root = Path(__file__).resolve().parents[3]

    resume_path = project_root / "data" / "Mohd_Saif_Main_00.pdf"

    resume_text = read_pdf(resume_path)

    resume = parse_resume(resume_text)

    ip_address = get_client_ip(http_request)
    user_agent = http_request.headers.get("user-agent")

    stream = ask_candidate(request.question, resume)

    async def stream_and_log():
        full_answer = ""

        # ask_candidate sync ya async generator, dono ho sakte hain — auto-detect
        if inspect.isasyncgen(stream):
            async for chunk in stream:
                full_answer += chunk
                yield chunk
        else:
            for chunk in stream:
                full_answer += chunk
                yield chunk

        # DB insert ek blocking call hai, threadpool mein daala taaki
        # server ka event loop block na ho
        await run_in_threadpool(
            log_chat,
            question=request.question,
            answer=full_answer,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    return StreamingResponse(stream_and_log(), media_type="text/plain")