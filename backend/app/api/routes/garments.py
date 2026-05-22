from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import current_user
from app.core.database import get_db
from app.models.garment import Garment
from app.schemas.garment import GarmentCreateRequest, GarmentResponse

router = APIRouter(prefix="/api/garments", tags=["garments"])


@router.post("", response_model=GarmentResponse, status_code=status.HTTP_201_CREATED)
async def create_garment(
    req: GarmentCreateRequest,
    user_id: int = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    garment = Garment(category=req.category, image_url=req.image_url)
    db.add(garment)
    await db.commit()
    await db.refresh(garment)
    return GarmentResponse.model_validate(garment)


@router.get("", response_model=list[GarmentResponse])
async def list_garments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Garment).order_by(Garment.created_at.desc()).limit(100))
    return [GarmentResponse.model_validate(g) for g in result.scalars().all()]


@router.get("/{garment_id}", response_model=GarmentResponse)
async def get_garment(garment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Garment).where(Garment.id == garment_id))
    garment = result.scalar_one_or_none()
    if not garment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="服装不存在")
    return GarmentResponse.model_validate(garment)
