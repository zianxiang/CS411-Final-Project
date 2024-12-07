import os
import math
import requests
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import NewUserForm

# Load environment variables (if using django-environ or similar)
# If not using django-environ, ensure these variables are available in your OS environment.
VISUALCROSSING_API_KEY = os.getenv('VISUALCROSSING_API_KEY')
IPGEOLOCATION_API_KEY = os.getenv('IPGEOLOCATION_API_KEY')

# Current date/time formatted for the weather API
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S')


def calculate_feels_like(d_temperature, d_windspeed, d_humidity, d_uvindex):
    """
    Takes in daily avg temp, wind speed, humidity, and UV index and returns a 
    string describing how these factors affect the perceived temperature.
    """
    # Convert humidity to a percentage integer
    d_humidity = math.floor(d_humidity * 100)
    feels_like = []

    # Hot day conditions
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
        # Cooler day conditions
        if d_windspeed >= 15:
            feels_like.append("High wind speeds may make temperatures feel cooler.")
        elif d_windspeed >= 7:
            feels_like.append("Breeze may make temperatures feel slightly cooler.")
        else:
            feels_like.append("Temperature reflects outside conditions.")

    return " ".join(feels_like)


def index(request):
    """
    Calls Geolocation and Weather API to display weather information.
    """
    # Fetch user's city via IP geolocation
    # Make sure IPGEOLOCATION_API_KEY is set in environment variables or replace it with your key.
    geo_url = f"https://ipgeolocation.abstractapi.com/v1/?api_key={IPGEOLOCATION_API_KEY}"
    try:
        city_response = requests.get(geo_url)
        city_response.raise_for_status()
        city_data = city_response.json()
        city = city_data.get("city", "Unknown")
    except requests.RequestException:
        # If geolocation fails, set default city or handle gracefully
        city_data = {}
        city = "Unknown"

    # Build weather API URL (Visual Crossing)
    # Ensure VISUALCROSSING_API_KEY is set.
    weather_url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        f"{city}/{formatted_datetime}?unitGroup=us&key={VISUALCROSSING_API_KEY}"
    )

    # Fetch weather data
    try:
        r = requests.get(weather_url)
        r.raise_for_status()
        weather_data = r.json()
    except requests.RequestException:
        weather_data = {}

    # Extract daily and hourly data safely
    feels_like = None
    city_weather = {}

    days = weather_data.get('days', [])
    if days:
        d = days[0]
        hours = d.get('hours', [])
        if hours:
            h = hours[0]

            city_weather = {
                'city': city,
                'daily_temperature': d.get('temp'),
                'daily_max': d.get('tempmax'),
                'daily_min': d.get('tempmin'),
                'daily_description': d.get('description', 'No description'),
                'daily_windspeed': d.get('windspeed', 0),
                'daily_humidity': d.get('humidity', 0),
                'daily_uvindex': d.get('uvindex', 0),
                'hourly_temperature': h.get('temp', 0),
                'hourly_windspeed': h.get('windspeed', 0),
                'hourly_humidity': h.get('humidity', 0),
            }

            # Call feels_like function
            feels_like = calculate_feels_like(
                d.get('temp', 0),
                d.get('windspeed', 0),
                d.get('humidity', 0),
                d.get('uvindex', 0)
            )

    context = {
        'city_weather': city_weather,
        'city_data': city_data,
        'feels_like': feels_like
    }

    if request.user.is_authenticated:
        context['user'] = request.user

    return render(request, 'weatherapp/weather.html', context)


def register_request(request):
    """
    Handles user registration.
    """
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to the weather page (assuming "weather" is a named url pattern)
            return redirect("weather")
        else:
            # Show form errors
            for msg in form.error_messages:
                print(form.error_messages[msg])
    else:
        form = NewUserForm()

    return render(request, "weatherapp/register.html", {"register_form": form})


def login_request(request):
    """
    Handles login process.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("weather")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "weatherapp/login.html", {"login_form": form})


def logout_request(request):
    """
    Logs out the user and redirects to the weather page.
    """
    logout(request)
    return redirect("weather")


@login_required
def profile(request):
    """
    Displays the user's profile.
    """
    return render(request, 'weatherapp/profile.html')
