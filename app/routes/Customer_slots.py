from fastapi import FastAPI, APIRouter, Depends, HTTPException
from ..database_sql_doc import engine,get_db
from sqlalchemy.orm import Session
from .. import model,schema
import httpx
from datetime import time,date

model.Base.metadata.create_all(bind = engine)

router = APIRouter(
    prefix="/Customer_slots",
    tags=['Customer_slots']
)

def convert_time_to_str(time_obj: time) -> str:
    sorted_time_list = sorted(time_obj, key=lambda x: (x.hour, x.minute, x.second))
    time_string = sorted_time_list[0].strftime("%H:%M:%S")
    print(time_string)
    return(time_string)

def convert_date_to_str(date_obj : date) -> str:
    return(str(date_obj))
 
@router.post("/customer-slots")
def add_new_customer_slots(cust_slot : schema.Complete_slot, db:Session = Depends(get_db)):
    ride_date = cust_slot.ride_date
    ride_time = cust_slot.ride_time
    ride_type = cust_slot.ride_type
    customer_data = cust_slot.customers
    pickup_locs = cust_slot.pickup_loc
    drop_locs = cust_slot.drop_loc
    
    slot_av = db.query(model.AllSlots.customer_name).filter((model.AllSlots.booked_dates == ride_date)).filter(model.AllSlots.booked_time_slot[0] == ride_time[0]).all()
    print(slot_av)    
    if len(slot_av) == 0:
        driver_slot_alot = "http://127.0.0.1:7000/Vehicle_allocation/alot-slots"
        payload_driver_slot  = {
            "pickup_time" : convert_time_to_str(ride_time),
            "pickup_loc"  : pickup_locs[0],
            "drop_loc"    : drop_locs[1],
            "date"        : convert_date_to_str(ride_date)
        }
        
        try:
            repsonse = httpx.post(driver_slot_alot, json=payload_driver_slot, timeout=120)
            repsonse.raise_for_status()  # Raise an HTTPError for bad responses (non-2xx)
    
            driver_alotted_Resp = repsonse.json()

            if 'output' in driver_alotted_Resp:
                print(driver_alotted_Resp['output'])
                driver_alotted_Resp = driver_alotted_Resp['output']
            else:
                # Handle the case where 'output' is not present in the response
                print("Error: 'output' not found in response.")
                # Optionally, you can raise an exception or set a default value
                raise HTTPException(status_code=500, detail="Unexpected response format")
        except httpx.RequestError as e:
            # Handle network-related errors
            raise HTTPException(status_code=500, detail=f"Request error: {e}")
        except httpx.HTTPStatusError as e:
            # Handle HTTP error responses
            raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: No driver available {e}")
        except httpx.DecodingError as e:
            # Handle JSON decoding error
            raise HTTPException(status_code=500, detail=f"JSON decoding error: {e}")
        
        print(driver_alotted_Resp['output'])
        
        driver_alotted_Resp = driver_alotted_Resp['output']
        
        if ride_type.lower() == "private":
            for i in customer_data:
                co_passenger = i["co_passenger"]
                assert len(co_passenger) == 0
                shared_cust_list.append(customer_name)
                customer_id = db.query(model.Customers.id).filter(model.Customers.Customer_name == customer_name).first()
                if customer_id == None:
                    customer_data = model.Customers(
                        Customer_name = customer_name,
                        Phone = 0000000000
                    )
                    db.add(customer_data)
                    db.commit()
                    customer_id = db.query(model.Customers.id).filter(model.Customers.Customer_name == customer_name).first()
                    data_entry = {
                        "customer_name" : customer_name,
                        "customer_id" : customer_id,
                        "customer_drop_priority" : shared_cust_list,
                        "driver_id" : driver_alotted_Resp['driver_id'],
                        "driver_name" : driver_alotted_Resp['driver_name'],
                        "vehicle_number" : driver_alotted_Resp['vehicle_number'],
                        "driver_vehicle" : str(driver_alotted_Resp['vehicle_number']),
                        "booked_time_slot" : ride_time,
                        "pincode" : driver_alotted_Resp['pincode'],
                        "pickup_location" : pickup_locs,
                        "drop_location" : drop_locs,
                        "booked_dates" : ride_date,
                        "Ride_type" : ride_type,
                        "co_passenger" : ""
                    }
                data = model.AllSlots(
                    customer_name = customer_name,
                    customer_id = customer_id,
                    customer_drop_priority = shared_cust_list,
                    driver_id = driver_alotted_Resp['driver_id'],
                    driver_name = driver_alotted_Resp['driver_name'],
                    vehicle_number = driver_alotted_Resp['vehicle_number'],
                    driver_vehicle = str(driver_alotted_Resp['vehicle_number']),
                    booked_time_slot = ride_time,
                    pincode = driver_alotted_Resp['pincode'],
                    pickup_location = pickup_locs,
                    drop_location = drop_locs,
                    booked_dates = ride_date,
                    Ride_type = ride_type,
                    co_passenger = ""
                )
                db.add(data)
                db.commit()
                
                return (data_entry)
                 
        elif ride_type.lower() == "shared":
            shared_cust_list = []
            for i in customer_data:
                customer_name = i["customer_name"]
                shared_cust_list.append(customer_name)
                co_passenger = i["co_passenger"]
                assert len(co_passenger) != 1
                shared_cust_list.append(co_passenger)
                customer_id = db.query(model.Customers.id).filter(model.Customers.Customer_name == customer_name).first()
                if customer_id == None:
                    customer_data = model.Customers(
                        Customer_name = customer_name,
                        Phone = 0000000000
                    )
                    db.add(customer_data)
                    db.commit()
                    customer_id = db.query(model.Customers.id).filter(model.Customers.Customer_name == customer_name).first()
                
                    data_entry = {
                        "customer_name" : customer_name,
                        "customer_id" : customer_id,
                        "customer_drop_priority" : shared_cust_list,
                        "driver_id" : driver_alotted_Resp['driver_id'],
                        "driver_name" : driver_alotted_Resp['driver_name'],
                        "vehicle_number" : driver_alotted_Resp['vehicle_number'],
                        "driver_vehicle" : str(driver_alotted_Resp['vehicle_number']),
                        "booked_time_slot" : ride_time,
                        "pincode" : driver_alotted_Resp['pincode'],
                        "pickup_location" : pickup_locs,
                        "drop_location" : drop_locs,
                        "booked_dates" : ride_date,
                        "Ride_type" : ride_type,
                        "co_passenger" : ""
                    }   
                
                data = model.AllSlots(
                    customer_name = [customer_name],
                    customer_id = customer_id,
                    customer_drop_priority = shared_cust_list,
                    driver_id = driver_alotted_Resp['driver_id'],
                    driver_name = driver_alotted_Resp['driver_name'],
                    vehicle_number = driver_alotted_Resp['vehicle_number'],
                    driver_vehicle = str(driver_alotted_Resp['vehicle_number']),
                    booked_time_slot = [ride_time],
                    pincode = driver_alotted_Resp['pincode'],
                    pickup_location = [pickup_locs],
                    drop_location = [drop_locs],
                    booked_dates = ride_date,
                    Ride_type = ride_type,
                    co_passenger = co_passenger
                )
                db.add(data)
                db.commit()   
                return(data_entry)
        else:
            raise HTTPException(status_code=405, detail="trying to book from more than customers in one private ride")
        
        
    else:
        return{'slot already on that date time'}