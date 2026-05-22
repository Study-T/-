import enum
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TryOnStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class TryOnTask(Base):
    __tablename__ = "tryon_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    avatar_id: Mapped[int] = mapped_column(ForeignKey("avatars.id"))
    garment_id: Mapped[int] = mapped_column(ForeignKey("garments.id"))
    result_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[TryOnStatus] = mapped_column(
        Enum(TryOnStatus), default=TryOnStatus.pending
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
