import asyncio
import json

from celery import shared_task

from app.models.avatar import AvatarStatus
from app.models.tryon import TryOnStatus


async def _update_avatar_status(avatar_id: int, status: str, **kwargs):
    from app.core.database import async_session
    from app.models.avatar import Avatar
    from sqlalchemy import select

    async with async_session() as db:
        result = await db.execute(select(Avatar).where(Avatar.id == avatar_id))
        avatar = result.scalar_one_or_none()
        if not avatar:
            return
        avatar.status = AvatarStatus(status)
        for k, v in kwargs.items():
            setattr(avatar, k, v)
        await db.commit()


async def _update_tryon_status(task_id: int, status: str, **kwargs):
    from app.core.database import async_session
    from app.models.tryon import TryOnTask
    from sqlalchemy import select

    async with async_session() as db:
        result = await db.execute(select(TryOnTask).where(TryOnTask.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            return
        task.status = TryOnStatus(status)
        for k, v in kwargs.items():
            setattr(task, k, v)
        await db.commit()


@shared_task(bind=True, max_retries=2, default_retry_delay=10)
def generate_avatar(self, avatar_id: int, photo_url: str):
    """
    Celery task: call LHM service to generate 3D avatar.
    In dev mode without GPU, simulates processing with delays.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def run():
        await _update_avatar_status(avatar_id, "processing")

        # TODO: call LHM API — POST /generate {image_url: photo_url}
        # For now, simulate 5-second processing
        await asyncio.sleep(5)

        smplx_params = {"height": 1.70, "weight": 65, "shoulder_width": 0.42}
        model_url = f"s3://digital-human/avatars/{avatar_id}/model.glb"

        await _update_avatar_status(
            avatar_id, "completed",
            smplx_params=smplx_params,
            model_url=model_url,
        )

    try:
        loop.run_until_complete(run())
    except Exception as exc:
        loop.run_until_complete(_update_avatar_status(avatar_id, "failed"))
        raise self.retry(exc=exc)
    finally:
        loop.close()


@shared_task(bind=True, max_retries=2, default_retry_delay=10)
def run_tryon(self, task_id: int, avatar_model_url: str, garment_url: str):
    """
    Celery task: call FASHN VTON service for virtual try-on.
    In dev mode without GPU, simulates processing with delays.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def run():
        await _update_tryon_status(task_id, "processing")

        # TODO: call FASHN VTON API — POST /tryon {person_image_url, garment_image_url}
        # Then: UV texture mapping back to 3D model
        await asyncio.sleep(8)

        result_url = f"s3://digital-human/tryon/{task_id}/result.png"

        await _update_tryon_status(task_id, "completed", result_url=result_url)

    try:
        loop.run_until_complete(run())
    except Exception as exc:
        loop.run_until_complete(_update_tryon_status(task_id, "failed"))
        raise self.retry(exc=exc)
    finally:
        loop.close()
