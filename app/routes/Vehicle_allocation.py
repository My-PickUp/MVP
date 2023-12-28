from fastapi import FastAPI, APIRouter,Depends
from ..database_sql_doc import engine,get_db
from sqlalchemy.orm import Session
from .. import model,schema
from sqlalchemy import Time, Date,text
import datetime
from datetime import time,datetime
from typing import List

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
        current_location = curr_loc.current_location,
        lat = curr_loc.lat,
        lon = curr_loc.lon
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
    from ..Misc.geo_loc import get_lat_long_from_address, driving_dst,get_address_pincode_from_laton

    
    start_time = driver_slot.pickup_time
    
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
    end_time = str(add_hours_to_time(start_time,1))
                   
    result = db.execute(
        raw_sql,
        {
            "start_time" : str(start_time),
            "end_time" : str(end_time)
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
           driver_lat, driver_lon = db.query(model.Current_Location.lat, model.Current_Location.lon).filter(model.Current_Location.driver_id == i).first()
           lat,lon = get_lat_long_from_address(driver_slot.pickup_loc)
           print(f"driver latlon {driver_lat}, {driver_lon}")
           print(f"latlon {lat}, {lon}")
           #find the distance from the driver to the pickup loc and store it in the array 
           #check if the driver has the location nearer to the previous location
           driver_dist = driving_dst(driver_lat,driver_lon,lat,lon)
           if len(temp_array) > 1 :
               if driver_dist > temp_array[1]:
                   temp_array[0] = i 
                   temp_array[1] = driver_dist
               else:
                   pass 
           else:
                temp_array.append(i)
                temp_array.append(driver_dist)
       #assign the driver to the slot
       driver_details = db.query(model.Drivers).filter(model.Drivers.id == temp_array[0]).first()
       driver_info = {**driver_details.__dict__}
       
       loc = get_address_pincode_from_laton(lat,lon)
       location = loc[0]
       pincode = loc[-1]
       
       print(driver_info, driver_slot.date)
       
       print(driver_slot.date)
       
       """
       pickup_time_str = "12:00:00"
pickup_time_obj = datetime.strptime(pickup_time_str, "%H:%M:%S").time()
       """
       
       start_time = datetime.strptime(start_time,"%H:%M:%S").time()
       end_time = datetime.strptime(end_time, "%H:%M:%S").time()
       
       new_slot = model.Driver_Slots(
        driver_id = driver_info['id'],
        driver_name = driver_info['Driver_name'],
        vehicle_number = driver_info['vehicle_number'],
        booked_time_slot = [[start_time,end_time]],
        pincode = [pincode],
        location = [[location,driver_slot.drop_loc]],
        booked_dates = [driver_slot.date]
        )
       db.add(new_slot)
       db.commit()
       
       data = {
           "driver_id" : driver_info['id'],
        "driver_name" : driver_info['Driver_name'],
        "vehicle_number" : driver_info['vehicle_number'],
        "booked_time_slot" : [[start_time,end_time]],
        "pincode" : [pincode],
        "location" : [[location,driver_slot.drop_loc]],
        "booked_dates" : [driver_slot.date]
       }

       return {"output" : data}
       
    return {"ouput" : f"{records}"}
           
