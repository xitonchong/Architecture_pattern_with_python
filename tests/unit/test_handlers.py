from datetime import date
import pytest 
from unittest import mock 

from allocation.adapters import repository 
from allocation.domain import events
from allocation.service_layer import handlers, messagebus, unit_of_work



class FakeRepository(repository.AbstractRepository):
    def __init__(self, products):
        super().__init__()
        self._products =  set(products) 

    
    def _add(self, product):
        self._products.add(product)

    def _get(self, sku):
        return next((p for p in self._products if p.sku == sku), None)

    def _get_by_batchref(self, batchref):
        return next( 
            (p for p in self._products for b in p.batches if b.reference == batchref), 
            None,
        )



class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.products = FakeRepository([])
        self.committed = False 

    def _commit(self):
        self.committed = True 

    def rollback(self):
        pass 



class TestAddBatch:
    pass


class TestAllocate:
    pass 

class TestChangeBatchQuantity:
    pass 


