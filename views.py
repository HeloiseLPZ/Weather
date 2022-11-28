from django.shortcuts import render
import requests, json
import datetime as dt
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=&appid=f9fb3f084554c7f8971d9f1ae1768046&lang=fr'
    cities = City.objects.all()
    form = CityForm()
    weather_data = []
    
    for city in cities:
        city_weather = requests.get(
            url.format(city)).json()

        def kelvin_to_celsius(kelvin):
            celsius = kelvin - 273.15
            return celsius

        response = requests.get(
            url.format(city)).json()
        print(response)

        temp_kelvin = response['main']['temp']
        temp_celsius = round(kelvin_to_celsius(temp_kelvin), 1)
        feels_like_kelvin = response['main']['feels_like']
        feels_like_celsius = kelvin_to_celsius(temp_kelvin)
        wind_speed = response['wind']['speed']
        humidiy = response['main']['humidity']
        description = response['weather'][0]['description']
        sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
        sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
    
        weather = {
            'city': city,
            'temperature': temp_celsius,
            'description': description,
            'icon': city_weather['weather'][0]['icon']
        }
    
        weather_data.append(weather)

    context = {'weather_data': weather_data, 'form' : form}

    return render(request, 'weather/index.html', context)

    
