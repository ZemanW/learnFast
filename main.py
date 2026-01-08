from fastapi import FastAPI, status , HTTPException , Response
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class post(BaseModel):
    title:str
    content:str
    published: bool = True
my_post = [
    {"title":"title1","content":"content 1","id" :1},
    {"title":"title2","content":"content 2","id" :2},]
def find_index(id):
    for i , p in enumerate(my_post):
        if id == p['id']:
            return i
def find_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return p

@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post : post):
    if post:
      post_dict = post.model_dump()
      post_dict["id"] = randrange(0,100000)
      my_post.append(post_dict)
      return {"new_post":post_dict}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
@app.get("/post/{id}")
def get_one(id : int):
    post = find_post(id)
    if post:
       return {"post":post}
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no post with {id}")

@app.delete("/post/{id}")
def delete_post(id : int):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No post with Id:{id}")

    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    
@app.put("/post/{id}")
def update_post(id:int , post : post):
     index = find_index(id)
     if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No post with Id:{id}")
     post_dict = post.model_dump()
     post_dict["id"] = id
     my_post[index] = post_dict
     return {"data":my_post[index]}
