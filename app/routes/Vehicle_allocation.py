from fastapi import FastAPI, APIRouter,Depends
from ..database_sql_doc import engine,get_db
from sqlalchemy.orm import Session
from .. import model,schema
from sqlalchemy import Time, Date,text,and_
import datetime
from datetime import time

model.Base.metadata.create_all(bind = engine)

router = APIRouter(
    prefix="/Vehicle_allocation",
    tags=['vehicle_allocation'] 
)

@router.post("/add_current_location")
def Add_current_locs(curr_loc : schema.AddDriver_loc, db : Session = Depends(get_db)):
    driver_name = db.query(model.Drivers.Driver_name).filter(model.Drivers.id == curr_loc.driver_id).scalar()
    data = model.Current_Location(
        driver_id = curr_loc.driver_id ,
        Driver_name = driver_name,
        current_location = curr_loc.current_location
    )
    db.add(data)
    db.commit()
    return {"data added"}

@router.post("/add-slot")
def Add_slot(driver_slot : schema.AddDriverSlot, db : Session = Depends(get_db)):
    driver__id = db.query(model.Drivers.id).filter(driver_slot.driver_name == model.Drivers.Driver_name).first()
    
    if driver__id is not None : 
        new_slot = model.Driver_Slots(
        driver_id = driver__id.id,
        driver_name = driver_slot.driver_name,
        vehicle_number = driver_slot.driver_vh_number,
        booked_time_slot = driver_slot.slots,
        pincode = driver_slot.pincode,
        location = driver_slot.location,
        booked_dates = driver_slot.dates
        )
        db.add(new_slot)
        db.commit()
    
    return {"data added"}


    
    
@router.post("/alot-slots")
def Driver_slots(driver_slot: schema.Slots, db: Session = Depends(get_db)):
    from ..Misc.misc import add_hours_to_time
    start_time = driver_slot.pickup_time
    aloting_dates = driver_slot.date
    """
    SELECT DISTINCT driver_id
    FROM driver_slots
    WHERE driver_id NOT IN (
    SELECT DISTINCT ds.driver_id
    FROM driver_slots ds
    WHERE booked_time_slot @> ARRAY[time '08:00:00', time '09:00:00']
);
    """
    raw_sql = text("""
                  SELECT DISTINCT driver_id
FROM driver_slots
WHERE driver_id NOT IN (
    SELECT DISTINCT ds.driver_id
    FROM driver_slots ds
    WHERE booked_time_slot @> ARRAY[time :start_time, time :end_time]
);
                  """) 
    result = db.execute(
        raw_sql,
        {
            "start_time" : str(start_time),
            "end_time" : str(add_hours_to_time(start_time,1))
        }
    )

    records = result.all()
    
    if records is not None:
       driver_set = set()
       temp_array = []
       #the temp_array will be [dist, name]
       [driver_set.add(j) for i in records for j in i ]
       #iterate through each driver and check for each location
       print(driver_set)
       for i in driver_set:
           dist_ = db.query(model.Current_Location.current_location).filter(model.Current_Location.driver_id == i).first()
           #find the distance from the driver to the pickup loc and store it in the array 
           
       #check if the driver has the location nearer to the previous location
       #assign the driver to the slot
       
    return {"ouput" : f"{records}"}
           
