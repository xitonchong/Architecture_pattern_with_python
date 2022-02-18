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
        product = uow.products.get(sku=sku)
        if product is None:
            product = model.Product(sku, batches=[])
            uow.products.add(product)
        product.batches.append(model.Batch(ref, sku, qty, eta))
        uow.commit()




# we want to pass in only primitive type, and change to domain classes in this functio 
def allocate(
    orderid: str, sku: str, qty: int,
    uow: AbstractUnitOfWork
) -> str:

    line = OrderLine(orderid, sku, qty)
    

    with uow: 
        product = uow.products.get(sku=line.sku)
        if product is None: 
            raise InvalidSku(f"Invalid sku {line.sku}")
        batchref = product.allocate(line) 
        uow.commit() 
    return batchref 