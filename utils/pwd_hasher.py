#!/usr/bin/env python3
import bcrypt


salt = bcrypt.gensalt()

class PwdHasher:
    @staticmethod
    def pwd_hash(password: str) -> bytes:
        encode = password.encode('utf-8')
        return bcrypt.hashpw(encode, salt)

    @staticmethod
    def pwd_check(password: str, hashed_pwd: str) -> bool:
        password_bytes = password.encode()
        if bcrypt.checkpw(password_bytes, hashed_pwd.encode()):
            return True
        return False
