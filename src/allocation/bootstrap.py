import inspect 
from typing import Callable 
from allocation.adapters import orm, redis_eventpublisher
from allocation.adapters.notifications import (
    AbstractNotification, 
    EmailNotifications
)

from allocation.service_layer import handlers, messagebus, unit_of_work


def bootstrap(
    start_orm: bool = True,
    uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
    notification: AbstractNotification = None,
    publish: Callable = redis_eventpublisher.publish,
) -> messagebus.MessageBus:
