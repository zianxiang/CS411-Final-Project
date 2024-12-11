#!/bin/bash

# Define the base URL for the Flask app
BASE_URL="http://localhost:5000"

# Function to echo JSON responses if needed
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done


# HEALTH CHECK #
check_health() {
 #checking if the app is running by sednign a request to the base URL	
  echo "Checking health status..."
  response=$(curl -s -X GET "$BASE_URL/")
  if [[ "$response" == *"Weather Dashboard"* ]]; then
    echo "App is running!"
  else
    echo "Health check failed."
    exit 1
  fi
}


# USER REGISTRATION #
register_user() {
 #checking if registration works by sending a POST req to the /register route 	 
  echo "Registering user 'testuser'..."
  response=$(curl -s -X POST "$BASE_URL/register" -d "username=testuser&password=TestPassword123!")
  if [[ "$response" == *"redirect"* ]]; then
    echo "User registered successfully!"
  else
    echo "User registration failed."
    exit 1
  fi
}



# USER LOGIN #
login_user() {
  #checking logging in by sending a POST request 
  echo "Logging in user 'testuser'..."
  response=$(curl -s -X POST "$BASE_URL/login" -d "username=testuser&password=TestPassword123!")
  if [[ "$response" == *"redirect"* ]]; then
    echo "User logged in successfully!"
  else
    echo "Login failed."
    exit 1
  fi
}



# FETCH WEATHER DATA # 
get_weather_data() {
  #checking fetching weather data
  echo "Fetching weather data..."
  response=$(curl -s -X GET "$BASE_URL/")
  if [[ "$response" == *"Current Weather"* && "$response" == *"feels like"* ]]; then
    echo "Weather data fetched successfully!"
  else
    echo "Failed to fetch weather data."
    exit 1
  fi
}


# USER LOGOUT #
logout_user() {
  #checking logging out a client by sending a GET req
  echo "Logging out user..."
  response=$(curl -s -X GET "$BASE_URL/logout")
  if [[ "$response" == *"redirect"* ]]; then
    echo "User logged out successfully!"
  else
    echo "Logout failed."
    exit 1
  fi
}


# PROFILE ACESS #
access_profile() {
  #checking if profile access works by sending a GET req 
  echo "Accessing user profile..."
  response=$(curl -s -X GET "$BASE_URL/profile")
  if [[ "$response" == *"Profile Page"* ]]; then
    echo "Profile accessed successfully!"
  else
    echo "Failed to access profile."
    exit 1
  fi
}


# EXECUTE SMOKE TEST #
check_health # Health check
register_user # User registration
login_user # User login
get_weather_data # Fetch weather data
logout_user # User logout

# Profile access (ensure user is logged in first)
login_user
access_profile

echo "All smoke tests completed successfully!"

