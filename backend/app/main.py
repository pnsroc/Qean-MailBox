from fastapi import FastAPI
from .database import Base, engine
from .routers import auth, mail

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Qean-MailBox")

app.include_router(auth.router)
app.include_router(mail.router)
