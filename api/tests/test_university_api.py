from rest_framework.test import APITestCase
from backend.models import University, Language, AppUser, Department, Course
from cities_light.models import Country, City
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
import json
import uuid

"""DEfine tests for edusoft APIs"""


class TestUniversity(APITestCase):
    """Define tests for University"""

    @classmethod
    def tearDownClass(cls):
        """Cleanup the test data"""
        cls.test_user.delete()
        cls.app_user.delete()

    @classmethod
    def setUpClass(cls):
        """setup data for the whole test"""
        cls.url_name = "api:university_list_create"
        cls.url = reverse(cls.url_name)
        cls.test_password = "mypassword@1"
        cls.test_email = "idris01@gmail.com"
        cls.test_username = "adeyemi"
        cls.university_data = dict(
            name="University of UnitTesting",
            country="NG",
            history="founded 1980",
            postal_code="230210",
            languages=["English", "Arabic"],
            accomodation="On campus Accomodations for new students",
            city="lagos",
            website="https://www.lasu.com",
        )

        test_user = AppUser.objects.filter(email=cls.test_email)
        if test_user:
            test_user[0].delete()
        # create admin user
        cls.test_user = AppUser.objects.create_user(
            email=cls.test_email,
            password=cls.test_password,
            username=cls.test_username,
            first_name="ade",
            last_name="idris",
        )
        cls.test_user.is_staff = True
        cls.test_user.is_superuser = True
        cls.test_user.save()
        admin_token = RefreshToken.for_user(cls.test_user)
        cls.test_token = str(admin_token.access_token)

        # create  non-admin user
        cls.app_user_email = "idris01@yahoo.com"
        cls.app_user_passwd = "appUser1"

        app_user = AppUser.objects.filter(email=cls.app_user_email)

        # delete user if it already exist
        if app_user:
            app_user[0].delete()

        cls.app_user = AppUser.objects.create_user(
            email=cls.app_user_email,
            password=cls.app_user_passwd,
            username="ade",
            first_name="yemi",
            last_name="folohunso",
        )

        user_token = RefreshToken.for_user(cls.app_user)
        cls.app_token = str(user_token.access_token)

    def tearDown(self):
        for obj in self.obj_list:
            obj.delete()
        self.obj_list = []
        if self.client.login:
            self.client.logout()

    def setUp(self):
        """Create sample data for testing"""

        self.obj_list = []

        country = Country.objects.get(code2="NG")  # get country using country code2
        city, city_created = City.objects.get_or_create(country=country, name="Ogbomoso")
        if city_created:
            self.obj_list.append(city)
        university = University.objects.create(
            name="Lautech",
            history="Founded August 1990",
            country=country,
            accomodation="On-campus accomodation available",
            postal_code="210212",
            city=city,
            website="www.lautech.edu.ng",
        )

        self.obj_list.append(university)

        langs_name = ["Yoruba", "English", "Arabic"]
        langs = []
        for lang in langs_name:
            new_lang, is_created = Language.objects.get_or_create(name=lang.title())
            if is_created:
                langs.append(new_lang)

        self.obj_list.extend(langs)
        university.languages.add(*langs)

    def test_university_list_ok(self):
        """test GET method on  /api/universities"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_university_post(self):
        """test POST method on /api/universities"""

        self.client.login(email=self.test_email, password=self.test_password)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.test_token}")
        initial_count = University.objects.count()
        data = self.university_data
        response = self.client.post(self.url, data)
        if response.status_code == status.HTTP_201_CREATED:
            self.obj_list.append(University.objects.last())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(initial_count + 1, University.objects.count())
        response_data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(
            str(self.test_user.username), response_data.get("created_by", None)
        )

    def test_university_course_search(self):
        """Test filtering of University against Course"""

        country = Country.objects.get(code2="NG")  # get country using country code2
        city, city_created = City.objects.get_or_create(country=country, name="Ogbomoso")
        if city_created:
            self.obj_list.append(city)

        uni_count1 = University.objects.count()

        # Create the first University, with a department and a course
        uni1 = University.objects.create(
            name="Uni1",
            history="Founded August 1990",
            country=country,
            accomodation="On-campus accomodation available",
            postal_code="210212",
            city=city,
            website="www.uni1.edu.ng",
        )
        self.obj_list.append(uni1)
        dep1 = Department.objects.create(
            name="dep1", university=uni1, about="departement of dept1"
        )
        self.obj_list.append(dep1)
        course1 = Course.objects.create(
            name="Agricutltural Science",
            department=dep1,
            about="Study of Agricultural Science",
        )
        self.obj_list.append(course1)

        # create the second University, with a department and a course
        uni2 = University.objects.create(
            name="Uni2",
            history="Founded August 1990",
            country=country,
            accomodation="On-campus accomodation available",
            postal_code="210212",
            city=city,
            website="www.uni2.edu.ng",
        )
        self.obj_list.append(uni2)
        dep2 = Department.objects.create(
            name="dep2", university=uni2, about="departement of dept2"
        )
        self.obj_list.append(dep2)
        course2 = Course.objects.create(
            name="Software engineering",
            department=dep2,
            about="Study of Agricultural Science",
        )
        self.obj_list.append(course2)

        self.assertEqual(uni_count1 + 2, University.objects.count())

        resp = self.client.get(self.url + "?search=software")
        resp_data = json.loads(resp.content.decode("utf-8"))
        self.assertEqual(len(resp_data["results"]), 1)
        self.assertEqual(resp_data["results"][0]["name"], "Uni2")

    def test_university_update(self):
        """Test updating university attributes"""

        country = Country.objects.get(code2="GB")  # get country using country code2
        city, city_created = City.objects.get_or_create(country=country, name="London")
        if city_created:
            self.obj_list.append(city)

        # Create the first University, with a department and a course
        uni1 = University.objects.create(
            name="Uni1",
            history="Founded August 1990",
            country=country,
            accomodation="On-campus accomodation available",
            postal_code="210212",
            city=city,
            website="www.uni1.edu.ng",
            created_by=self.test_user,
        )

        new_data = dict(
            name=str(uuid.uuid4()).replace("-", "")[20],
            history="Founded August 1990",
            country="NG",
            accomodation="On-campus accomodation available",
            languages=["English", "Yoruba"],
            postal_code="210500",
            city="Lagos",
            website="https://www.unilag.edu.ng",
        )

        self.obj_list.append(uni1)

        url = reverse("api:university_detail", kwargs={"id": str(uni1.id)})

        # request from anonymous user
        response = self.client.put(url, new_data)
        self.assertIn(
            response.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED)
        )

        # request from non admin user
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.app_token}")
        response = self.client.put(url, new_data)
        self.assertIn(
            response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        )

        self.client.logout()

        # request from admin user
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.test_token}")
        response = self.client.put(url, new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(str(uni1.id), data.get("id"))
        self.assertEqual(data.get("name"), new_data["name"])
        self.assertEqual(data.get("country_code"), new_data["country"])
        self.assertEqual(data.get("city"), new_data["city"])
        self.assertEqual(data.get("postal_code"), new_data["postal_code"])
        self.assertEqual(data.get("website"), new_data["website"])
        self.assertEqual(data.get("history"), new_data["history"])
        self.assertEqual(sorted(data.get("languages")), sorted(new_data["languages"]))
        self.assertEqual(data.get("accomodation"), new_data["accomodation"])

        # test the get endpoint with Anonymous user
        self.client.logout()
        result = self.client.get(url)
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        # test delete endpoint with Anonymous user
        result = self.client.delete(url)
        self.assertIn(
            result.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        )

        # test delete endpoint with regular user
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.app_token}")

        result = self.client.delete(url)
        self.assertIn(
            result.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        )

        self.client.logout()

        # test delete endpoint with Admin user
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.test_token}")

        result = self.client.delete(url)
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)
