# pylint: disable=redefined-outer-name
from datetime import date
from sqlalchemy.orm import clear_mappers
from unittest import mock 
import pytest 
from allocation import bootstrap, views
from allocation.domain import commands
from allocation.service_layer import unit_of_work


today = date.today() 



@pytest.fixture
def sqlite_bus(sqlite_session_factory):
    bus = bootstrap.bootstrap(
        start_orm=True,
        uow=unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory),
        notifications=mock.Mock(),
        publish= lambda *args: None,
    )
    yield bus
    clear_mappers()


def test_allocations_view(sqlite_bus):
    '''allocate one batch to batch 1, and do some transaction on other batch
    , make sure that nothing happens to batch 1'''
    sqlite_bus.handle(commands.CreateBatch("sku1batch", "sku1", 50 , None))
    sqlite_bus.handle(commands.CreateBatch("sku2batch", "sku2", 50, today))
    sqlite_bus.handle(commands.Allocate("order1", "sku1", 20))
    sqlite_bus.handle(commands.Allocate("order2", "sku2", 20))
    # add a spurious batch and order to make sure we're getting the right ones
    sqlite_bus.handle(commands.CreateBatch("sku1batch-later", "sku1", 30))
    sqlite_bus.handle(commands.Allocate("otherorder", "sku2", 10))

    assert views.allocations("order1", sqlite_bus.uow) == [
        {"sku": "sku1", "batchref": "sku1batch"},
        {"sku": "sku2", "batchref": "sku2batch"},
    ]


def test_deallocation(sqlite_bus):
    ''' test same sku, if first batch is change to smaller batch, allocate should 
    go to batch no 2 with the same sku'''
    sqlite_bus.handle(commands.CreateBatch("b1", "sku1", 50, None))
    sqlite_bus.handle(commands.CreateBatch("b2", "sku1", 50, today))
    sqlite_bus.handle(commands.Allocate("o1", "sku1", 40))
    sqlite_bus.handle(commands.ChangeBatchQuantity("b1", 10))

    assert views.allocations("o1", sqlite_bus) == [
        {"sku": "sku1", "batchref": "b2"},
    ]