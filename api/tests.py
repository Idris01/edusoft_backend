from rest_framework.test import APITestCase
from backend.models import University
from cities_light.models import Country
from rest_framework import status
from django.urls import reverse

"""DEfine tests for edusoft APIs"""


class TestUniversity(APITestCase):
    """Define tests for University"""

    def setUp(self):
        """Create sample data for testing"""
        country = Country.objects.get(code2="NG")  # get country using country code2

        University.objects.create(
            name="Ladoke Akintola University of Technology",
            history="Founded August 1990",
            country=country,
            accomodation="On-campus accomodation available",
            postal_code="210212",
            city="Ogbomoso",
            website="www.lautech.edu.ng",
            languages=["Yoruba", "English", "Arabic"],
        )

    def test_university_list_ok(self):
        """test GET method on  /api/universities"""
        url_name = "university_list_create"
        url = reverse(url_name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
