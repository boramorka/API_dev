from fastapi import FastAPI, Depends
from . import mdls
from .dtbs import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth, vote
from .config import sttngs
from fastapi.middleware.cors import CORSMiddleware


#mdls.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(mdls.Post).all()
    return posts 