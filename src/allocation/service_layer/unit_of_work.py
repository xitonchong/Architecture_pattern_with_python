#pylint: disable=attribute-defined-outside-init 
from __future__  import annotations 

from sqlalchemy  import create_engine 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.orm.session import Session 

from allocation import config 
from allocation.adapters import repository

import abc 


class AbstractUnitOfWork(abc.ABC):
    batches: repository.AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self 

    def __exit__(self, *args):
        self.rollback() 

    @abc.abstractmethod 
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod 
    def rollback(self):
        raise NotImplementedError 




DEFAULT_SESSION_FACTORY = sessionmaker(
    bind = create_engine(
        config.get_postgres_uri(),
    )
)
    