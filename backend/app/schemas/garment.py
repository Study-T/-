from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class GarmentCreateRequest(BaseModel):
    category: str
    image_url: str


class GarmentResponse(BaseModel):
    id: int
    category: str
    image_url: str
    metadata_: Optional[dict] = None
    created_at: datetime

    model_config = {"from_attributes": True}
