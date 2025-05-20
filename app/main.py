from fastapi import FastAPI
from .database import engine
from . import models
from .routers import users, posts, comments, settings, auth
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      
    allow_credentials=True,     
    allow_methods=["*"],        
    allow_headers=["*"],        
)

app.add_middleware(SessionMiddleware, secret_key="YOUR_SECRET_KEY")

# app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
# app.include_router(comments.router, prefix="/api/comments", tags=["comments"])
# app.include_router(settings.router, prefix="/api/settings", tags=["settings"])

@app.get("/")
def read_root():
    return {"message": "Backend is running"}