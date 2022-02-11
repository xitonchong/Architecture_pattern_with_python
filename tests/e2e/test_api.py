import uuid 
import pytest 
import requests 


import config 


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_sku(name=""):
    return f"sku-{name}-{random_suffix()}"


def random_batchref(name=""):
    return f"batch-{name}-{random_suffix()}"


def random_orderid(name=""):
    return f"order-{name}-{random_suffix()}"

# restart_api in conftest.py

@pytest.mark.usefixtures("restart_api")
def test_happy_path_returns_201_and_allocated_batch():
    print('in happy path')