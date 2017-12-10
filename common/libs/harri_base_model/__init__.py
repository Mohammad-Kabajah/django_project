__author__ = 'omar'

from sqlalchemy import Column, Integer, TIMESTAMP, func, Boolean
from sqlalchemy.ext.declarative import declarative_base


class HBaseModel(object):
    id = Column(Integer, primary_key=True)
    created = Column(TIMESTAMP, default=func.now())
    updated = Column(TIMESTAMP, default=func.now(), onupdate=func.current_timestamp())


HBaseModel = declarative_base(cls=HBaseModel)


class HModelMixin(object):
    deleted = Column(Boolean, default=False, nullable=False)
