from django.test import TestCase
from django.db import IntegrityError
from .models import University

class TestUniversity(TestCase):
    """Test for University"""

    def test_university_no_parameters(self):
        """Test that university raises Exception eith no arguments"""

        with self.assertRaisesMessage(
                IntegrityError,
                "backend_university_name_not_empty"):
            uni = University.objects.create()
