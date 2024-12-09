import pytest
from apps import calculate_feels_like  # Import the function for testing

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
