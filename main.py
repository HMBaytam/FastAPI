from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Welcome to my api!!"}

@app.get("/posts")
def get_post():
    return {"data": "this is your posr"}

@app.post("/post")
def create_post(post: Post):
    print(post.dict())
    return {"data": "new post"}