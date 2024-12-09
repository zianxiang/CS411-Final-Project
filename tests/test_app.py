import pytest
from apps import calculate_feels_like  # Import the function for testing
import pytest
from unittest.mock import patch

#TESTING CALCULATE FEELS LIKE 
def test_calculate_feels_like_hot_weather():
    #Test for hot weather with high UV, moderate wind, and high humidity.
    
    result = calculate_feels_like(80, 10, 50, 8)  # High temperature, high UV, moderate wind
    assert "High UV Index may make temperatures feel warmer." in result
    assert "A breeze might provide some relief." in result
    assert "High humidity may make temperatures feel warmer." in result

def test_calculate_feels_like_cool_weather():
    #Test for cool weather with high wind and moderate temperature.
    
    result = calculate_feels_like(50, 20, 30, 5)  # Cool temperature, high wind
    assert "High wind speeds may make temperatures feel cooler." in result
    assert "Temperature reflects outside conditions." in result

def test_calculate_feels_like_moderate_weather():
    #Test for moderate weather with no extreme conditions.

    result = calculate_feels_like(70, 5, 60, 4)  # Moderate temperature and wind
    assert "Temperature reflects outside conditions." in result

def test_calculate_feels_like_extreme_cold_weather():
    #Test for extreme cold weather where the wind has minimal effect.

    result = calculate_feels_like(20, 3, 40, 3)  # Very cold temperature, low wind
    assert "Temperature reflects outside conditions." in result
    assert "Breeze may make temperatures feel slightly cooler." not in result

#TESTING FLASK ROUTES 
@pytest.fixture
def client():
    #Fixture to set up Flask test client.
    with app.test_client() as client:
        yield client

@patch("apps.requests.get")

#TESTING FOR THE INDEX ROUTE
def test_index_weather(client, mock_get):
    # Mocking geolocation API response
    mock_get.return_value.json.return_value = {
        "city": "Tokyo", "latitude": 35.6762, "longitude": 139.6503
    }
    mock_get.return_value.status_code = 200
    
    # Mocking weather API response
    mock_get.return_value.json.return_value = {
        'days': [{'temp': 80, 'tempmax': 85, 'tempmin': 75, 'windspeed': 5, 'humidity': 50, 'uvindex': 7}],
        'hours': [{'temp': 78, 'windspeed': 5, 'humidity': 45}],
    }

    # Sending GET request to the `/` route
    response = client.get("/")
    
    # Checking if the response contains the city and the temperature
    assert response.status_code == 200
    assert b"Tokyo" in response.data
    assert b"80" in response.data  # Checking if the temperature is shown in the response

#TESTING FOR THE REGISTER ROUTE 
@patch("apps.requests.get")
def test_register(client, mock_get):
    # Test the `/register` route to ensure user registration works.
    mock_get.return_value.json.return_value = {"city": "Tokyo"}  # Mock geolocation
    # Simulate a POST request with registration data
    response = client.post("/register", data={"username": "testuser", "password": "password123"})
    # Ensure redirection after successful registration
    assert response.status_code == 302  # Should redirect to the index page
    assert b"testuser" in response.data  # Check if the username is in the response

#TESTING FOR THE LOGIN ROUTE 
@patch("apps.requests.get")
def test_login(client, mock_get):
    #Test the `/login` route to ensure that login works with valid credentials.
    mock_get.return_value.json.return_value = {"city": "Tokyo"}  # Mock geolocation
    # Simulate login attempt with valid credentials
    client.post("/register", data={"username": "testuser", "password": "password123"})  # Register first
    response = client.post("/login", data={"username": "testuser", "password": "password123"})
    # Ensure redirection after successful login
    assert response.status_code == 302  # Should redirect to the index page

#TESINNG FOR THE LOGOUT ROUTE 
def test_logout(client):
    # Test the `/logout` route to ensure that users are logged out properly.
    response = client.get("/logout")
    # Ensure redirection after logout
    assert response.status_code == 302  # Should redirect to the index page

#TESTING FOR THE PROGILE 
@patch("apps.requests.get")
def test_profile(client, mock_get):
    #Test the `/profile` route to ensure profile is only accessible to logged-in users.
    mock_get.return_value.json.return_value = {"city": "Tokyo"}  # Mock geolocation
    # Simulate a POST request with registration data
    client.post("/register", data={"username": "testuser", "password": "password123"})  # Register user
    client.post("/login", data={"username": "testuser", "password": "password123"})  # Login user
    # Ensure the profile page loads correctly
    response = client.get("/profile")
    assert response.status_code == 200  # Should return 200 OK
    assert b"testuser" in response.data  # Check if the username is in the response

