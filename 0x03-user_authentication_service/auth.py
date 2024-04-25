#!/usr/bin/env python3
"""Module for authentication.
"""


import logging
from typing import Union
from uuid import uuid4

import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User

logging.disable(logging.WARNING)


def _hash_password(password: str) -> bytes:
    """ takes in a password string arguments and returns bytes
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """mandatory email and password string arguments
        and return a User object
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        hashed_password = _hash_password(password)
        user = self._db.add_user(email, hashed_password)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """ expect email and password required
        arguments and return a boolean
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                password = password.encode('utf-8')
                hashed_password = user.hashed_password
                if bcrypt.checkpw(password, hashed_password):
                    return True
        except NoResultFound:
            return False
        return False
