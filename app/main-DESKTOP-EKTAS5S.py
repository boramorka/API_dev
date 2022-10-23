from typing import Optional
from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import mdls
from .dtbs import engine, get_db
from sqlalchemy.orm import Session

mdls.Base.metadata.create_all(bind=engine)

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
                                dtbs='fastapi', 
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

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(mdls.Post).all()
    return {"data" : posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    #Using straight SQL
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
    #Using straight SQLAlchemy
    posts = db.query(mdls.Post).all()

    return {"data" : posts}


@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_posts(post : Post, db: Session = Depends(get_db)):
    #Using straight SQL
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    #Using straight SQLAlchemy
    #new_post = mdls.Post(title=post.title, content=post.content, published=post.published)
    #same as
    new_post = mdls.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

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
