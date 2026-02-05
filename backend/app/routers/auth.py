from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserLogin
from ..security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


# -----------------------------
# 检查是否需要初始化管理员
# -----------------------------
@router.get("/need-init")
def need_init(db: Session = Depends(get_db)):
    admin = db.query(User).first()
    return {"need_init": admin is None}


# -----------------------------
# 初始化管理员（仅第一次）
# -----------------------------
@router.post("/init-admin")
def init_admin(data: UserCreate, db: Session = Depends(get_db)):
    admin = db.query(User).first()
    if admin:
        raise HTTPException(status_code=403, detail="Admin already initialized")

    new_admin = User(
        email=data.email,
        password_hash=hash_password(data.password)
    )
    db.add(new_admin)
    db.commit()
    return {"message": "Admin initialized"}


# -----------------------------
# 登录
# -----------------------------
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token}
