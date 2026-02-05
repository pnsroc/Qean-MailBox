from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.auth_service import AuthService
from ..services.mail_service import MailService
from .. import schemas

router = APIRouter(prefix="/mail", tags=["mail"])

@router.post("/test-connection")
def test_connection(data: schemas.TestConnection):
    try:
        MailService.test_connection(data)
    except Exception as e:
        raise HTTPException(400, str(e))
    return {"status": "ok"}

@router.post("/add-manual")
def add_manual(
    data: schemas.ManualAccountCreate,
    user=Depends(AuthService.get_current_user),
    db: Session = Depends(get_db),
):
    acc = MailService.add_manual_account(user.id, data, db)
    return {"id": acc.id, "email": acc.email}

@router.get("/unified/inbox")
def unified_inbox(
    user=Depends(AuthService.get_current_user),
    db: Session = Depends(get_db),
):
    return MailService.unified_inbox(user.id, db)

@router.get("/unified/search")
def unified_search(
    q: str,
    user=Depends(AuthService.get_current_user),
    db: Session = Depends(get_db),
):
    return MailService.unified_search(user.id, q, db)

@router.get("/unified/from")
def unified_from(
    q: str,
    user=Depends(AuthService.get_current_user),
    db: Session = Depends(get_db),
):
    return MailService.unified_from_filter(user.id, q, db)

# 其他统一过滤接口（subject/date/size/...）可按同样模式继续加
