# forecast/middleware.py
from django.utils import timezone
from datetime import timedelta
from .models import WeatherData
import logging

# Configure logging
logger = logging.getLogger(__name__)

class ExpiredWeatherDataCleanupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        expiration_time = timezone.now() - timedelta(minutes=10)
        
        deleted_count, _ = WeatherData.objects.filter(last_updated__lt=expiration_time).delete()
        
        if deleted_count:
            logger.info(f"Deleted {deleted_count} expired weather data records.")

        response = self.get_response(request)
        return response
