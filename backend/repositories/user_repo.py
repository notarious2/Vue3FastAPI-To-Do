import secrets
import string
from datetime import datetime, timezone

from fastapi import status
from httpx import AsyncClient, Response
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import User
from backend.schemas import UserCreate
from backend.utils import get_hashed_password, verify_hashed_password


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def authenticate_user(self, username: str, password: str):
        user: User | None = await self.get_user_by_username_or_email(username)
        if not user:
            return False
        # check if passwords match - use hashed_password to check
        if not verify_hashed_password(plain_password=password, hashed_password=user.password):
            return False
        return user

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.db_session.get(User, user_id)

    async def get_user_by_username_or_email(self, username: str) -> User:
        result = await self.db_session.execute(
            select(User).where(or_(User.username == username, User.email == username)),
        )
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User:
        result = await self.db_session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User:
        result = await self.db_session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create_user(self, user_schema: UserCreate) -> User:
        hashed_password = get_hashed_password(user_schema.password)

        user = User(
            email=user_schema.email,
            name=user_schema.name,
            username=user_schema.username,
            password=hashed_password,
        )

        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)
        return user

    async def delete_user_by_id(self, user_id: int) -> bool:
        user = await self.db_session.get(User, user_id)
        if not user:
            return False

        await self.db_session.delete(user)
        await self.db_session.commit()
        return True

    async def create_user_from_google_credentials(self, **kwargs) -> User:
        # generate random password for google user and hash it
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = "".join(secrets.choice(alphabet) for _ in range(20))
        hashed_password = get_hashed_password(password)

        user = User(
            username=kwargs.get("email"),  # Using Google email as username
            email=kwargs.get("email"),
            name=f"{kwargs.get('given_name')} {kwargs.get('family_name')}",
            password=hashed_password,
        )
        self.db_session.add(user)
        await self.db_session.commit()

        return user

    # https://stackoverflow.com/questions/16501895/how-do-i-get-user-profile-using-google-access-token
    # Verify the auth token received by client after google signin
    async def verify_google_token(self, google_access_token: str) -> dict[str, str] | None:
        google_url = f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={google_access_token}"

        async with AsyncClient() as client:
            response: Response = await client.get(google_url)
            if response.status_code == status.HTTP_200_OK:
                user_info: dict = response.json()
            else:
                return None

        # check that user_info contains email, given and family name
        if {"email", "given_name", "family_name"}.issubset(set(user_info)):
            return user_info

        return None

    async def update_user_last_login(self, user: User) -> None:
        user.last_login = datetime.now(timezone.utc)
        await self.db_session.commit()
