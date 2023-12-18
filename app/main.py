from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import Vehicle_allocation, Customer_slots, Driver_slots
from . import model
from .database_sql_doc import engine
 
app = FastAPI()

model.Base.metadata.create_all(bind = engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
                   )

@app.get("/")
def read_root():
    return {"Hello" : "World"}

app.include_router(Vehicle_allocation.router)
app.include_router(Customer_slots.router)
app.include_router(Driver_slots.router)