from fastapi import APIRouter, UploadFile, File, Form

from .notes_controller import import_notes_controller


router = APIRouter(
    prefix="/api/v1/notes",
    tags=["Notes"]
)


@router.post("/import")
async def import_notes(
    file: UploadFile = File(...),
    topic: str = Form(...)
):

    return import_notes_controller(
        file=file,
        topic=topic
    )