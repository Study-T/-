from pydantic import BaseModel
from typing import Any, Optional


class ErrorResponse(BaseModel):
    code: str
    message: str


class ApiError(BaseModel):
    error: ErrorResponse


class UploadResponse(BaseModel):
    url: str
