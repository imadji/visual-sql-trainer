from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import subprocess
from io import BytesIO

router = APIRouter(prefix="/auth")


@router.get("/dump/schema/{schema_name}", response_class=StreamingResponse)
async def dump_schema(schema_name: str):
    """
    Генерирует и отдает дамп указанной схемы БД
    """
    try:
        cmd = [
            "pg_dump",
            "-U",
            "root",
            "-d",
            "umom_db",
            "-n",
            schema_name,
            "-Fp",
            "-w",
        ]

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={"PGPASSWORD": "root"},
        )

        def generate():
            while True:
                chunk = process.stdout.read(4096)
                if not chunk:
                    break
                yield chunk

        return StreamingResponse(
            generate(),
            media_type="application/sql",
            headers={
                "Content-Disposition": f"attachment; filename={schema_name}_dump.sql"
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
