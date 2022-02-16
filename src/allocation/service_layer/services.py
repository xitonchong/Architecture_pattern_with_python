from __future__ import annotations 

from typing import Optional
from datetime import date 

from allocation.domain import model 
from allocation.domain.model import OrderLine 
from allocation.adapters.repository import AbstractRepository 
from allocation.service_layer.unit_of_work import AbstractUnitOfWork

class InvalidSku(Exception):
    pass 



def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def add_batch(
    ref: str, sku: str, qty: int, eta: Optional[date],
    uow: AbstractUnitOfWork
):
    with uow:
        uow.batches.add(model.Batch(ref, sku, qty, eta))
        uow.commit()




# we want to pass in only primitive type, and change to domain classes in this functio 
def allocate(
    orderid: str, sku: str, qty: int,
    uow: AbstractUnitOfWork
) -> str:

    line = OrderLine(orderid, sku, qty)
    

    with uow: 
        batches = uow.batches.list()
        if not is_valid_sku(line.sku, batches):
            raise InvalidSku(f"Invalid sku {line.sku}")
        batchref = model.allocate(line, batches)
        uow.commit() 
    return batchref 