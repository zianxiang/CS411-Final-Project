import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env()

# Read the .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Now you can access variables defined in .env like this:
SECRET_KEY = env('SECRET_KEY')
VISUALCROSSING_API_KEY = env('VISUALCROSSING_API_KEY')
IPGEOLOCATION_API_KEY = env('IPGEOLOCATION_API_KEY')
