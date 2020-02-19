from astral import LocationInfo
import datetime

# l = LocationInfo('name', 'region', 'timezone/name', 0.1, 1.2)

city = LocationInfo("Newcastle Upon Tyne", "England", "Europe/London", 55.0464, 1.4513)
print((
    f"Information for {city.name}/{city.region}\n"
    f"Timezone: {city.timezone}\n"
    f"Latitude: {city.latitude:.02f}; Longitude: {city.longitude:.02f}\n"
))