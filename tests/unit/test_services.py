import pytest 
from allocation.adapters import repository 
from allocation.service_layer import services, unit_of_work

# Fake Repository only for testing, inherit from abstract repository 
class FakeRepository(repository.AbstractRepository):
    def __init__(self, batches):
        self._batches =  set(batches) 

    
    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.batches = FakeRepository([])
        self.committed = False 

    def commit(self):
        self.committed = True 

    def rollback(self):
        pass 


def test_add_batch():
    uow = FakeUnitOfWork() 
    services.add_batch('b1', 'CRUNCHY-ARMCHAIR', 100, None, uow)
    assert uow.batches.get('b1') is not None 
    assert uow.committed 


def test_allocate_returns_allocation():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "OMNINOUS-MIRROR", 100, None, uow)
    result = services.allocate("o1", "OMNINOUS-MIRROR", 10, uow)
    assert result == "b1"


def test_allocate_errors_for_invalid_sku():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "AREALSKU", 100, None, uow)

    with pytest.raises(services.InvalidSku, match="Invalid sku FAKESKU"):
        services.allocate("o1", "FAKESKU", 10, uow )
        # is there a different usign session above?


def test_commits():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "OM", 100, None, uow)
    services.allocate("o1", "OM", 10, uow)
    assert uow.committed is True 