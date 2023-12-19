from geopy.geocoders import Nominatim
from pydantic import BaseModel
import requests

def get_address_pincode_from_laton(latitude, longitude):
    geolocator = Nominatim(user_agent="my-geocoder")
    
    location = geolocator.reverse((latitude, longitude), language='en')
    address = location.address if location else None 
    pincode = location.raw.get('address', {}).get('postcode') if location else None 
    
    return address, pincode 

def get_pincode_from_address(address):
    geolocator = Nominatim(user_agent="my-geocoder")
    location = geolocator.geocode(address)
    
    if location:
        print("Raw Data:", location.raw)
        pincode = location.raw.get('address', {}).get('postcode')
        if pincode:
            return pincode
        else:
            print("Postal code not found in raw data.")
            return None
    else:
        print("Geocoding failed for address:", address)
        return None

def get_lat_long_from_address(address : str):
    import requests


    url = "https://maps-data.p.rapidapi.com/geocoding.php"


    querystring = {"query":address,"lang":"en","country":"fr"}


    headers = {
    "X-RapidAPI-Key": "e5d677f092msh4fe5d9ac84e7f83p1c481fjsnf14ebc7fe6c7",
    "X-RapidAPI-Host": "maps-data.p.rapidapi.com"
    }


    response = requests.get(url, headers=headers, params=querystring)

    response = response.json()
    
    lat = response["data"]['lat']
    long = response["data"]['lng']

    return([lat,long])
    
def geocodeing_data(address, api_key):
    base_url = "https://geocode.search.hereapi.com/v1/geocode"
    parmas = {
        "q" : address,
        "apiKey" : api_key
    }
    
    response = requests.get(base_url, params=parmas)
    data = response.json()
    
    if response.status_code == 200 and data.get("items"):
        location = data["items"][0]["position"]
        address_details = data["items"][0]["address"]
        
        latitude = location["lat"]
        longitude = location["lng"]
        postal_code = address_details.get("postlaCode")
        
        return {"lat":latitude,
                "long":longitude, "pincode":postal_code}
    else:
        print(f"Error : {response.status_code} {data.get('title')}")

x = geocodeing_data("UNITED CRICKET CLUB , NOIDA","NONtRb0nM3nqpEos8Z8ulTyYAFlt2RQIeSEgYJThoR0")
print("Result:", x)

from geopy.geocoders import Here
from geopy.extra.rate_limiter import RateLimiter

import requests

def get_geocoding_data(address):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data:
        # Extracting information from the response
        location = data[0]

        latitude = location["lat"]
        longitude = location["lon"]
        display_name = location["display_name"]
        
        return {
            "latitude": latitude,
            "longitude": longitude,
            "display_name": display_name,
        }
    else:
        print(f"Error: Unable to geocode address {address}")
        return None
    
def driving_dst(orig_lat, orig_lon, dest_lat, dest_lon):
    import geopy.distance as dst
    origin = (orig_lat,orig_lon)
    destination = (dest_lat,dest_lon)
    return(dst.distance(origin, destination))