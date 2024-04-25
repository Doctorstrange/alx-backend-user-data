#!/usr/bin/env python3
"""DB module
"""
import logging
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User

logging.disable(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """two required string arguments:
        email and hashed_password, and returns a User object

        Returns: a User object. The method should save the user to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            print(f"Error couldn't add user to database: {e}")
            self._session.rollback()
            raise
        return new_user

    def find_user_by(self, **kwargs: Dict[str, str]) -> User:
        """takes in arbitrary keyword arguments and returns the first
        row found in the users table as filtered by the method’s
        input arguments

         Raises:
            error: NoResultFound: When no results are found.
            error: InvalidRequestError: When invalid query arguments are passed

        Returns:
            NoResultFound and InvalidRequestError
            are raised when no results are found
        """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """takes as argument a required user_id integer and
        arbitrary keyword arguments, and returns None.
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError("User with id {} not found".format(user_id))

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError("User has no attribute {}".format(key))
            setattr(user, key, value)

        try:
            self._session.commit()
        except InvalidRequestError:
            raise ValueError("Invalid request")
