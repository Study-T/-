import enum
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Enum, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AvatarStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class Avatar(Base):
    __tablename__ = "avatars"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    photo_url: Mapped[str] = mapped_column(String(500))
    smplx_params: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    model_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[AvatarStatus] = mapped_column(
        Enum(AvatarStatus), default=AvatarStatus.pending
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
