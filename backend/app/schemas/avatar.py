from pydantic import BaseModel, Field
from typing import Optional


class AvatarCreateRequest(BaseModel):
    photo_url: str


class AvatarUpdateParamsRequest(BaseModel):
    height: Optional[float] = Field(None, ge=1.0, le=2.5)
    weight: Optional[float] = Field(None, ge=30, le=200)
    shoulder_width: Optional[float] = Field(None, ge=0.3, le=0.6)
    chest: Optional[float] = Field(None, ge=0.5, le=1.5)
    waist: Optional[float] = Field(None, ge=0.4, le=1.5)
    hip: Optional[float] = Field(None, ge=0.5, le=1.5)
    leg_length: Optional[float] = Field(None, ge=0.5, le=1.2)


class AvatarResponse(BaseModel):
    id: int
    user_id: int
    photo_url: str
    smplx_params: Optional[dict] = None
    model_url: Optional[str] = None
    status: str
    created_at: str

    class Config:
        from_attributes = True
