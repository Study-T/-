"""FASHN VTON Virtual Try-On Service — GPU-backed FastAPI microservice."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from pathlib import Path

app = FastAPI(title="FASHN VTON Try-On Service", version="0.1.0")

JOBS = {}

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


class TryOnRequest(BaseModel):
    person_image_url: str
    garment_image_url: str


@app.post("/tryon")
async def tryon(req: TryOnRequest):
    task_id = uuid.uuid4().hex
    JOBS[task_id] = {"status": "pending"}

    # TODO: download images, run FASHN VTON inference, upload result
    JOBS[task_id] = {
        "status": "completed",
        "result_url": f"{OUTPUT_DIR}/{task_id}.png",
    }

    return {"task_id": task_id}


@app.get("/task/{task_id}")
async def get_task(task_id: str):
    job = JOBS.get(task_id)
    if not job:
        raise HTTPException(404, "Task not found")
    return {"task_id": task_id, **job}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
