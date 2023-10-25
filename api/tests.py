from rest_framework.test import APITestCase
from backend.models import University, Language, AppUser
from cities_light.models import Country, City
from rest_framework import status
from django.urls import reverse
import json

"""DEfine tests for edusoft APIs"""


class TestUniversity(APITestCase):
    """Define tests for University"""

    @classmethod
    def tearDownClass(cls):
        """Cleanup the test data"""
        cls.test_user.delete()

    @classmethod
    def setUpClass(cls):
        """setup data for the whole test"""
        cls.url_name = "api:university_list_create"
        cls.url = reverse(cls.url_name)
        cls.test_password = "mypassword@1"
        cls.test_email = "idris@gmail.com"
        cls.test_username = "adeyemi"
        cls.university_data = dict(
            name="University Of Lagos",
            country="NG",
            history="founded 1980",
            postal_code="230210",
            languages=["English", "Arabic"],
            accomodation="On campus Accomodations for new students",
            city="lagos",
            website="https://www.lasu.com",
        )

        # create a test user for use when authentication is requied
        cls.test_user = AppUser.objects.create_user(
            email=cls.test_email,
            password=cls.test_password,
            username=cls.test_username,
            first_name="ade",
            last_name="idris",
        )
        cls.test_user.is_staff = True
        cls.test_user.save()

    def tearDown(self):
        for obj in self.obj_list:
            obj.delete()
        self.obj_list = []

    def setUp(self):
        """Create sample data for testing"""

        self.obj_list = []

        country = Country.objects.get(code2="NG")  # get country using country code2
        city = City.objects.get(country=country, name="Ogbomoso")
        self.obj_list.append(city)
        self.obj_list.append(country)
        university = University.objects.create(
            name="Ladoke Akintola University of Technology",
            history="Founded August 1990",
            country=country,
            accomodation="On-campus accomodation available",
            postal_code="210212",
            city=city,
            website="www.lautech.edu.ng",
        )

        self.obj_list.append(university)

        langs = ["Yoruba", "English", "Arabic"]
        for index, lang in enumerate(langs):
            langs[index] = Language(name=lang)
            langs[index].save()

        self.obj_list.extend(langs)
        university.languages.add(*langs)

    def test_university_list_ok(self):
        """test GET method on  /api/universities"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_university_post(self):
        """test POST method on /api/universities"""

        self.client.login(email=self.test_email, password=self.test_password)
        initial_count = University.objects.count()
        data = self.university_data
        response = self.client.post(self.url, data)
        if response.status_code == status.HTTP_201_CREATED:
            self.obj_list.append(University.objects.last())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(initial_count + 1, University.objects.count())
        response_data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(str(self.test_user.id), response_data.get("created_by", None))
