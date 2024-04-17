#!/usr/bin/env python3
"""Authentication module.
"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """Authentication class.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False - path and excluded_paths
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        for ex_path in excluded_paths:
            if fnmatch.fnmatch(path, ex_path):
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
