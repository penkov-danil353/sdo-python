from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from modules.models import *

sqlite_database = "sqlite:///test.db"
engine = create_engine(sqlite_database, echo=True)
Base.metadata.create_all(bind=engine)

