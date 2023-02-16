from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated="auto")


class Hash():
    def get_hashed_password(plain_password):
        return pwd_ctx.hash(plain_password)

    def verify_hashed_password(plain_password, hashed_password):
        return pwd_ctx.verify(plain_password, hashed_password)