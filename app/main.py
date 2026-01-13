from fastapi import FastAPI, APIRouter
from .database import engine
from . import models
from .routers import post,user,auth
app = FastAPI()

models.Base.metadata.create_all(bind=engine)  # type: ignore

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
@app.get("/")
def root():
    return {"message":"root"}




