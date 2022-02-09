import model 
import repository 




def test_repository_can_save_a_batch(session):
    batch = model.Batch("batch1", "sku1", 12, None)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit() # need to commit after adding else not shown in db

    rows = session.execute(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"')
    assert list(rows) == [("batch1", "sku1", 12, None)]


def insert_order_line(session):
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty)"
        ' VALUES ("order1", "GENERIC-SOFA", 12)'
    )
    [[orderid]] = session.execute(
        "SELECT id from order_lines WHERE orderid=:orderid AND sku=:sku",
        dict(orderid="order1", sku="GENERIC-SOFA"),
    )
    return orderid 

def insert_batch(session, batch_id):
    session.execute(
        "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
        ' VALUES (:batch_id, "GENERIC-SOFA", 100, null)',
        dict(batch_id=batch_id),
    )
    [[batch_id]] = session.execute(
        'SELECT id FROM batches WHERE reference=:batch_id AND sku="GENERIC-SOFA"',
        dict(batch_id=batch_id),
    )
    return batch_id


def insert_allocations(session, orderline_id, batch_id):
    session.execute(
        "INSERT INTO allocations (orderline_id, batch_id) "
        " VALUES (:orderline_id, :batch_id)",
        dict(orderline_id=orderline_id, batch_id=batch_id)
    )



def test_repository_can_retrieve_a_batch_with_allocations(session):
    # create batch
    # create orderline 
    olid = insert_order_line(session) # hardcoded orderid "order1"
    batch1_id = insert_batch(session, "batch1")
    print(f"batch1_id is {batch1_id}")
    insert_batch(session, "batch2")
    insert_allocations(session, olid, batch1_id) 

    repo = repository.SqlAlchemyRepository(session)
    retrieved = repo.get(reference="batch1")

    expected = model.Batch("batch1", 'GENERIC-SOFA', 100, None)
    assert retrieved == expected # only compare reference
    assert retrieved.sku == expected.sku 
    assert retrieved._purchased_quantity == expected._purchased_quantity 
    assert retrieved._allocations == {
        model.OrderLine("order1", "GENERIC-SOFA", 12),
    }


