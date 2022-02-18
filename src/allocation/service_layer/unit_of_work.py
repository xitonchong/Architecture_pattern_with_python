#pylint: disable=attribute-defined-outside-init 
from __future__  import annotations 

from sqlalchemy  import create_engine 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.orm.session import Session 

from allocation import config 
from allocation.adapters import repository

import abc 
from .  import messagebus


class AbstractUnitOfWork(abc.ABC):
    products: repository.AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self 

    def __exit__(self, *args):
        self.rollback() 


    def commit(self):
        self._commit()
        self.publish_events()


    def publish_events(self):
        for product in self.products.seen:
            while product.events:
                event = product.events.pop(0)
                messagebus.handle(event)
                

    @abc.abstractmethod 
    def rollback(self):
        raise NotImplementedError 

    
    @abc.abstractclassmethod
    def _commit(self):
        raise NotImplemented 

    


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind = create_engine(
        config.get_postgres_uri(),
        isolation_level="REPEATABLE READ"
    )
)
    

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory() # type session 
        self.products = repository.SqlAlchemyRepository(self.session) 
        return super().__enter__() # essentially calling return self froim abstractunitofwork


    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close() 

    def _commit(self):
        self.session.commit() # using rollback function from sessionmaker


    def rollback(self):
        self.session.rollback() 