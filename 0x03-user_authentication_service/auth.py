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
