import math
import requests
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "some_secret_key"  # 实际部署时请从环境变量中获取

# 配置你的 API Key
VISUALCROSSING_API_KEY = "你的VISUALCROSSING_API_KEY"
IPGEOLOCATION_API_KEY = "你的IPGEOLOCATION_API_KEY"

# 模拟用户数据存储（内存中），实际可使用数据库
users = {}  # 格式: { "username": {"password_hash": "..."} }

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_request"


class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    # user_id 就是 username，这里在内存中加载
    if user_id in users:
        return User(user_id)
    return None


def calculate_feels_like(d_temperature, d_windspeed, d_humidity, d_uvindex):
    """
    与之前Django版本相同的逻辑
    """
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

    return " ".join(feels_like)


@app.route("/")
def index():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S')

    # Geolocation
    geo_url = f"https://ipgeolocation.abstractapi.com/v1/?api_key={IPGEOLOCATION_API_KEY}"
    try:
        city_response = requests.get(geo_url)
        city_response.raise_for_status()
        city_data = city_response.json()
        city = city_data.get("city", "Unknown")
    except requests.RequestException:
        city_data = {}
        city = "Unknown"

    # Weather
    weather_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{formatted_datetime}?unitGroup=us&key={VISUALCROSSING_API_KEY}"
    try:
        r = requests.get(weather_url)
        r.raise_for_status()
        weather_data = r.json()
    except requests.RequestException:
        weather_data = {}

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
            feels_like = calculate_feels_like(
                d.get('temp', 0),
                d.get('windspeed', 0),
                d.get('humidity', 0),
                d.get('uvindex', 0)
            )

    context = {
        'city_weather': city_weather,
        'city_data': city_data,
        'feels_like': feels_like,
        'user': current_user if current_user.is_authenticated else None
    }

    return render_template('weather.html', **context)


@app.route("/register", methods=["GET", "POST"])
def register_request():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users:
            flash("Username already exists.", "error")
        else:
            # 保存用户并加密密码
            password_hash = generate_password_hash(password)
            users[username] = {"password_hash": password_hash}
            login_user(User(username))
            return redirect(url_for("index"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login_request():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user_data = users.get(username)
        if user_data and check_password_hash(user_data["password_hash"], password):
            login_user(User(username))
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password.", "error")
    return render_template("login.html")


@app.route("/logout")
def logout_request():
    logout_user()
    return redirect(url_for("index"))


@app.route("/profile")
@login_required
def profile():
    # 已经通过@login_required确保用户已登录
    return render_template("profile.html", user=current_user)


if __name__ == "__main__":
    app.run(debug=True)
