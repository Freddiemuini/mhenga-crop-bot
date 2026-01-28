import requests
from config import AGROMONITORING_API_KEY


def get_weather(lat, lon):
    """Fetch weather data from AgroMonitoring API"""
    try:
        weather_url = f"http://api.agromonitoring.com/agro/1.0/weather?lat={lat}&lon={lon}&appid={AGROMONITORING_API_KEY}"
        weather_response = requests.get(weather_url, timeout=15)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        weather_description = weather_data.get('weather', [{}])[0].get('description', 'Unknown')
        temp_kelvin = weather_data.get('main', {}).get('temp')
        temp_celsius = temp_kelvin - 273.15 if temp_kelvin else 'Unknown'

        return {
            "description": weather_description,
            "temperature_celsius": round(temp_celsius, 2) if isinstance(temp_celsius, (int, float)) else temp_celsius,
            "success": True
        }
    except Exception as e:
        return {
            "error": f"Weather API failed: {str(e)}",
            "success": False
        }


def get_planting_recommendation(temp_celsius):
    """Get planting recommendation based on temperature"""
    if temp_celsius != 'Unknown' and isinstance(temp_celsius, (int, float)) and temp_celsius > 17:
        return "Suitable for planting"
    return "Not suitable for planting"
