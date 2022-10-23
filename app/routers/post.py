from app import oauth2
from .. import mdls, schms
from ..dtbs import  get_db
from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

#@router.get("/", response_model=List[schms.Post])
@router.get("/", response_model=List[schms.PostOut])
def get_posts(db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user),
                limit : int = 10, 
                skip: int = 0,
                search : Optional[str] = ""):
    #print(current_user.email)
    #Pydentic
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
    #Using SQLAlchemy
    #posts = db.query(mdls.Post).filter(mdls.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(mdls.Post, func.count(mdls.Vote.post_id).label("votes")).join(mdls.Vote, mdls.Vote.post_id == mdls.Post.id, isouter=True).group_by(mdls.Post.id).filter(mdls.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.post('/',status_code=status.HTTP_201_CREATED, response_model=schms.Post)
def create_posts(post : schms.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    #Pydentic
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    #Using SQLAlchemy
    #new_post = mdls.Post(title=post.title, content=post.content, published=post.published)
    #or
    print(current_user.email)
    new_post = mdls.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.get("/{id}", response_model=schms.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    #Pydentic
#     cursor.execute("""
#                     SELECT * FROM posts WHERE id = %s
#                     """, (str(id), ))
#     post = cursor.fetchone()

    #Using SQLAlchemy 
    
    #post = db.query(mdls.Post).filter(mdls.Post.id == id).first()

    post = db.query(mdls.Post, func.count(mdls.Vote.post_id).label("votes")).join(mdls.Vote, mdls.Vote.post_id == mdls.Post.id, isouter=True).group_by(mdls.Post.id).filter(mdls.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    #Pydentic
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit() 

    # if deleted_post == None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
    #                         detail = f"post with id: {id} does not exist")
    # return Response(status_code=status.HTTP_204_NO_CONTENT)       

    post_query = db.query(mdls.Post).filter(mdls.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)    

                


@router.put("/{id}", response_model=schms.Post)
def update_post(id: int, updated_post: schms.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""
    #                 UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *
    #                 """, (post.title, post.content, post.published, str(id), ))
    
    # updated_post = cursor.fetchone()
    # conn.commit() 

    # if updated_post == None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
    #                         detail = f"post with id: {id} does not exist")

    #Using SQLAlchemy
    post_query = db.query(mdls.Post).filter(mdls.Post.id == id)
    post = post_query.first()
    print('____________________')
    print(post)

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()  