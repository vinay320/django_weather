from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
import requests
from .models import WeatherData

def home(request):
    context = {}

    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        detailing_type = request.POST.get('detailing_type')

        if latitude and longitude and detailing_type:
            api_key = 'YOUR_API_KEY'
            if detailing_type == 'current':
                url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid=d2456f98d4e676f279930ef523298c8a'
            elif detailing_type == 'hourly':
                url = f'http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid=d2456f98d4e676f279930ef523298c8a'
            elif detailing_type == 'daily':
                url = f'http://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude=hourly,minutely&appid=d2456f98d4e676f279930ef523298c8a'
            else:
                context['error'] = 'Invalid detailing type.'
                return render(request, 'home.html', context)

            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200 and 'weather' in data:
                if detailing_type == 'current':
                    now_utc = timezone.now()
                    ist_offset = timedelta(hours=5, minutes=30)
                    last_updated_ist = now_utc + ist_offset
                    weather_data = WeatherData.objects.update_or_create(
                        city=data['name'],
                        defaults={
                            'description': data['weather'][0]['description'],
                            'icon': data['weather'][0]['icon'],
                            'celsius_temperature': round(data['main']['temp'] - 273.15, 2),
                            'kelvin_temperature': round(data['main']['temp'], 2),
                            'humidity': data['main']['humidity'],
                            'pressure': data['main']['pressure'],
                            'last_updated': last_updated_ist
                        }
                    )[0]
                    
                    context['data'] = {
                        'city': data['name'],
                        'description': data['weather'][0]['description'],
                        'icon': data['weather'][0]['icon'],
                        'celsius_temperature': round(data['main']['temp'] - 273.15, 2),
                        'kelvin_temperature': round(data['main']['temp'], 2),
                        'humidity': data['main']['humidity'],
                        'pressure': data['main']['pressure']
                    }
                elif detailing_type in ['hourly', 'daily']:
                    forecast_data = data['list'][0] if detailing_type == 'hourly' else data['daily'][0]
                    context['data'] = {
                        'description': forecast_data['weather'][0]['description'],
                        'icon': forecast_data['weather'][0]['icon'],
                        'celsius_temperature': round(forecast_data['main']['temp'] - 273.15, 2),
                        'kelvin_temperature': round(forecast_data['main']['temp'], 2),
                        'humidity': forecast_data['main']['humidity'],
                        'pressure': forecast_data['main']['pressure']
                    }
                else:
                    context['error'] = 'Invalid detailing type.'
            else:
                context['error'] = 'Unable to retrieve weather data. Please try again.'
        else:
            context['error'] = 'Latitude, Longitude, and detailing type are required.'
    return render(request, 'home.html', context)
