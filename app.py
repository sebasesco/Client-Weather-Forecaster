from flask import Flask, render_template
from requests import get
import datetime

app = Flask(__name__)

# sets webpage route to home page /
@app.route("/")
def home():
    # Uses ipapi API to get IP as well other location information
    ip = get('https://ipapi.co/ip/').text
    city = get('https://ipapi.co/{0}/city/'.format(ip)).text
    region = get('https://ipapi.co/{0}/region/'.format(ip)).text
    countryName = get('https://ipapi.co/{0}/country_name/'.format(ip)).text
    lat = get('https://ipapi.co/{0}/latitude/'.format(ip)).text
    lon = get('https://ipapi.co/{0}/longitude/'.format(ip)).text
    apiKey = "d1e7fa71a867ac46ea183cad0e7e0429"

    # Gets openweathermap API to retireve weather info
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apiKey}&units=imperial'
    
    # Makes a get request to API and turns data into JSON format
    response = get(url).json()

    # Extracts specific data from openweathermap API
    description = response["weather"][0]["description"]
    temp = response["main"]["temp"]
    humidity = response["main"]["humidity"]
    visibility = response["visibility"]
    pressure = response["main"]["pressure"]
    windSpeed = response["wind"]["speed"]
    windDirection = response["wind"]["deg"]
    sunrise = response["sys"]["sunrise"]
    sunset = response["sys"]["sunset"]

    # Converts epoch to date/time
    sunrise = datetime.datetime.fromtimestamp(sunrise)
    sunset = datetime.datetime.fromtimestamp(sunset)

    # Converts from degrees to wind direction
    val = int((windDirection/22.5)+.5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    
    direction = arr[(val % 16)]

    # Renders data onto index.html webpage
    return render_template("index.html", ip=ip, city=city, state=region, country=countryName, description=description, temp=temp, humidity=humidity, visibility=visibility, pressure=pressure, windSpeed=windSpeed, direction=direction, windDirection=windDirection, sunrise=sunrise, sunset=sunset)


if __name__ == "__main__":
    app.run()
