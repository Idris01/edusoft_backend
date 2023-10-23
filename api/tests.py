from rest_framework.test import APITestCase
from backend.models import University

"""DEfine tests for edusoft APIs"""


class TestUniversity(APITestCase):
    """Define tests for University"""

    def test_university_list(self):
        """test GET method on  /api/universities"""
        uni1 = University.objects.create(
            name="University of Nigeria", country="NG", state="Oyo"
        )
        self.assertEqual(uni1.name, "University of Nigeria")
