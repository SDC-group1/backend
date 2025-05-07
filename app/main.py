from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import Blog, BlogCreate 
from typing import List
from fastapi import HTTPException

app = FastAPI()

fake_blogs_db = [
        {"id": 0, "name": "Understanding FastAPI"},
        {"id": 1, "name": "Deploying Python Apps with Docker"},
        {"id": 2, "name": "Async IO in Python: A Practical Guide"}
    ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Blog API"}

@app.get("/blogs/", response_model=List[Blog])
def read_blogs():
   return fake_blogs_db

@app.get("/blogs/{blog_id}", response_model= Blog)
def read_blog(blog_id: int):
    if blog_id < len(fake_blogs_db):
        return {"id": blog_id, "name": fake_blogs_db[blog_id]["name"]}
    raise HTTPException(status_code=404, detail="Blog not found")

@app.post("/blogs/", response_model=Blog)
def create_item(blog: BlogCreate):
    blog_dictionary = blog.dict()
    blog_dictionary["id"] = len(fake_blogs_db)
    fake_blogs_db.append(blog_dictionary)
    return blog_dictionary 