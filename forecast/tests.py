from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

class WeatherDataViewTest(TestCase):

    @patch('forecast.views.requests.get')
    def test_invalid_api_response(self, mock_get):
        
        mock_get.return_value.status_code = 500  
        mock_get.return_value.json.return_value = {}

        
        response = self.client.post(reverse('home'), {
            'latitude': '40.7128',
            'longitude': '-74.0060',
            'detailing_type': 'current',
        })

        
        self.assertContains(response, 'Unable to retrieve weather data. Please try again.')

        

    def test_missing_input(self):
       
        response = self.client.post(reverse('home'), {
            'latitude': '40.7128',
            'longitude': ''  
            
        })

       
        self.assertContains(response, 'Latitude, Longitude, and detailing type are required.')

        