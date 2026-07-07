import os
import uuid
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from starlette.background import BackgroundTask
import anyio

import converter
import converter2

app = FastAPI(title="Video Converter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


def cleanup_files(*paths: Path):
    for path in paths:
        try:
            if path.exists():
                path.unlink()
        except Exception as e:
            print(f"Error deleting temp file {path}: {e}")


async def _save_upload(file: UploadFile, destination_path: Path):
    with destination_path.open("wb") as f:
        while chunk := await file.read(1024 * 1024):  # 1MB chunks
            f.write(chunk)


@app.get("/")
def root():
    return {"message": "Video converter API is running"}


@app.post("/convert")
async def convert_mp4_to_mkv(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".mp4"):
        return JSONResponse(status_code=400, content={"error": "Only MP4 files are supported."})

    temp_dir = Path(tempfile.gettempdir())
    input_path = temp_dir / f"input_{uuid.uuid4().hex}.mp4"
    output_path = temp_dir / f"output_{uuid.uuid4().hex}.mkv"

    try:
        await _save_upload(file, input_path)
        
        # Run conversion in a worker thread to prevent event loop blocking
        await anyio.to_thread.run_sync(converter2.convert_mp4_to_mkv, str(input_path), str(output_path))
        
        if not output_path.exists() or output_path.stat().st_size == 0:
            cleanup_files(input_path, output_path)
            return JSONResponse(status_code=500, content={"error": "Conversion did not produce a valid output file."})

        original_stem = Path(file.filename).stem
        download_name = f"{original_stem}.mkv"

        return FileResponse(
            path=output_path,
            media_type="video/x-matroska",
            filename=download_name,
            background=BackgroundTask(cleanup_files, input_path, output_path),
        )
    except Exception as e:
        cleanup_files(input_path, output_path)
        return JSONResponse(status_code=500, content={"error": f"Conversion failed: {str(e)}"})


@app.post("/convert-mkv-to-mp4")
async def convert_mkv_to_mp4(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".mkv"):
        return JSONResponse(status_code=400, content={"error": "Only MKV files are supported."})

    temp_dir = Path(tempfile.gettempdir())
    input_path = temp_dir / f"input_{uuid.uuid4().hex}.mkv"
    output_path = temp_dir / f"output_{uuid.uuid4().hex}.mp4"

    try:
        await _save_upload(file, input_path)
        
        # Run conversion in a worker thread to prevent event loop blocking
        await anyio.to_thread.run_sync(converter.convert_mkv_to_mp4, str(input_path), str(output_path))
        
        if not output_path.exists() or output_path.stat().st_size == 0:
            cleanup_files(input_path, output_path)
            return JSONResponse(status_code=500, content={"error": "Conversion did not produce a valid output file."})

        original_stem = Path(file.filename).stem
        download_name = f"{original_stem}.mp4"

        return FileResponse(
            path=output_path,
            media_type="video/mp4",
            filename=download_name,
            background=BackgroundTask(cleanup_files, input_path, output_path),
        )
    except Exception as e:
        cleanup_files(input_path, output_path)
        return JSONResponse(status_code=500, content={"error": f"Conversion failed: {str(e)}"})
