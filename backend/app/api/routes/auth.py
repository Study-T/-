from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import create_token
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import SendCodeRequest, LoginRequest, LoginResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])

VERIFICATION_CODES: dict[str, str] = {}


@router.post("/send-code")
async def send_code(req: SendCodeRequest):
    code = "123456"
    VERIFICATION_CODES[req.phone] = code
    return {"message": "验证码已发送"}


@router.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    expected = VERIFICATION_CODES.get(req.phone)
    if not expected or req.code != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="验证码错误")

    result = await db.execute(select(User).where(User.phone == req.phone))
    user = result.scalar_one_or_none()

    if not user:
        user = User(phone=req.phone)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    token = create_token(user.id)
    del VERIFICATION_CODES[req.phone]

    return LoginResponse(token=token, user_id=user.id)
