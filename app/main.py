from typing import Optional
from fastapi import FastAPI, status, HTTPException, Response
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

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
            
            
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


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data" : posts}


@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_posts(post : Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data" : new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""
                    SELECT * FROM posts WHERE id = %s
                    """, (str(id), ))
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
    return {"data" : post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)                        


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""
                    UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *
                    """, (post.title, post.content, post.published, str(id), ))
    
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    
    return {"data" : updated_post}


















my_posts = [{"title" : "title of post", "content" : "content of post", "id" : 1},
{"title" : "title of post", "content" : "content of post", "id" : 2}]

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


@app.get("/posts/{id}")
def get_posts(id):
    print(type(id))
    post = find_post(int(id))
    return {"post_detail" : post}
"""