from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import current_user
from app.core.database import get_db
from app.models.avatar import Avatar
from app.models.garment import Garment
from app.models.tryon import TryOnTask, TryOnStatus
from app.schemas.tryon import TryOnRequest, TryOnResponse

router = APIRouter(prefix="/api/tryon", tags=["tryon"])


@router.post("", response_model=TryOnResponse, status_code=status.HTTP_201_CREATED)
async def create_tryon(
    req: TryOnRequest,
    user_id: int = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    avatar_result = await db.execute(
        select(Avatar).where(Avatar.id == req.avatar_id, Avatar.user_id == user_id)
    )
    avatar = avatar_result.scalar_one_or_none()
    if not avatar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="数字人不存在")

    garment_result = await db.execute(select(Garment).where(Garment.id == req.garment_id))
    garment = garment_result.scalar_one_or_none()
    if not garment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="服装不存在")

    task = TryOnTask(
        user_id=user_id, avatar_id=req.avatar_id, garment_id=req.garment_id,
        status=TryOnStatus.pending,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)

    try:
        from app.tasks.ai_tasks import run_tryon
        run_tryon.delay(task.id, avatar.model_url or "", garment.image_url)
    except Exception:
        import asyncio, threading
        from app.tasks.ai_tasks import run_tryon_task
        threading.Thread(
            target=lambda: asyncio.run(
                run_tryon_task(task.id, avatar.model_url or "", garment.image_url)
            ),
            daemon=True,
        ).start()

    return TryOnResponse.model_validate(task)


@router.get("/{task_id}", response_model=TryOnResponse)
async def get_tryon_task(
    task_id: int,
    user_id: int = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TryOnTask).where(TryOnTask.id == task_id, TryOnTask.user_id == user_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
    return TryOnResponse.model_validate(task)


@router.get("", response_model=list[TryOnResponse])
async def list_tryon_history(
    user_id: int = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TryOnTask).where(TryOnTask.user_id == user_id)
        .order_by(TryOnTask.created_at.desc()).limit(50)
    )
    return [TryOnResponse.model_validate(t) for t in result.scalars().all()]
