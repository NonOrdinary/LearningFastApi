from fastapi import FastAPI, Response , status ,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    # name : expected data type
    # if any of the attribute isn't passed and isn't expected 
    # it returns an error
    title : str
    content : str
    
    # optional attribute 
    published : bool = True  # if user doesn't provide this it would take True
    rating : Optional[int] = None  #completely optional no default value storing ,its either given or none



# data section
my_posts = [{"title" : "Killua" , "content" : "Hunter X Hunter", "id":1} ,{"title" : "Isagi" , "content" : "Blue Lock", "id":2} ] # storing posts locally untill we are ready for database but every refresh would reset so hardcoding rn
assigned_id = set()
total = 0
for entry in my_posts:
    assigned_id.add(entry["id"])
    total = total + int(entry["id"])
    

def getUniqueId():
    global total
    
    size = len(assigned_id)
    max_id = max(assigned_id)
    new_id = 0
    if max_id == size:
        total = total + max_id + 1
        new_id =  max_id + 1
    else:
        new_id = (size *(size + 1)) // 2 - total
        total = (size * (size + 1))//2
    
    assigned_id.add(new_id)
    return new_id
         
         
def find_post(id):
    if int(id) > len(my_posts):
        return None
    my_posts.sort(key=lambda x: x["id"])  # Ensure sorted by ID
    left , right = -1, len(my_posts) + 1
    while left + 1 < right :
        mid = (left + right)//2
        if my_posts[mid]["id"] == int(id):
            return my_posts[mid]
        elif my_posts[mid]["id"] < int(id):
            left = mid
        else :
            right = mid
    
    
    

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts/{id}")
def get_post_by_id(id, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'{id} not found' )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error" : f'{id} not found'}
    #id doesn't exist then we show status code and return error message
    
    return {"data" : post}




@app.get("/posts")
def get_posts():
    return {"data" : my_posts}


 
@app.post("/posts")
def create_post(post: Post):
    # print(post)
    # we can convert all this to dict by post.dict() or post.model_dump() because here post in pydantic model
    
    post_dict = post.model_dump()
    post_dict['id'] = getUniqueId()
    my_posts.append(post_dict)
    return {"data" : post_dict}
# expected data from post = title, content