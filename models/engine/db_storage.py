import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """Represents a database storage engine."""

    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object."""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                getenv("HBNB_MYSQL_USER"),
                getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"),
                getenv("HBNB_MYSQL_DB"),
            ),
            pool_pre_ping=True,
        )

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on the current database
        session all objects of the given class.
        """
        try:
            if cls is None:
                objs = self.__session.query(State).all()
                objs.extend(self.__session.query(City).all())
                objs.extend(self.__session.query(User).all())
                objs.extend(self.__session.query(Place).all())
                objs.extend(self.__session.query(Review).all())
                objs.extend(self.__session.query(Amenity).all())
            else:
                if isinstance(cls, str):
                    cls = eval(cls)
                objs = self.__session.query(cls).all()
            return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}
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
        Create all tables in the database
         and initialize a new session.
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
            self.__session.close()
        except SQLAlchemyError as e:
            logging.error("Error closing the session: %s", e)
