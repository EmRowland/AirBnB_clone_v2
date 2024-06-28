#!/usr/bin/python3
"""Defines the DBStorage engine."""

import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from dotenv import load_dotenv

load_dotenv()


class DBStorage:
    """Represents a database storage engine."""

    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object."""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                os.getenv("HBNB_MYSQL_USER"),
                os.getenv("HBNB_MYSQL_PWD"),
                os.getenv("HBNB_MYSQL_HOST"),
                os.getenv("HBNB_MYSQL_DB"),
            ),
            pool_pre_ping=True,
        )

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session all objects of the given class.
        """
        try:
            objs = []
            if cls:
                if isinstance(cls, str):
                    cls = eval(cls)
                objs = self.__session.query(cls).all()
            else:
                for model in [State, City, User, Place, Review, Amenity]:
                    objs.extend(self.__session.query(model).all())
            return {
                "{}.{}".format(type(obj).__name__, obj.id): obj
                for obj in objs
            }
        except SQLAlchemyError as e:
            logging.error("Error querying the database: %s", e)
            return {}

    def new(self, obj):
        """Add obj to the current database session."""
        try:
            self.__session.add(obj)
        except SQLAlchemyError as e:
            logging.error("Error adding the object to the session: %s", e)

    def save(self):
        """Commit all changes to the current database session."""
        try:
            self.__session.commit()
        except SQLAlchemyError as e:
            logging.error("Error committing the session: %s", e)
            self.__session.rollback()

    def delete(self, obj=None):
        """Delete obj from the current database session."""
        try:
            if obj is not None:
                self.__session.delete(obj)
        except SQLAlchemyError as e:
            logging.error("Error deleting the object from the session: %s", e)

    def reload(self):
        """
        Create all tables in the database and initialize a new session.
        """
        try:
            Base.metadata.create_all(self.__engine)
            session_factory = sessionmaker(
                bind=self.__engine,
                expire_on_commit=False
            )
            Session = scoped_session(session_factory)
            self.__session = Session()
        except SQLAlchemyError as e:
            logging.error("Error reloading the session: %s", e)

    def close(self):
        """Close the working SQLAlchemy session."""
        try:
            self.__session.remove()  # Using remove() for scoped_session
        except SQLAlchemyError as e:
            logging.error("Error closing the session: %s", e)
