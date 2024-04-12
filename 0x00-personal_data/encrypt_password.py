#!/usr/bin/env python3
"""
package to perform the hashing
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """  function that expects one string argument name password """
    encode = password.encode()
    hashed = bcrypt.hashpw(encode, bcrypt.gensalt())

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """  expects 2 arguments and returns a boolean """
    boolian = False
    encode = password.encode()
    if bcrypt.checkpw(encode, hashed_password):
        boolian = True
    return boolian
