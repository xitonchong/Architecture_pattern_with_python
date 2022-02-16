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
    

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factor=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory() # type session 
        self.batches = repository.SqlAlchemyRepository(self.session) 
        #only init repo wehn needed, pace in __enter__ method
        return super().__enter__() # essentially calling return self froim abstractunitofwork


    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close() 

    def commit(self):
        self.session.commit() # using rollback function from sessionmaker


    def rollback(self):
        self.session.rollback() 