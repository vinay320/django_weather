from django.db import models
from django.utils import timezone
from datetime import timedelta

class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=50)
    celsius_temperature = models.FloatField()
    kelvin_temperature = models.FloatField()
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def is_expired(self):
        expiration_time = timezone.now() - timedelta(minutes=10)
        return self.last_updated < expiration_time

    def __str__(self):
        return f"WeatherData(city={self.city}, description={self.description}, last_updated={self.last_updated})"
