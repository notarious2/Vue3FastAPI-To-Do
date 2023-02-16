from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Depends
import jwt
from fastapi.security import OAuth2PasswordBearer
from config import settings
import crud
from database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/jwt/create/", scheme_name="JWT") #important path to get token


def decode_access_token(db, token):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
  except jwt.ExpiredSignatureError:
      raise HTTPException(status_code=401, detail='Token expired')
  except jwt.InvalidTokenError:
      raise HTTPException(status_code=401, detail='Invalid Access Token')
  except jwt.PyJWTError:
    raise credentials_exception
  
  user = crud.get_user_by_username(db, username=username)
  if user is None:
    raise credentials_exception
  return user

def get_current_user(db: Session = Depends(get_db),
                	token: str = Depends(oauth2_scheme)):
   return decode_access_token(db, token)