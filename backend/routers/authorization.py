from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from models import User
from database import get_async_session
import crud
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from utils import verify_hashed_password
from fastapi.encoders import jsonable_encoder
import datetime
from config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from auth import create_access_token, create_refresh_token



router = APIRouter(
    prefix = '/user',
    tags = ['user']
)

@router.post('/jwt/create/')
async def login(db_session: Session = Depends(get_async_session), form_data: OAuth2PasswordRequestForm = Depends()):
   """
    ## LogIn a User
    This requires the following fields:
    ```
        username: str
        password: str

    and returns a token pair 'access' and 'refresh' tokens
    ```
        
   """ 
   user = await authenticate_user(db=db_session, username=form_data.username, password=form_data.password)
   if not user:
    raise HTTPException(
       	status_code=status.HTTP_401_UNAUTHORIZED,
       	detail="Incorrect username or password",
       	headers={"WWW-Authenticate": "Bearer"},
   	)
   access_token = create_access_token(subject = user.username, expires_time=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
   refresh_token = create_refresh_token(subject = user.username)
   
    
   response = {
        "access_token": access_token, # must have as access_token to avoid errors with Swagger
        "refresh_token": refresh_token,
        "token_type": 'Bearer' # need this to avoid errors with Swagger
    }
   
   return jsonable_encoder(response) 

# @router.get('/jwt/refresh/')
# def refresh(Authorize: AuthJWT = Depends()):
#     """refresh token is not verified when creating access token"""
#     try:        
#         Authorize.jwt_refresh_token_required()
#         current_user = Authorize.get_jwt_subject()
#         new_access_token = Authorize.create_access_token(subject=current_user, expires_time=expires)
#     except:
#         raise HTTPException(
#        	status_code=status.HTTP_401_UNAUTHORIZED,
#        	detail="Invalid Refresh Token")

#     return {"access_token": new_access_token}


#Authenticate user based on username/email and password
async def authenticate_user(username: str, password: str, db_session: AsyncSession):
    # find user with such username
    user: User | None = await crud.get_user_by_username_or_email(db_session, username)
    if not user:
        return False
    # check if passwords match - use hashed_password to check
    if not verify_hashed_password(plain_password=password, hashed_password=user.password):
        return False
    return user        
