from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "Hello World", "content": "First post content", 'id': 1}, {"title": "Goodbye World", "content": "Second post content", 'id': 2}, {"title": "Hello Mars", "content": "Third post content", 'id': 3}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None

@app.get("/")
async def root():
    return {"data": 'Welcome to my api!!'}

@app.get("/posts")
def get_post():
    return {"data": my_posts}

@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(1, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get('/post/{id}')
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"data": post}

@app.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/post/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post, response: Response):
    post_dict = post.dict()
    post_dict['id'] = id
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    my_posts.remove(post)
    my_posts.append(post_dict)
    return {"message": post_dict}

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=57889, reload=True)