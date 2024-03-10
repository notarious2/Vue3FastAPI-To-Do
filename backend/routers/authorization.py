from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth import create_access_token, create_refresh_token
from database import get_async_session
from repositories.user_repo import UserRepository

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/jwt/create/")
async def login(
    db_session: AsyncSession = Depends(get_async_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    ## LogIn a User
    This requires the following fields:
    ```
        username: str
        password: str

    and returns a token pair 'access' and 'refresh' tokens
    ```

    """
    user_repo = UserRepository(db_session)
    user = await user_repo.authenticate_user(username=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=user.username)
    refresh_token = create_refresh_token(subject=user.username)

    response = {
        "access_token": access_token,  # must have as access_token to avoid errors with Swagger
        "refresh_token": refresh_token,
        "token_type": "Bearer",  # need this to avoid errors with Swagger
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
