from pydantic import BaseModel, validator
from sqlalchemy import Time
from typing import List, Tuple, Dict, Union
from datetime import time,date,datetime
 
class Add_Driver(BaseModel):
    name : str
    vehicle : str
    vehicle_num : str
    phone : int
    
class AddDriver_loc(BaseModel):
    driver_id : int 
    current_location : str
    lat : float
    lon : float
    
    class Config:
        json_schema_extra = {
            "example": {
                "driver_id" : 1,
                "current_location": "l2b2",
                "lat": "23.342",
                "lon": "23.232"
            }
        }

class Slots(BaseModel):
    pickup_time: str
    pickup_loc: str
    drop_loc: str
    date: date
    
    @validator("pickup_time", pre=True)
    def validate_pickup_time(cls, value):
        parsed_time = datetime.strptime(value, "%H:%M:%S").time()
        return parsed_time.strftime("%H:%M:%S")
    
    class Config:
        json_schema_extra = {
            "example": {
                "pickup_time": "12:00:00",
                "date": "2023-01-02",
                "pickup_loc": "l1a1",
                "drop_loc": "l2b2"
            }
        }
        
    
class AddDriverSlot(BaseModel):
    driver_name : str 
    driver_vh_number : str 
    slots : List[Tuple[time,time]]
    dates: List[date]
    pincode : List[int] 
    location : List[Tuple[str,str]]
    
    @validator("slots", pre=True, each_item=True)
    def parse_time(cls, value):
        return tuple(map(lambda t: time.fromisoformat(t) if isinstance(t, str) else t, value))
    
    @validator("dates", pre=True, each_item=True)
    def parse_date(cls, value):
        return date.fromisoformat(value)
    
    class Config:
        json_schema_extra = {
            "example": {
                "driver_name": "John Doe",
                "driver_vh_number": "ABC123",
                "slots": [["08:00:00", "12:00:00"], ["14:30:00", "18:00:00"]],
                "dates": ["2023-01-01", "2023-01-02"],
                "pincode": [12345, 67890],
                "location": [["l1a1", "l2a2"], ["l3a3", "l4a4"]]
            }
        }
        
class Complete_slot(BaseModel):
    
    ride_date : date
    ride_time : List[time]
    ride_type : str
    customers : List[Dict[str,Union[int,str]]]
    pickup_loc: List[str]
    drop_loc  : List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "ride_date": "2023-12-27",
                "ride_time": ["10:00:00","10:15:00"],
                "ride_type": "string",
                "customers": [
                    {
                        "customer_name": "ABC", 
                        "drop_priority": 1,
                        "co_passenger": "XYZ"
                    }
                ],
                "pickup_loc": ["loc1","loc2"],
                "drop_loc"  : ["loc3","loc4"]
            }
        }
        