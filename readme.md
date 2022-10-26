<h1 align="center">
  <br>
 API development using <br>
 :fire: FastAPI :fire: <br> :fire: SQLAlchemy :fire: <br> :fire: Postgres :fire: <br>
  :computer: Social network with authentication and votes. :computer:<br>
:hammer_and_wrench: Deployment on Heroku + Docker. :hammer_and_wrench: <br>
</h1>


<h3 align="center">
  Built with
  <br>
    <img src="https://raw.githubusercontent.com/boramorka/usercontent/aad4d15178483720bcc0562617c86a7c84a7d257/shields.io/python.svg" height="30">
    <img src="https://raw.githubusercontent.com/boramorka/usercontent/aad4d15178483720bcc0562617c86a7c84a7d257/shields.io/heroku.svg" height="30">
    <img src="https://raw.githubusercontent.com/boramorka/usercontent/4747733b63d843a80f861cc51bf58fcf8586dd82/shields.io/postgres.svg" height="30">
    <img src="https://raw.githubusercontent.com/boramorka/usercontent/4747733b63d843a80f861cc51bf58fcf8586dd82/shields.io/fastapi.svg" height="30">
    <img src="https://raw.githubusercontent.com/boramorka/usercontent/4747733b63d843a80f861cc51bf58fcf8586dd82/shields.io/docker.svg" height="30">
    <img src="https://github.com/boramorka/usercontent/blob/main/API_dev/pydantic.png?raw=true" height="30">
    <img src="https://github.com/boramorka/usercontent/blob/main/API_dev/sqlalchemy.png?raw=true" height="30">

<p align="center">
  • <a href="#how-to-use">How To Use</a> • <br>
  • <a href="#built-process">Built process</a> • :arrow_right: • <a href="#main-script">Main script</a> • <a href="#post-route">Post route</a> • <a href="#user-route">User route</a> • <a href="#vote-route">Vote route</a> • <a href="#auth-module">Authorization module</a> • <a href="#jwt-tokenization-using-oauth2">JWT Tokenization using Oauth2</a> • <a href="#hashing-passwords">Hashing passwords</a> •
  <a href="#database-connection">Database connection</a> •
  <a href="#sqlalchemy-model">SQLAlchemy Model</a> •
  <a href="#pydantic-response-scheme">Pydantic response scheme</a> •
  <a href="#alembic-migrations">Alembic migrations</a> •
  <a href="#heroku-deployment">Heroku deployment</a> •
  <a href="#heroku-procfile-configuration">Heroku Procfile configuration</a> •
  <a href="#dockerfile">Dockerfile</a> •
  <a href="#docker-compose">Docker-compose</a> •
  <a href="#docker-build">Docker build</a> • <br>
  :person_in_tuxedo: • <a href="#feedback">Feedback</a> • :person_in_tuxedo:
</p>

## How to use
### Deployment
:hammer_and_wrench: This app deployed to heroku. So you can:
- Test it as a heroku app: Go to https://fastapi-boramorka.herokuapp.com/docs


- Build it locally using docker:
  
  ``` bash
  # Pull these images to docker
  $ docker pull boramorka/fastapi
  $ docker pull postgres

  # Clone this repository
  $ git clone https://github.com/boramorka/API_dev.git

  # Go to app dir
  $ cd API_dev

  # Run docker-compose to start an app
  $ docker-compose up -d
  """ 
  Then go to localhost:8000/docs
  """
  # Type this to stop
  $ docker-compose down
  ```

### Usage 
:green_circle: API has authorize block in the upper-right corner, posts block, users block, auth block and likes (votes) block:

