#!/usr/bin/env python3
"""Authentication module.
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Authentication class.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False - path and excluded_paths
        """
        if not path:
            return True

        if not excluded_paths:
            return True

        path = path.rstrip("/")
        for ex_path in excluded_paths:
            if ex_path.endswith("*") and \
                    path.startswith(ex_path[:-1]):
                return False
            elif path == ex_path.rstrip("/"):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ returns None - request will be the Flask request object
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """  returns None - request will be the Flask request
        """
        return None

    def session_cookie(self, request=None):
        """
        returns a cookie value from a request:
        """
        if request is None:
            return None
        The_session = os.getenv('SESSION_NAME')
        return request.cookies.get(The_session)
