import os
import math
import requests
from datetime import datetime
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
app.secret_key = "your_secret_key"

# API Key
VISUALCROSSING_API_KEY = os.getenv("VISUALCROSSING_API_KEY", "N4LDNA95X9MT5YGWHSF3QRHWJ")
IPGEOLOCATION_API_KEY = os.getenv("IPGEOLOCATION_API_KEY", "795becf8ea1847fc8ae8894ac0666799")

# health check
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "running", "message": "Service is healthy"}), 200

# route1：get city information
@app.route('/get_city', methods=['GET'])
def get_city():
    geo_url = f"https://ipgeolocation.abstractapi.com/v1/?api_key={IPGEOLOCATION_API_KEY}"
    try:
        response = requests.get(geo_url)
        response.raise_for_status()
        city_data = response.json()
        return jsonify({
            "city": city_data.get("city", "Unknown"),
            "region": city_data.get("region", "Unknown"),
            "country": city_data.get("country", "Unknown")
        }), 200
    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch city information", "details": str(e)}), 500

# route2：get weather data
@app.route('/get_weather/<city>', methods=['GET'])
def get_weather(city):
    current_datetime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    weather_url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        f"{city}/{current_datetime}?unitGroup=us&key={VISUALCROSSING_API_KEY}"
    )
    try:
        response = requests.get(weather_url)
        response.raise_for_status()
        weather_data = response.json()
        return jsonify({
            "city": city,
            "daily_temperature": weather_data["days"][0].get("temp"),
            "daily_max": weather_data["days"][0].get("tempmax"),
            "daily_min": weather_data["days"][0].get("tempmin"),
            "description": weather_data["days"][0].get("description")
        }), 200
    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch weather data", "details": str(e)}), 500

# route3：calculate feels like
@app.route('/calculate_feels_like', methods=['POST'])
def calculate_feels_like():
    try:
        data = request.json
        d_temperature = data["temperature"]
        d_windspeed = data["windspeed"]
        d_humidity = data["humidity"]
        d_uvindex = data["uvindex"]

        d_humidity = math.floor(d_humidity * 100)
        feels_like = []

        if d_temperature >= 75:
            if d_uvindex >= 7:
                feels_like.append("High UV Index may make temperatures feel warmer.")
                if d_humidity >= 40:
                    feels_like.append("High humidity may add to the discomfort.")
                if d_windspeed >= 7:
                    feels_like.append("A breeze might provide some relief.")
            elif d_humidity >= 40:
                feels_like.append("High humidity may make temperatures feel warmer.")
                if d_windspeed >= 7:
                    feels_like.append("A breeze might provide some relief.")
            elif d_windspeed >= 7:
                feels_like.append("Breeze may provide some relief against hot temperatures.")
            else:
                feels_like.append("Temperature reflects outside conditions.")
        else:
            if d_windspeed >= 15:
                feels_like.append("High wind speeds may make temperatures feel cooler.")
            elif d_windspeed >= 7:
                feels_like.append("Breeze may make temperatures feel slightly cooler.")
            else:
                feels_like.append("Temperature reflects outside conditions.")

        return jsonify({"feels_like": " ".join(feels_like)}), 200
    except KeyError:
        return jsonify({"error": "Invalid input data"}), 400

# route4：get weather prediction of future 7 day
@app.route('/forecast/<city>', methods=['GET'])
def get_forecast(city):
    weather_url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        f"{city}?unitGroup=us&key={VISUALCROSSING_API_KEY}&include=days"
    )
    try:
        response = requests.get(weather_url)
        response.raise_for_status()
        forecast_data = response.json()["days"]
        forecast = [
            {"date": day["datetime"], "temp": day["temp"], "description": day["description"]}
            for day in forecast_data[:7]
        ]
        return jsonify({"city": city, "forecast": forecast}), 200
    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch forecast data", "details": str(e)}), 500

# route5：return all parameter supported by weather API
@app.route('/api_details', methods=['GET'])
def api_details():
    return jsonify({
        "endpoints": [
            "/get_city",
            "/get_weather/<city>",
            "/calculate_feels_like",
            "/forecast/<city>",
            "/api_details"
        ],
        "description": "API to fetch weather data and process it."
    }), 200

# start Flask application
if __name__ == "__main__":
    app.run(debug=True)
