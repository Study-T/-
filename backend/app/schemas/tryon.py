from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class TryOnRequest(BaseModel):
    avatar_id: int
    garment_id: int


class TryOnResponse(BaseModel):
    id: int
    user_id: int
    avatar_id: int
    garment_id: int
    result_url: Optional[str] = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
