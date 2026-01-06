from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class post(BaseModel):
    title:str
    content:str
    published: bool = True
    rating: int = None 

@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.post("/createposts")
def create_post(new_post : post):
    print(new_post.published)
    return {"new_post":"Okay"}