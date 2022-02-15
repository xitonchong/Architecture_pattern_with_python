from flask import Flask, request 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from datetime import datetime 

import config
from domain import model 
from adapters import orm
from adapters import repository  
from service_layer import services 


orm.start_mappers() 
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))

app = Flask(__name__)



@app.route("/add_batch", methods=["POST"])
def add_batch():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    eta = request.json["eta"]
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    services.add_batch(
        request.json["ref"],
        request.json["sku"],
        request.json["qty"],
        eta,
        repo,
        session,
    )
    return "OK", 201



@app.route("/allocate", method=["POST"])
def allocate_endpoint():
    session = get_session() 
    repo = repository.SqlAlchemyRepository(session)
    try:
        batchref = services.allocate(
            request.json["orderid"],
            request.json["sku"],
            request.json["qty"],
            repo,
            session,
        )
    except (model.OutOfStock, services.InvalidSku)  as e: 
        return {"message": str(e)}, 400


    return {"batchref": batchref}, 201