from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status

from app.core.auth import current_user
from app.core.storage import upload_file
from app.schemas.common import UploadResponse

router = APIRouter(prefix="/api/upload", tags=["upload"])
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE = 10 * 1024 * 1024


@router.post("", response_model=UploadResponse)
async def upload(
    file: UploadFile = File(...),
    user_id: int = Depends(current_user),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="仅支持 JPEG/PNG/WebP")
    data = await file.read()
    if len(data) > MAX_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="文件最大 10MB")
    url = upload_file(data, file.content_type or "image/jpeg", prefix=f"users/{user_id}")
    return UploadResponse(url=url)
