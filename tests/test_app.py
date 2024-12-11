import pytest
from app import calculate_feels_like  # Import the function for testing
import pytest
from unittest.mock import patch

from app import app
from unittest.mock import patch
from werkzeug.security import generate_password_hash, check_password_hash

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

@patch("app.requests.get")

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
@patch("app.requests.get")
def test_register(client, mock_get):
    # testing the `/register` route to ensure user registration works.
    mock_get.return_value.json.return_value = {"city": "Tokyo"}  # Mock geolocation
    # Simulate a POST request with registration data
    response = client.post("/register", data={"username": "testuser", "password": "password123"})
    # Ensure redirection after successful registration
    assert response.status_code == 302  # Should redirect to the index page
    assert b"testuser" in response.data  # Check if the username is in the response

#TESTING FOR THE LOGIN ROUTE 
@patch("app.requests.get")
def test_login(client, mock_get):
    #Testingg the `/login` route to ensure that login works with valid credentials.
    mock_get.return_value.json.return_value = {"city": "Tokyo"}  # Mock geolocation
    # Simulating a login attempt with valid credentials
    client.post("/register", data={"username": "testuser", "password": "password123"})  # Register first
    response = client.post("/login", data={"username": "testuser", "password": "password123"})
    # Ensuring redirection after successful login
    assert response.status_code == 302  # Should redirect to the index page

#TESINNG FOR THE LOGOUT ROUTE 
def test_logout(client):
    # Test the `/logout` route to ensure that users are logged out properly.
    response = client.get("/logout")
    # Ensure redirection after logout
    assert response.status_code == 302  # Should redirect to the index page

#TESTING FOR THE PROGILE 
@patch("app.requests.get")
def test_profile(client, mock_get):
    #Testing the `/profile` route to ensure profile is only accessible to logged-in users.
    mock_get.return_value.json.return_value = {"city": "Tokyo"}  # Mock geolocation
    # Simulate a POST request with registration data
    client.post("/register", data={"username": "testuser", "password": "password123"})  # Register user
    client.post("/login", data={"username": "testuser", "password": "password123"})  # Login user
    # Ensuring the profile page loads correctly
    response = client.get("/profile")
    assert response.status_code == 200  # Should return 200 OK
    assert b"testuser" in response.data  # Check if the username is in the response

# Test setup: Create a test client for Flask app
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@patch('database.user_model.Users.create_account')
def test_create_account(client, mock_create_account):
    # Testing the create_account route to ensure the password is hashed before storing.
    mock_create_account.return_value = None  # Simulate successful account creation

    # Simulate a POST request to create a new user
    response = client.post('/create-account', json={
        'username': 'testuser',
        'password': 'TestPassword123!'
    })
    
    assert response.status_code == 201
    assert b'Account created successfully' in response.data

    # Test error handling (e.g., username already exists)
    mock_create_account.side_effect = ValueError("Username already exists")
    response = client.post('/create-account', json={
        'username': 'testuser',
        'password': 'TestPassword123!'
    })
    
    assert response.status_code == 400
    assert b'Username already exists' in response.data


@patch('database.user_model.Users.check_password')
def test_login(client, mock_check_password):
    #testing the login route to ensure password is correctly verified.
    # Mock the check_password method to simulate valid password check
    mock_check_password.return_value = True  # Simulate correct password

    # testin login with valid credentials
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'TestPassword123!'
    })
    assert response.status_code == 200
    assert b'Login successful' in response.data

    # testing login with invalid credentials
    mock_check_password.return_value = False  # Simulate incorrect password
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'WrongPassword123!'
    })
    assert response.status_code == 401
    assert b'Invalid credentials' in response.data


@patch('database.user_model.Users.update_password')
def test_update_password(client, mock_update_password):
    #testing the update_password route to ensure the password is hased before storaing.
    mock_update_password.return_value = None  # Simulate successful password update

    # Simulating a POST request to update the password
    response = client.post('/update-password', json={
        'username': 'testuser',
        'old_password': 'TestPassword123!',
        'new_password': 'NewPassword123!'
    })
    
    assert response.status_code == 200
    assert b'Password updated successfully' in response.data

    # Test password update for non-existing user
    mock_update_password.side_effect = ValueError("User not found")
    response = client.post('/update-password', json={
        'username': 'nonexistentuser',
        'old_password': 'TestPassword123!',
        'new_password': 'NewPassword123!'
    })
    
    assert response.status_code == 404
    assert b'User not found' in response.data


def test_password_hashing():
    #testing the password is hashed correctly 
    password = "TestPassword123!"
    hashed_password = generate_password_hash(password)
    
    # Verify if the hash matches the original password
    assert check_password_hash(hashed_password, password) == True
    assert check_password_hash(hashed_password, "WrongPassword") == False

def test_password_hash_storage():
    #testing that passwords are stored as hashes 
    password = "TestPassword123!"
    hashed_password = generate_password_hash(password)

    # The password should not be stored in plaintext
    assert password != hashed_password
    assert check_password_hash(hashed_password, password) == True

@patch("app.requests.get")
def test_get_city(client, mock_get):
    # Mocking the geolocation API response
    mock_get.return_value.json.return_value = {
        "city": "Tokyo", "region": "Kanto", "country": "Japan"
    }
    mock_get.return_value.status_code = 200
    
    # testing the `/get_city` route !
    response = client.get("/get_city")
    
    # Check the response
    assert response.status_code == 200
    assert b"Tokyo" in response.data
    assert b"Kanto" in response.data
    assert b"Japan" in response.data

def test_health_check(client):
    # testing the `/health` route !
    response = client.get("/health")
    assert response.status_code == 200
    assert b"Service is healthy" in response.data



