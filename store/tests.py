from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Location

class LocationAPITestCase(APITestCase):
    def test_location_create(self):
        # Send a POST request to create a new location object
        url = reverse('location_create')
        data = {'latitude': 11.0739, 'longitude': 76.0740}
        response = self.client.post(url, data)

        # Verify that the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the district field is not empty in the response data
        self.assertNotEqual(response.data['district'], None)

        # Verify that a new location object was created in the database
        self.assertEqual(Location.objects.count(), 1)
