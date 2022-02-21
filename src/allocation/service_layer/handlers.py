from __future__ import annotations 
from typing import TYPE_CHECKING

from allocation.domain import events, model
from allocation.adapters import email 
from allocation.domain.model import OrderLine

class InvalidSku(Exception):
    pass 



def add_batch(event: events.BatchCreated,
    uow: unit_of_work.AbstractUnitOfWork,
): 
    with uow:
        product = uow.products.get(sku=event.sku)
    if product is None: 
        product = model.Product(event.sku, batches=[])
        uow.products.add(product)
    product.batches.append(
        model.Batch(event.ref, event.sku, event.qty, event.eta)
    )
    uow.commit() 




def change_batch_quantity(event: events.BatchQuantityChanged,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        product = uow.products.get_by_batchref(batchref=event.ref)
        product.change_batch_quantity(ref=event.ref, qty=event.qty)
        uow.commit() 


        


def allocate(): 
    ... 


def send_out_stock_notification(
    event: events.OutOfStock,
    uow: unit_of_work.AbstractUnitOfWork,
):
    email.send(
        "stock@made.com",
        f"Out of Stock for {event.sku}"
    )