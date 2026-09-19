from pydantic import BaseModel


class NoteImportResponse(BaseModel):
    success: bool
    message: str
    topic: str