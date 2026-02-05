from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel): 
    email: str 
    password: str 
    
class UserLogin(BaseModel): 
    email: str 
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class ManualAccountCreate(BaseModel):
    email: EmailStr
    password: str
    imap_host: str
    imap_port: int
    imap_ssl: bool
    smtp_host: str
    smtp_port: int
    smtp_ssl: bool


class TestConnection(BaseModel):
    email: EmailStr
    password: str
    imap_host: str
    imap_port: int
    imap_ssl: bool
    smtp_host: str
    smtp_port: int
    smtp_ssl: bool
