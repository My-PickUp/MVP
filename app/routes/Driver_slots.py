from fastapi import FastAPI, APIRouter, Depends, HTTPException
from app.database_sql_doc import engine,get_db
from sqlalchemy.orm import Session
from app import model,schema

model.Base.metadata.create_all(bind = engine)

router = APIRouter(
    prefix="/Driver_slots",
    tags=['Driver_slots']
)

app = FastAPI()

@router.post("/Add-Drivers")
def add_drivers(Driver : schema.Add_Driver, db : Session = Depends(get_db)):
    temp_vh_num = db.query(model.Drivers.vehicle_number).filter(model.Drivers.vehicle_number == Driver.vehicle_num).first()
    print(temp_vh_num)
    try:
        if temp_vh_num is None:
            data = model.Drivers(
                Driver_name = Driver.name,
                Driver_vehicle = Driver.vehicle,
                vehicle_number = Driver.vehicle_num,
                Phone = Driver.phone
            )
            
            db.add(data)
            db.commit()
            return {"message":f"driver details with the following data has been added {data}"}
        else:
            return {"message":f"vehicle already present, please try a new driver"}
    except Exception as e:
        print(f"Error : {e}")
        raise HTTPException(status_code=500, detail=f"Error processing file : {e}")
        