![Blocks](https://github.com/boramorka/usercontent/blob/main/API_dev/show_start.png?raw=true)

:green_circle: First, go to Create User section and fill the json form:

![Blocks](https://github.com/boramorka/usercontent/blob/main/API_dev/create_user.png?raw=true)

:green_circle: Then use authorize button:

![Blocks](https://github.com/boramorka/usercontent/blob/main/API_dev/auth1.png?raw=true)

:green_circle: And fill the credentials:

![Blocks](https://github.com/boramorka/usercontent/blob/main/API_dev/auth2.png?raw=true)

:green_circle: Now you can use a get block to get all posts and use a filter.

![Blocks](https://github.com/boramorka/usercontent/blob/main/API_dev/get_posts.png?raw=true)

:green_circle: Or search specific post by id.

![Blocks](https://github.com/boramorka/usercontent/blob/main/API_dev/get_posts_id.png?raw=true)

:green_circle: Create post.

![Blocks](https://github.com/boramorka/usercontent/blob/main/API_dev/create_post.png?raw=true)

:yellow_circle: Update post.

![Blocks](https://github.com/boramorka/usercontent/blob/main/API_dev/upd_post.png?raw=true)

:red_circle: Delete post.

![Blocks](https://github.com/boramorka/usercontent/blob/main/API_dev/del_post.png?raw=true)

:purple_circle: You can like someone's post by ID. Dir means direction (Like and unlike)

![Blocks](https://github.com/boramorka/usercontent/blob/main/API_dev/like.png?raw=true)

## Built process

## Main script

  ```python
  """
  Main.py block
  This code connecnts main app to routers. Each router has it's own role.
  """

from fastapi import FastAPI

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
  ```

  ```python
  """
  CORS BLOCK

  Cross-Origin Resource Sharing (CORS) is an HTTP-header based mechanism that allows a server to indicate any origins (domain, scheme, or port) other than its own from which a browser should permit loading resources. CORS also relies on a mechanism by which browsers make a "preflight" request to the server hosting the cross-origin resource, in order to check that the server will permit the actual request. In that preflight, the browser sends headers that indicate the HTTP method and headers that will be used in the actual request.
  """
  from fastapi.middleware.cors import CORSMiddleware

  origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )
  ```

## Post route

This route can provide you access to all posts by id. Also this block includes logic for creating, updating and deleting posts.

  ```python
  """
  Get all posts
  """
@router.get("/", response_model=List[schms.PostOut])
def get_posts(db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user),
                limit : int = 10, 
                skip: int = 0,
                search : Optional[str] = ""):

    posts = db.query(mdls.Post, func.count(mdls.Vote.post_id).label("votes")).\
      join(mdls.Vote, mdls.Vote.post_id == mdls.Post.id, isouter=True).\
        group_by(mdls.Post.id).\
          filter(mdls.Post.title.contains(search)).\
            limit(limit).\
              offset(skip).\
                all()

    return posts
  ```

  ```python
  """
  Get one post by id 
  """
  @router.get("/{id}", response_model=schms.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(mdls.Post, func.count(mdls.Vote.post_id).label("votes")).\
      join(mdls.Vote, mdls.Vote.post_id == mdls.Post.id, isouter=True).\
        group_by(mdls.Post.id).\
          filter(mdls.Post.id == id).\
            first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
    return post
  ```

  ```python
  """
  Create post
  """
  @router.post('/',status_code=status.HTTP_201_CREATED, response_model=schms.Post)
def create_posts(post : schms.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    new_post = mdls.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

  ```

  ```python
  """
  Update post
  """
  @router.put("/{id}", response_model=schms.Post)
def update_post(id: int, updated_post: schms.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(mdls.Post).filter(mdls.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()  
  ```


  ```python
  """
  Delete post
  """
  @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):     

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
  ```

## User route

  ```python
  """
  Create user
  """
  @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schms.UserOut)
def create_user(user: schms.UserCreate, db: Session = Depends(get_db)):

    #hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = mdls.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
  ```


  ```python
  """
  Get user by id
  """
  @router.get("/{id}", response_model=schms.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(mdls.User).filter(mdls.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {id} not found")
    
    return user
  ```

## Vote route

  ```python
  """
  Vote (like or unlike post)
  """
  @router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schms.Vote, 
           db: Session = Depends(dtbs.get_db), 
           current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(mdls.Post).filter(mdls.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {vote.post_id} does not exist.")

    vote_query = db.query(mdls.Vote).\
      filter(mdls.Vote.post_id == vote.post_id, mdls.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"User {current_user.id} has already voted.")

        new_vote = mdls.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message" : "successuefuly added vote"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Vote does not exist.")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message" : "successuefuly deleted vote"}
  ```

## Authorization module


  ```python
  """
  Autorization block
  """
  @router.post("/login", response_model=schms.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), 
            db: Session = Depends(dtbs.get_db)):

    user = db.query(mdls.User).\
      filter(mdls.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid credentials")

    #create a token
    #return token

    access_token = oauth2.create_access_token(data = {"user_id" : user.id})
    return {"access_token": access_token, "token_type" : "bearer"}
  ```

## JWT Tokenization using Oauth2
Auth block is connected to oauth2 module that contains 3 important logical parts:
- It creates JWT token for each new user
- It checks credentials of autheficationing user
- It verifyng JWT token of autheficationing user

```python
"""
oauth2 block
"""
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=MINS_EXPIRE)
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt 

def verify_access_token(token: str, credentials_exception):
    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schms.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data

  def get_current_user(token: str = Depends(scheme_oauth2), db: Session = Depends(dtbs.get_db)):
      credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
      detail=f'Could not validate credentials', headers={"WWW_Authenticate" : "Bearer"})

      token = verify_access_token(token, credentials_exception)
      user = db.query(mdls.User).filter(mdls.User.id == token.id).first()
      return user
  ```


## Hashing passwords
  ```python
  """
  Hashing in verifying hashes
  """
  from passlib.context import CryptContext
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

  def hash(password: str):
      return pwd_context.hash(password)

  def verify(plain_password, hashed_password):
      return pwd_context.verify(plain_password, hashed_password)

  ```

## Database connection

  ```python
  """
  DB connecton
  """
  from sqlalchemy import create_engine
  from sqlalchemy.ext.declarative import declarative_base
  from sqlalchemy.orm import sessionmaker
  from .config import sttngs

  SQLALCHEMY_DATABASE_URL = f'postgresql://{sttngs.DB_USERNAME}:{sttngs.DB_PASSWORD}@{sttngs.DB_HOSTNAME}:{sttngs.DB_PORT}/{sttngs.DB_NAME}'

  engine = create_engine(SQLALCHEMY_DATABASE_URL)

  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

  Base = declarative_base()

  # Dependency
  def get_db():
      db = SessionLocal()
      try:
          yield db
      finally:
          db.close()
  ```

## SQLAlchemy Model
  ```python
  """
  SQLAlchemy
  Declaring a tables using SQLAlchemy API
  """
  from .dtbs import Base
  from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
  from sqlalchemy.orm import relationship
  from sqlalchemy.sql.sqltypes import TIMESTAMP
  from sqlalchemy.sql.expression import text

  #DECLARING POSTS TABLE
  class Post(Base):
      __tablename__ = "posts"

      id = Column(Integer, primary_key = True, nullable=False)
      title = Column(String, nullable=False)
      content = Column(String, nullable=False)
      published = Column(Boolean, server_default="TRUE", nullable=False)
      created_at = Column(TIMESTAMP(timezone=True), nullable = False, 
                                      server_default=text('now()'))
      owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
      owner = relationship("User")
  
  #DECLARING USERS TABLE
  class User(Base):
      __tablename__ = "users"
      id = Column(Integer, primary_key = True, nullable=False)
      email = Column(String, nullable=False, unique=True)
      password = Column(String, nullable=False)
      created_at = Column(TIMESTAMP(timezone=True), nullable = False, 
                                      server_default=text('now()'))

  #DECLARING VOTES TABLE
  class Vote(Base):
      __tablename__ = 'votes'
      user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key = True)
      post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key = True)
  ```

## Pydantic response scheme
  ```python
  """
  Pydantic scheme for FastAPI responses serialization.
  """
  from pydantic import BaseModel, EmailStr
  from datetime import datetime
  from typing import Optional
  from pydantic.types import conint

  class PostBase(BaseModel):
      title : str
      content : str 
      published: bool = True

  class PostCreate(PostBase):
      pass

  class UserOut(BaseModel):
      id: int
      email: EmailStr
      created_at: datetime

      class Config:
          orm_mode = True

  class Post(PostBase):
      id: int
      created_at: datetime
      owner_id: int
      owner: UserOut

      class Config:
          orm_mode = True

  class PostOut(BaseModel):
      Post: Post
      votes: int

      class Config:
          orm_mode = True

  class UserCreate(BaseModel):
      email: EmailStr
      password: str

  class UserLogin(BaseModel):
      email: EmailStr
      password: str

  class Token(BaseModel):
      access_token: str
      token_type: str

  class TokenData(BaseModel):
      id: Optional[str] = None

  class Vote(BaseModel):
      post_id: int
      dir: conint(le=1)
  ```

## Alembic migrations

  ```python
  """
  Alembic autogenerating block for DB migration.
  """
  from alembic import op
  import sqlalchemy as sa


  # revision identifiers, used by Alembic.
  revision = '90ac1c319bb6'
  down_revision = None
  branch_labels = None
  depends_on = None


  def upgrade() -> None:
      # ### commands auto generated by Alembic - please adjust! ###
      op.create_table('users',
      sa.Column('id', sa.Integer(), nullable=False),
      sa.Column('email', sa.String(), nullable=False),
      sa.Column('password', sa.String(), nullable=False),
      sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
      sa.PrimaryKeyConstraint('id'),
      sa.UniqueConstraint('email')
      )
      op.create_table('posts',
      sa.Column('id', sa.Integer(), nullable=False),
      sa.Column('title', sa.String(), nullable=False),
      sa.Column('content', sa.String(), nullable=False),
      sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False),
      sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
      sa.Column('owner_id', sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
      sa.PrimaryKeyConstraint('id')
      )
      op.create_table('votes',
      sa.Column('user_id', sa.Integer(), nullable=False),
      sa.Column('post_id', sa.Integer(), nullable=False),
      sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
      sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
      sa.PrimaryKeyConstraint('user_id', 'post_id')
      )
      # ### end Alembic commands ###


  def downgrade() -> None:
      # ### commands auto generated by Alembic - please adjust! ###
      op.drop_table('votes')
      op.drop_table('posts')
      op.drop_table('users')
      # ### end Alembic commands ###

  ```

## Heroku deployment

  ```bash
  # HEROKU DEPLOYMENT PROCESS

# Login to Heroku, and create a new app:
  $ heroku login
  $ git init
  $ heroku create fastapi-boramorka
  $ heroku git:remote -a fastapi-boramorka

  # Add Config Vars:
  # Here you need to set env variables inside heroku or using bash (cmd)
  $ heroku config:set ENV_VAR=VALUE

  # Deploy app on Heroku:
  $ git add .
  $ git commit -m "Initial commit to Heroku"
  $ heroku git:remote -a fastapi-boramorka
  $ git push heroku master

  # Init Posgres to Heroku
  $ heroku addons:create heroku-postgresql:hobby-dev

  # Run worker
  $ heroku ps:scale web=1

  #Run migrations
  $ heroku run bash --app fastapi-boramorka alembic revision --autogenerate -m "Add all tables"
  ```

## Heroku Procfile configuration

  ```bash
  web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}
  ```

## Dockerfile

  ```python
  FROM python:3.9.13

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```

## Docker-compose

  ```python
  version: "3"
services:
  api:
    build: .
    ports:
      - 8000:8000
    volumes:
      - ./:/usr/src/app
    # env_file:
    #     - ./.env
    environment:
      - DB_HOSTNAME=postgres
      - DB_PORT=5432
      - DB_PASSWORD=0000
      - DB_NAME=fastapi
      - DB_USERNAME=postgres
      - SECRET_KEY=gh8762wygb8&Yh8b7^GT46ER7Yg75bh8i765r^U^UY&
      - ALGORITHM=HS256
      - MINS_EXPIRE=30
      
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    depends_on:
      - postgres

  postgres:
    image: postgres
    environment:
      - POSTGRES_PASSWORD=0000
      - POSTGRES_DB=fastapi
    volumes:
      - postgres-db:/var/lib/postgresql/data
    #command: bash -c "pwd"

volumes:
    postgres-db:
  ```
## Docker build
  ```bash
  $ docker build -t fastapi .
  ```

## Feedback
:person_in_tuxedo: Feel free to send me feedback on [Telegram](https://t.me/boramorka). Feature requests are always welcome. 

:abacus: [Check my other projects.](https://github.com/boramorka)




