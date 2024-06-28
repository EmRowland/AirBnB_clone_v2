#!/usr/bin/python3
"""Defines the State class."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """Defines the State class."""

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship(
        "City",
        backref="state",
        cascade="all,delete-orphan"
    )

    if models.storage_type != "db":

        @property
        def cities(self):
            """Get a list of all related City instances."""
            return [
                city
                for city in models.storage.all(City).values()
                if city.state_id == self.id
            ]
