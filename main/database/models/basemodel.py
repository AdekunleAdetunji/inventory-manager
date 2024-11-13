#!/usr/bin/env python3
"""
This module contains the BaseModel class that contains shared class attributes
and methods between all database models
"""
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import inspect
from sqlalchemy import UUID
from uuid import uuid4
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from ..base import Base


class BaseModel(Base):
    """BaseModel class for all tables"""

    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        UUID,
        primary_key=True,
        nullable=False,
        default=uuid4,
    )
    created: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    updated: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes new model object with kwargs arguments
        """
        # if class has attr. with key name, assign the key value to the attr
        for k, v in kwargs.items():
            if k not in ["created", "updated", "id"] and hasattr(self, k):
                # assign key value to each class attribute in the kwargs
                setattr(self, k, v)

    def to_dict(self) -> dict:
        """
        get dictionary representation of an initialized model
        """
        return {
            c.key: (
                getattr(self, c.key).strftime("%Y-%m-%dT%H:%M:%S")
                if isinstance(getattr(self, c.key), datetime)
                else getattr(self, c.key)
            )
            for c in inspect(self).mapper.column_attrs
        }

    def __repr__(self) -> str:
        """
        return a string representation of the class that can be reinstantiated
        """
        # convert dictionary to a string of format (k=v)
        args_tup = ", ".join([f"{k}={v}" for k, v in self.to_dict().items()])
        return f"{type(self).__name__}({args_tup})"

    def __str__(self) -> str:
        """return human readable representation of the class instance"""
        return self.__repr__()


if __name__ == "__main__":
    # from sqlalchemy import inspect
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine("sqlite://", echo=False)

    class User(BaseModel):
        __tablename__ = "users"
        pass

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        user_1 = User()
        session.add(user_1)
        session.commit()
        session.flush()
        print(user_1)
