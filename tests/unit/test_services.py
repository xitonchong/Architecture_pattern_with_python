import pytest 
from unittest import mock 
from allocation.adapters import repository 
from allocation.service_layer import services, unit_of_work



class FakeRepository(repository.AbstractRepository):
    def __init__(self, products):
        super().__init__()
        self._products =  set(products) 

    
    def _add(self, product):
        self._products.add(product)

    def _get(self, sku):
        return next((p for p in self._products if p.sku == sku), None)



class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.products = FakeRepository([])
        self.committed = False 

    def _commit(self):
        self.committed = True 

    def rollback(self):
        pass 



def test_add_batch():
    uow = FakeUnitOfWork() 
    services.add_batch('b1', 'CRUNCHY-ARMCHAIR', 100, None, uow)
    assert uow.products.get('CRUNCHY-ARMCHAIR') is not None 
    assert uow.committed 


def test_add_batch_for_existing_product():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "OMNINOUS-MIRROR", 100, None, uow)
    services.add_batch("b2", "OMNINOUS-MIRROR", 99, None, uow) 
    assert "b2" in [b.reference for b in uow.products.get("OMNINOUS-MIRROR").batches]


def test_allocate_returns_allocation():
    uow = FakeUnitOfWork() 
    services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow) 
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, uow)
    assert result == "batch1"
    

def test_allocate_errors_for_invalid_sku():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "AREALSKU", 100, None, uow)

    with pytest.raises(services.InvalidSku, match="Invalid sku FAKESKU"):
        services.allocate("o1", "FAKESKU", 10, uow )
        # is there a different usign session above?


def test_allocate_commits():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "OM", 100, None, uow)
    services.allocate("o1", "OM", 10, uow)
    assert uow.committed is True 

def test_sends_email_on_out_of_stock_error():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "POPULAR-CURTAINS", 9, None, uow)

    with mock.patch("allocation.adapters.email.send_mail") as mock_send_mail:
        services.allocate("o1", "POPULAR-CURTAINS", 10, uow)
        assert mock_send_mail.call_args == mock.call(
            "stock@made.com",
            f"Out of stock for POPULAR-CURTAINS"
        )
