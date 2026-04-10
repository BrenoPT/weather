import requests
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.geocoders import Nominatim


def Get_Weather(city):
    try:
        cityData = Get_Data(city)
    except (GeocoderUnavailable, GeocoderTimedOut):
        return "Não foi possível estabelecer conexão."
    except InvalidLocation:
        return "Localização inválida."

    lat = cityData["latitude"]
    lon = cityData["longitude"]
    name = cityData["name"]

    try:
        data = Fetch_Api(Create_Url(lat, lon))
    except requests.exceptions.RequestException:
        return "Erro ao receber dados."

    temp = data["current"]["temperature_2m"]

    return f"Temperatura atual em {name}: {temp}°C {Get_Emoji(temp)}"


def Get_Data(city):
    if not city.strip():
        raise InvalidLocation

    geolocator = Nominatim(user_agent="meee")

    try:
        location = geolocator.geocode(city)
    except (GeocoderUnavailable, GeocoderTimedOut):
        raise

    if not location:
        raise InvalidLocation

    locationDict = location.raw

    return {
        "latitude": locationDict["lat"],
        "longitude": locationDict["lon"],
        "name": locationDict["name"],
    }


def Create_Url(lat, lon):
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
