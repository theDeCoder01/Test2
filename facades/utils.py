import json

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


def load_config(path_to_config: str = "./resources/config.json"):
    with open(path_to_config) as f:
        confg = json.load(f)
    return confg


def load_db(path_to_config: str = "./resources/config.json"):
    confg = load_config(path_to_config)

    engine = create_engine(confg.get("SQLALCHEMY_DATABASE_URI"))

    Base = automap_base()
    Base.prepare(engine, reflect=True)

    session = Session(engine, autoflush=False, autocommit=False)
    return session, Base
