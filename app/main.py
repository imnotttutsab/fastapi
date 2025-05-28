from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favourite food","content":"I like pizzan" ,"id":2}]


# Pydantic model for creating the post
#ID is not here because we dont expect user to provide one
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : Optional[int] = None


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_post_index(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return{"data":my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED) 
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}


#{id} is a path parameter
@app.get("/posts/{id}")
def get_post(id: int, response:Response):
    post = find_post(id)

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
                            
    return{"post_detail": post}

#The 204 actually expects you to not return anything, just a response code
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):

    post= find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    my_posts.remove(post)
    Response(status_code=status.HTTP_204_NO_CONTENT)
    return


@app.put("/posts/{id}")
def update_post(id:int, post:Post):

    #We cant use find_post cause for update we need the index anyhow
    index= find_post_index(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")

    #We need to convert the Pydantic model to a dictionary 
    # and add the id cause if you remember the pydentic model aint got no id
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return{"data":post_dict}