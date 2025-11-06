from geopy import Nominatim

def get_address_from_gps(latitude: float, longitude: float) -> str:
    geolocator = Nominatim(user_agent="safetyscooter")
    location = geolocator.reverse((latitude, longitude), language='ru')

    if location and location.address:
        return location.address

    return "Адрес не найден"