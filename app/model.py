from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Time,func,Date, Float
from app.database_sql_doc import Base
from sqlalchemy.dialects.postgresql import ARRAY

class Drivers(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, nullable=False)
    Driver_name = Column(String, nullable=False)
    Phone = Column(Integer, nullable=False)
    Driver_vehicle = Column(String, nullable=False)
    vehicle_number = Column(String, nullable=False)
    
class Customers(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, nullable=False)
    Customer_name = Column(String, nullable= False)
    Phone = Column(Integer, nullable= False)

class Driver_Slots(Base):
    __tablename__ = "driver_slots"
    id = Column(Integer, primary_key=True, nullable= False)
    driver_id = Column(Integer,ForeignKey("drivers.id",ondelete="CASCADE"))
    driver_name = Column(String, nullable=False)
    vehicle_number = Column(String, nullable= False)
    #the structure will be [[time1,time2],[time3,time4]]
    booked_time_slot = Column(ARRAY((Time), dimensions= 2))
    #the structure will be [[pincode1],[pincode2]]
    pincode = Column(ARRAY(Integer)) 
    #the structure will be [[l1a1,l2a2],[l3a3,l4a4]]
    #l1a1 means location 1 area 1
    location = Column(ARRAY((String), dimensions= 2))
    booked_dates = Column(ARRAY(Date))
    
    __table_args__ = (
        CheckConstraint(func.array_length(booked_time_slot, 1) == 2),
        CheckConstraint(func.array_length(location, 1) == 2),
    )

class AllSlots(Base):
    __tablename__ = "all_Slots"
    id = Column(Integer, primary_key=True, nullable= False)
    #customers
    customer_name = Column(ARRAY(String), nullable=False)
    customer_id = Column(ARRAY(Integer), nullable=False)
    customer_drop_priority = Column(ARRAY(String), nullable=False)
    driver_id = Column(Integer,ForeignKey("drivers.id",ondelete="CASCADE"), nullable=False)
    driver_name = Column(String, nullable=False)
    vehicle_number = Column(String, nullable= False)
    driver_vehicle = Column(String, nullable=False)
    #the structure will be [[time1,time2],[time3,time4]]
    booked_time_slot = Column(ARRAY((Time), dimensions= 2), nullable=False)
    #the structure will be [[pincode1],[pincode2]]
    pincode = Column(ARRAY(Integer), nullable=False) 
    #the structure will be [[l1a1,l2a2],[l3a3,l4a4]]
    #l1a1 means location 1 area 1
    pickup_location = Column(ARRAY((String), dimensions= 2), nullable=False)
    drop_location = Column(ARRAY((String), dimensions= 2), nullable=False) 
    booked_dates = Column(Date, nullable=False)
    Ride_type = Column(String, nullable=False)
    co_passenger = Column(String)
    
    __table_args__ = (
        CheckConstraint(func.array_length(booked_time_slot, 0) == 2),
        CheckConstraint(func.array_length(pickup_location, 0) == 2),
    )    

class Customer_Slots(Base):
    __tablename__ = "customer_slots"
    Customer_id = Column(Integer, primary_key=True, nullable=False)
    Customer_name = Column(String, nullable=False)
    #the time slots will be of order [time1,time2]
    booking_slots = Column(ARRAY(Time),)
    #the structure will be [[l1a1,l2a2],[l3a3,l4a4]]
    #l1a1 means location 1 area 1
    location = Column(ARRAY((String), dimensions=2), name='indivisual-location')
    
    __table_args__ = (
        CheckConstraint(func.array_length(booking_slots, 0) == 2),
        CheckConstraint(func.array_length(location, 0) == 2),
    )
    
class Current_Location(Base):
    __tablename__ = "current_location"
    id = Column(Integer, primary_key= True ,nullable=False)
    driver_id = Column(Integer,ForeignKey("drivers.id",ondelete="CASCADE"))
    Driver_name = Column(String, nullable=False)
    current_location = Column(String, nullable=False)
    lat = Column(Float, nullable= False)
    lon = Column(Float, nullable= False)
    
    


    
