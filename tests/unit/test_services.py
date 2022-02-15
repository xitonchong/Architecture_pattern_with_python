import pytest 
from adapters import repository 
from service_layer import services 

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


# Fake Session
class  FakeSession:
    committed = False 

    def commit(self):
        self.committed = True 


def test_add_batch():
    repo, session = FakeRepository([]), FakeSession() 
    services.add_batch('b1', 'CRUNCHY-ARMCHAIR', 100, None, repo, session)
    assert repo.get('b1') is not None 
    assert session.committed 


def test_allocate_returns_allocation():
    repo, session = FakeRepository([]), FakeSession() 
    services.add_batch("b1", "OMNINOUS-MIRROR", 100, None, repo, session)
    result = services.allocate("o1", "OMNINOUS-MIRROR", 10, repo, session)
    assert result == "b1"


def test_allocate_errors_for_invalid_sku():
    repo, session = FakeRepository([]), FakeSession() 
    services.add_batch("b1", "AREALSKU", 100, None, repo, session)

    with pytest.raises(services.InvalidSku, match="Invalid sku FAKESKU"):
        services.allocate("o1", "FAKESKU", 10, repo, FakeSession() )
        # is there a different usign session above?


def test_commits():
    repo, session = FakeRepository([]), FakeSession() 
    services.add_batch("b1", "OM", 100, None, repo, session)
    services.allocate("o1", "OM", 10, repo, session)
    assert session.committed is True 