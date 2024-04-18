#!/usr/bin/env python3
"""
you have 2 authentication systems:
"""
import os
from datetime import (
    datetime,
    timedelta
)

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    you have 2 authentication systems:
    """
    def __init__(self):
        """
        Initialize the class
        """
        try:
            time = int(os.getenv('SESSION_DURATION'))
        except Exception:
            time = 0
        self.session_time = time

    def create_session(self, user_id=None):
        """
    you have 2 authentication systems:
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
    you have 2 authentication systems:
        """
        if session_id is None:
            return None
        user_details = self.user_id_by_session_id.get(session_id)
        if user_details is None:
            return None
        if "created_at" not in user_details.keys():
            return None
        if self.session_time <= 0:
            return user_details.get("user_id")
        created_at = user_details.get("created_at")
        allowed_window = created_at + timedelta(seconds=self.session_time)
        if allowed_window < datetime.now():
            return None
        return user_details.get("user_id")