from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from .config import sttngs
from datetime import datetime, timedelta
from . import schms, dtbs, mdls

scheme_oauth2 = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#Algorithm
#Expiration time

SECRET_KEY = sttngs.secret_key
ALGORITHM = sttngs.algorithm
MINS_EXPIRE = sttngs.MINS_EXPIRE

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