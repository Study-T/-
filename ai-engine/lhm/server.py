"""LHM Avatar Generation Service — GPU-backed FastAPI microservice."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import uuid
from pathlib import Path

app = FastAPI(title="LHM Avatar Service", version="0.1.0")

JOBS = {}

MODEL_DIR = Path(__file__).parent / "models"
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


class GenerateRequest(BaseModel):
    image_url: str


class TaskStatus(BaseModel):
    task_id: str
    status: str
    smplx_params: dict | None = None
    model_url: str | None = None


@app.post("/generate")
async def generate(req: GenerateRequest):
    task_id = uuid.uuid4().hex
    JOBS[task_id] = {"status": "pending"}

    # TODO: download image, run LHM inference, upload result
    # For now: placeholder that simulates processing
    JOBS[task_id] = {
        "status": "completed",
        "smplx_params": {"height": 1.70, "weight": 65, "shoulder_width": 0.42},
        "model_url": f"{OUTPUT_DIR}/{task_id}.glb",
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
    uvicorn.run(app, host="0.0.0.0", port=8001)
