from pathlib import Path

from .notes_service import import_notes


def import_notes_controller(file, topic: str):

    temp_path = Path("data/raw") / file.filename

    temp_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(temp_path, "wb") as buffer:
        buffer.write(file.file.read())

    result = import_notes(
        file_path=temp_path,
        topic=topic
    )

    return {
        "success": True,
        "message": "Notes imported successfully",
        "topic": topic
    }