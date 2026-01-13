import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut

def Get_Weather(city):
    try:
        coords = Get_Coords(city)
    except (GeocoderUnavailable, GeocoderTimedOut):
        return "Não foi possível estabelecer conexão."
    except InvalidLocation:
        return "Localização inválida."

    lat = coords["latitude"]
    lon = coords["longitude"]

    try:
        data = Fetch_Api(Create_Url(lat,lon))
    except requests.exceptions.RequestException:
        return "Erro ao receber dados."

    temp = data["current"]["temperature_2m"]

    return  f"Temperatura atual em {city}: {temp}°C {Get_Emoji(temp)}"

def Get_Coords(city):
    if not city.strip():
        raise InvalidLocation
    
    geolocator = Nominatim(user_agent="meee")

    try:
        location = geolocator.geocode(city)
    except (GeocoderUnavailable, GeocoderTimedOut):
        raise

    if not location:
        raise InvalidLocation
    
    return {"latitude": location.latitude, "longitude": location.longitude}
    
def Create_Url(lat,lon):
    return f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"

def Fetch_Api(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def Get_Emoji(temp):
    match temp:
        case temp if 15 >= temp:
            return "🥶"
        case temp if 25 >= temp > 15:
            return "😎"
        case _:
            return "🥵"

class InvalidLocation(Exception):
    pass