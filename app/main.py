from typing import Optional
from fastapi import FastAPI, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str 
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', 
                                database='fastapi', 
                                user='postgres', 
                                password='0000',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('DB connection successeful')
        break
    except psycopg2.OperationalError as error:
        print('Connecting failed')
        print(f'error {error}')
        print(error)
        time.sleep(2)

@app.get('/posts',status_code=status.HTTP_201_CREATED)
def get_posts():
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) """, 
                    (post.title, post.content, post.published))
    return {"data" : "created post"}




my_posts = [{"title" : "title of post", "content" : "content of post", "id" : 1},
{"title" : "title of post", "content" : "content of post", "id" : 2}]
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
            
@app.get("/") 
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def root():
    return {"data": my_posts}


@app.post("/createposts")
def create_posts(post : Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(1, 100000000)
    my_posts.append(post_dict)
    return(my_posts)

"""
@app.get("/posts/{id}")
def get_posts(id):
    dict_df = pd.DataFrame(my_posts)
    print(dict_df.columns)
    post_by_id = dict_df[dict_df['id'] == int(id)]
    output = dict()
    output["title"] = str(post_by_id["title"])
    output["content"] = str(post_by_id["content"])
    return output
"""

@app.get("/posts/{id}")
def get_posts(id):
    print(type(id))
    post = find_post(int(id))
    return {"post_detail" : post}