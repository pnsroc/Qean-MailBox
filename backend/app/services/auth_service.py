from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from ..database import get_db
from ..models import User
from ..security import verify_password, create_access_token
from ..config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class AuthService:
    @staticmethod
    def authenticate(email: str, password: str, db: Session):
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        token = create_access_token({"sub": str(user.id)})
        return token

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = int(payload.get("sub"))
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user = db.query(User).get(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
