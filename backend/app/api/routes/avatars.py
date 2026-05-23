from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import current_user
from app.core.database import get_db
from app.models.avatar import Avatar, AvatarStatus
from app.schemas.avatar import AvatarCreateRequest, AvatarUpdateParamsRequest, AvatarResponse

router = APIRouter(prefix="/api/avatars", tags=["avatars"])


async def get_avatar_or_404(avatar_id: int, user_id: int, db: AsyncSession) -> Avatar:
    result = await db.execute(
        select(Avatar).where(Avatar.id == avatar_id, Avatar.user_id == user_id)
    )
    avatar = result.scalar_one_or_none()
    if not avatar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="数字人不存在")
    return avatar


@router.post("", response_model=AvatarResponse, status_code=status.HTTP_201_CREATED)
async def create_avatar(
    req: AvatarCreateRequest,
    user_id: int = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    count_result = await db.execute(
        select(func.count(Avatar.id)).where(
            Avatar.user_id == user_id, Avatar.status != "failed"
        )
    )
    if count_result.scalar() >= 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="最多创建 3 个数字人")

    avatar = Avatar(user_id=user_id, photo_url=req.photo_url, status=AvatarStatus.pending)
    db.add(avatar)
    await db.commit()
    await db.refresh(avatar)

    from app.tasks.ai_tasks import generate_avatar
    generate_avatar.delay(avatar.id, req.photo_url)

    return AvatarResponse.model_validate(avatar)


@router.get("", response_model=list[AvatarResponse])
async def list_avatars(
    user_id: int = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Avatar).where(Avatar.user_id == user_id).order_by(Avatar.created_at.desc())
    )
    return [AvatarResponse.model_validate(a) for a in result.scalars().all()]


@router.get("/{avatar_id}", response_model=AvatarResponse)
async def get_avatar(
    avatar_id: int,
    user_id: int = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    avatar = await get_avatar_or_404(avatar_id, user_id, db)
    return AvatarResponse.model_validate(avatar)


@router.put("/{avatar_id}/params", response_model=AvatarResponse)
async def update_avatar_params(
    avatar_id: int,
    req: AvatarUpdateParamsRequest,
    user_id: int = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    avatar = await get_avatar_or_404(avatar_id, user_id, db)
    params = avatar.smplx_params or {}
    for field, value in req.model_dump(exclude_unset=True).items():
        if value is not None:
            params[field] = value
    avatar.smplx_params = params
    await db.commit()
    await db.refresh(avatar)
    return AvatarResponse.model_validate(avatar)


@router.delete("/{avatar_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_avatar(
    avatar_id: int,
    user_id: int = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    avatar = await get_avatar_or_404(avatar_id, user_id, db)
    await db.delete(avatar)
    await db.commit()
