from rest_framework.test import APITestCase
from backend.models import University, Language
from cities_light.models import Country, City
from rest_framework import status
from django.urls import reverse
import os
import shutil
import sys
from time import sleep
from pathlib import Path

"""DEfine tests for edusoft APIs"""

test_db_name="test_db.sqlite3"
db_name="db.sqlite3"

class TestUniversity(APITestCase):
    """Define tests for University"""
    @classmethod
    def tearDownClass(cls):
        pass

    @classmethod
    def setUpClass(cls):
        """setup data for the whole test"""
        if not Path(test_db_name).exists():
            print(f"{test_db_name} required but not found")
            print("do cp {} {}, to co create one".format(
                db_name, test_db_name))
            sys.exit(1)
        cls.url_name = "api:university_list_create"
        cls.url = reverse(cls.url_name)

    def tearDown(self):
        for obj in self.obj_list:
            obj.delete()
        self.obj_list = []

    def setUp(self):
        """Create sample data for testing"""
        
        self.obj_list = []

        country = Country.objects.get(code2="NG")  # get country using country code2
        city = City.objects.get(
                country=country,
                name="Ogbomoso")
        self.obj_list.append(city)
        self.obj_list.append(country)
        university = University.objects.create(
            name="Ladoke Akintola University of Technology",
            history="Founded August 1990",
            country=country,
            accomodation="On-campus accomodation available",
            postal_code="210212",
            city=city,
            website="www.lautech.edu.ng"
        )

        self.obj_list.append(university)

        langs = ["Yoruba", "English", "Arabic"]
        for index, lang in enumerate(langs):
            langs[index]=Language(name=lang)
            langs[index].save()

        self.obj_list.extend(langs)
        university.languages.add(*langs)

    def test_university_list_ok(self):
        """test GET method on  /api/universities"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_university_post(self):
        """test POST method on /api/universities"""
        data = dict(
                name="University Of Lagos",
                country="NG",
                history="founded 1980",
                postal_code="230210",
                languages= ["English","Arabic"],
                accomodation="On campus Accomodations for new students",
                city="lagos",
                website="https://www.lasu.com")
        response = self.client.post(self.url,data)
        if response.status_code == status.HTTP_201_CREATED:
            self.obj_list.append(
                    University.objects.all()[-1]
                    )
        print(response.content.decode("utf-8"))
        self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED)
        
