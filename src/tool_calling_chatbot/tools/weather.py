import requests

def get_weather(location: str) -> str:
    if "," not in location:
        location = f"{location}, Australia"

    # Geocode
    geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1").json()
    if not geo.get("results"):
        return f"Could not find location: {location}"

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]
    tz = geo["results"][0]["timezone"]

    # Weather request using current_weather
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current_weather=true&timezone={tz}"
    )
    weather_resp = requests.get(weather_url)
    if weather_resp.status_code != 200:
        return f"Unable to fetch weather data. Status: {weather_resp.status_code}"

    data = weather_resp.json()
    current = data.get("current_weather")
    if not current:
        return "Unable to fetch weather data."

    temp = current["temperature"]
    windspeed = current["windspeed"]
    weathercode = current["weathercode"]

    return f"The current temperature in {location} is {temp}°C with wind speed {windspeed} m/s and weather code {weathercode}."