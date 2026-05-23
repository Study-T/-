import asyncio
import time

from celery import shared_task


def _sync_update(update_type: str, obj_id: int, status: str, **kwargs):
    """Synchronous fallback: uses pymysql directly, no event loop needed."""
    import pymysql
    from app.core.config import settings

    table = "avatars" if update_type == "avatar" else "tryon_tasks"
    conn = pymysql.connect(
        host=settings.db_host, port=settings.db_port,
        user=settings.db_user, password=settings.db_password,
        database=settings.db_name, charset="utf8mb4",
    )
    try:
        with conn.cursor() as cur:
            if kwargs:
                import json
                if "smplx_params" in kwargs:
                    kwargs["smplx_params"] = json.dumps(kwargs["smplx_params"])
                set_clause = ", ".join(f"{k}=%s" for k in kwargs)
                cur.execute(
                    f"UPDATE {table} SET status=%s, {set_clause} WHERE id=%s",
                    (status, *kwargs.values(), obj_id),
                )
            else:
                cur.execute(f"UPDATE {table} SET status=%s WHERE id=%s", (status, obj_id))
        conn.commit()
    finally:
        conn.close()


# ---- Async versions (for Celery / Redis mode) ----

async def _async_update_avatar(avatar_id: int, status: str, **kwargs):
    from app.core.database import async_session
    from app.models.avatar import Avatar
    from sqlalchemy import select

    async with async_session() as db:
        result = await db.execute(select(Avatar).where(Avatar.id == avatar_id))
        avatar = result.scalar_one_or_none()
        if avatar:
            avatar.status = status
            for k, v in kwargs.items():
                setattr(avatar, k, v)
            await db.commit()


async def _async_update_tryon(task_id: int, status: str, **kwargs):
    from app.core.database import async_session
    from app.models.tryon import TryOnTask
    from sqlalchemy import select

    async with async_session() as db:
        result = await db.execute(select(TryOnTask).where(TryOnTask.id == task_id))
        task = result.scalar_one_or_none()
        if task:
            task.status = status
            for k, v in kwargs.items():
                setattr(task, k, v)
            await db.commit()


async def run_avatar_generation(avatar_id: int, photo_url: str):
    _sync_update("avatar", avatar_id, "processing")
    time.sleep(5)  # simulate GPU
    _sync_update("avatar", avatar_id, "completed",
                 smplx_params={"height": 1.70, "weight": 65, "shoulder_width": 0.42},
                 model_url=f"s3://digital-human/avatars/{avatar_id}/model.glb")


async def run_tryon_task(task_id: int, avatar_model_url: str, garment_url: str):
    _sync_update("tryon", task_id, "processing")
    time.sleep(8)  # simulate GPU
    _sync_update("tryon", task_id, "completed",
                 result_url=f"s3://digital-human/tryon/{task_id}/result.png")


# ---- Celery task wrappers (requires Redis) ----

@shared_task(bind=True, max_retries=2, default_retry_delay=10)
def generate_avatar(self, avatar_id: int, photo_url: str):
    asyncio.run(run_avatar_generation(avatar_id, photo_url))


@shared_task(bind=True, max_retries=2, default_retry_delay=10)
def run_tryon(self, task_id: int, avatar_model_url: str, garment_url: str):
    asyncio.run(run_tryon_task(task_id, avatar_model_url, garment_url))
