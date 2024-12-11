# CS411-Final-Project
Secure Password Storage
○ Database:
■ Create a SQLite table to store usernames, salts, and hashed passwords.
You can implement this using either SQLAlchemy directly or raw SQLite
commands. Using SQLAlchemy is recommended for ease of code re-use.
○ Routes:
■ /login: Checks the provided password against the stored hash. This
route doesn't need to handle actual user sessions.
■ /create-account: Allows new users to register by providing a
username and password.
■ /update-password: Enables users to change their password.


Application Overview:
This Weather Application is a Flask-based API service that provides real-time weather data and geolocation services. It interacts with external APIs such as Visual Crossing Weather API and Abstract API's IP Geolocation to fetch and process weather information. The application also includes functionality to calculate the "feels like" temperature and provides detailed weather forecasts.
Key Features:
* Retrieve geolocation data based on the user's IP address.
* Fetch current weather details for any specified city.
* Calculate "feels like" temperature using parameters like humidity, wind speed, and UV index.
* Provide a 7-day weather forecast for a given city.
* API documentation available via an endpoint.

Routes
1. Health Check
Route Name: Health Check Path: /health Request Type: GET
Purpose
Verifies that the application is running and healthy.
Request Format
* GET Parameters: None
Response Format
{
  "status": "string", // Status of the application
  "message": "string" // Message describing the health status
}
Example
Request:
curl -X GET http://127.0.0.1:5000/health
Response:
{
  "status": "running",
  "message": "Service is healthy"
}

2. Get City Information
Route Name: Get City Path: /get_city Request Type: GET
Purpose
Fetches the user's geolocation data based on their IP address.
Request Format
* GET Parameters: None
Response Format
{
  "city": "string",    // Name of the city
  "region": "string",  // Region or state
  "country": "string"  // Country name
}
Example
Request:
curl -X GET http://127.0.0.1:5000/get_city
Response:
{
  "city": "San Francisco",
  "region": "California",
  "country": "United States"
}

3. Get Current Weather
Route Name: Get Weather Path: /get_weather/<city> Request Type: GET
Purpose
Fetches the current weather data for a specified city.
Request Format
* GET Parameters:
    * city: The name of the city (path parameter).
Response Format
{
  "city": "string",              // Name of the city
  "daily_temperature": "float", // Current average temperature in Fahrenheit
  "daily_max": "float",         // Maximum temperature
  "daily_min": "float",         // Minimum temperature
  "description": "string"       // Weather description
}
Example
Request:
curl -X GET http://127.0.0.1:5000/get_weather/London
Response:
{
  "city": "London",
  "daily_temperature": 55.2,
  "daily_max": 60.0,
  "daily_min": 50.0,
  "description": "Partly cloudy"
}

4. Calculate Feels Like Temperature
Route Name: Calculate Feels Like Path: /calculate_feels_like Request Type: POST
Purpose
Calculates the "feels like" temperature based on temperature, wind speed, humidity, and UV index.
Request Format
* POST Body (JSON):
{
  "temperature": "float",  // Actual temperature in Fahrenheit
  "windspeed": "float",    // Wind speed in mph
  "humidity": "float",     // Humidity as a decimal (e.g., 0.5 for 50%)
  "uvindex": "float"       // UV index
}
Response Format
{
  "feels_like": "string" // Description of the feels like temperature
}
Example
Request:
curl -X POST http://127.0.0.1:5000/calculate_feels_like -H "Content-Type: application/json" -d '{
  "temperature": 85,
  "windspeed": 10,
  "humidity": 0.5,
  "uvindex": 8
}'
Response:
{
  "feels_like": "High UV Index may make temperatures feel warmer. A breeze might provide some relief."
}

5. Get 7-Day Weather Forecast
Route Name: Forecast Path: /forecast/<city> Request Type: GET
Purpose
Provides a 7-day weather forecast for a given city.
Request Format
* GET Parameters:
    * city: The name of the city (path parameter).
Response Format
{
  "city": "string",      // Name of the city
  "forecast": [
    {
      "date": "string",   // Date of the forecast (YYYY-MM-DD)
      "temp": "float",    // Predicted average temperature
      "description": "string" // Weather description
    }
  ]
}
Example
Request:
curl -X GET http://127.0.0.1:5000/forecast/New York
Response:
{
  "city": "New York",
  "forecast": [
    {"date": "2024-12-10", "temp": 32, "description": "Sunny"},
    {"date": "2024-12-11", "temp": 30, "description": "Cloudy"},
    {"date": "2024-12-12", "temp": 28, "description": "Snow"}
  ]
}

6. API Details
Route Name: API Details Path: /api_details Request Type: GET
Purpose
Provides a list of all available API endpoints and their descriptions.
Request Format
* GET Parameters: None
Response Format
{
  "endpoints": ["string"], // List of available endpoints
  "description": "string" // General description of the API
}
Example
Request:
curl -X GET http://127.0.0.1:5000/api_details
Response:
{
  "endpoints": [
    "/get_city",
    "/get_weather/<city>",
    "/calculate_feels_like",
    "/forecast/<city>",
    "/api_details"
  ],
  "description": "API to fetch weather data and process it."
}

How to Run the Application
1. Clone the repository.
2. Install required dependencies using pip install -r requirements.txt.
3. Set up your API keys for Visual Crossing and IP Geolocation as environment variables: export VISUALCROSSING_API_KEY="your_visualcrossing_api_key"
4. export IPGEOLOCATION_API_KEY="your_ipgeolocation_api_key"
5. Start the Flask application: python app.py
6. Access the application endpoints at http://127.0.0.1:5000.

