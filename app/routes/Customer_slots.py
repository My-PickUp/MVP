from fastapi import FastAPI, APIRouter
from ..database_sql_doc import engine,get_db
from sqlalchemy.orm import Session
from .. import model

model.Base.metadata.create_all(bind = engine)

router = APIRouter(
    prefix="/Customer_slots",
    tags=['Customer_slots']
)