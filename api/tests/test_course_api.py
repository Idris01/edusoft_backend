from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from backend.models import AppUser, University, Department, Language, Degree, Course
from cities_light.models import Country, City
import json


"""Test Module for the Course Model Api"""


class TestCourse(APITestCase):
    @classmethod
    def setUpClass(cls):
        """Setup general test requirements"""
        cls.course_url = reverse("api:course_list")
        cls.obj_list = []  # collect object for cleanup
        # define admin user data
        cls.admin_email = "admin1@gmail.com"
        cls.admin_passwd = "@adminPas01"

        old_admin = AppUser.objects.filter(email=cls.admin_email)
        if old_admin:
            old_admin[0].delete()

        admin = AppUser.objects.create_user(
            email=cls.admin_email,
            password=cls.admin_passwd,
            username="admin1",
            first_name="adminfirstname",
            last_name="adminlastname",
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        cls.obj_list.append(admin)

        # define regular user data
        cls.user_email = "user1@gmail.com"
        cls.user_passwd = "@user1Passwd"

        old_user = AppUser.objects.filter(email=cls.user_email)
        if old_user:
            old_user[0].delete()

        user = AppUser.objects.create_user(
            email=cls.user_email,
            password=cls.user_passwd,
            username="userone",
            first_name="userfirstname",
            last_name="userlastname",
            is_active=True,
        )

        cls.obj_list.append(user)

        # define Countries and Cities
        nigeria = Country.objects.get(code2__iexact="NG")
        osogbo = City.objects.get(name__iexact="Osogbo")
        uk = Country.objects.get(code2__iexact="gb")
        london = City.objects.get(name__iexact="london")

        # define languages
        english, _ = Language.objects.get_or_create(name="English")
        yoruba, _ = Language.objects.get_or_create(name="Yoruba")
        hausa, _ = Language.objects.get_or_create(name="Hausa")
        arabic, _ = Language.objects.get_or_create(name="Arabic")
        cls.obj_list.extend([english, yoruba, hausa, arabic])

        # define test universities
        uniosun = University.objects.create(
            name="osun state university",
            country=nigeria,
            city=osogbo,
            accomodation="on campus accomodation",
            history="founded in 2007",
            created_by=admin,
            postal_code="pmb 2000",
            website="https://www.uniosun.com",
        )

        uniosun.languages.set([english, yoruba])

        unilondon = University.objects.create(
            name="University of london",
            country=uk,
            city=london,
            accomodation="on campus accomodation",
            created_by=admin,
            history="founded in 1940",
            postal_code="pmb 7600",
            website="https://www.uniosun.com",
        )

        unilondon.languages.set([english, arabic])

        cls.obj_list.extend([uniosun, unilondon])

        # create test department
        uniosun_science = Department.objects.create(
            name="Agricultural of Sciences",
            university=uniosun,
            about="Deals with science courses such as Agricultural Science",
        )
        unilondon_medical = Department.objects.create(
            name="Medical studies",
            university=unilondon,
            about="General Medical studies such as Medicine,  Nursing",
        )

        cls.obj_list.extend([uniosun_science, unilondon_medical])

        # create courses
        osun_animal = Course.objects.create(
            name="Animal Production and Health",
            department=uniosun_science,
            about="Study of Farm animal production and health",
        )

        osun_crop = Course.objects.create(
            name="Crop Production",
            department=uniosun_science,
            about="Study of Crop Production",
        )

        london_nursing = Course.objects.create(
            name="Nursing studies",
            department=unilondon_medical,
            about="Nursing and Midwifery",
        )
        london_medical = Course.objects.create(
            name="Medical laboratory Science",
            department=unilondon_medical,
            about="Medical lab studies",
        )
        london_medicine = Course.objects.create(
            name="General Medicine",
            department=unilondon_medical,
            about="General Studies in Medicine",
        )
        cls.obj_list.extend(
            [osun_animal, osun_crop, london_nursing, london_medical, london_medicine]
        )

        # delete old degrees
        old_degrees = Degree.objects.all()
        for deg in old_degrees:
            deg.delete()

        # define the degrees for uniosun
        undergrad_crop = Degree.objects.create(
            name="Undergraduate",
            course=osun_crop,
            about="This is a 4 year undergraduate Degree",
        )
        undergrad_animal = Degree.objects.create(
            name="Undergraduate",
            course=osun_animal,
            about="This is a 5 years undergraduate Degree",
        )
        master_crop = Degree.objects.create(
            name="Masters", course=osun_crop, about="This is a 2 years Masters Degree"
        )

        cls.obj_list.extend([undergrad_crop, undergrad_animal, master_crop])

        # define the degrees for unilondon
        undergrad_nursing = Degree.objects.create(
            name="undergraduate",
            course=london_nursing,
            about="This is a 3 years Nursing Degree",
        )
        undergrad_medical = Degree.objects.create(
            name="undergraduate",
            course=london_medical,
            about="This is a 4 years Medical Undergraduate Degree",
        )
        cls.obj_list.extend([undergrad_nursing, undergrad_medical])

    @classmethod
    def tearDownClass(cls):
        for obj in cls.obj_list:
            obj.delete()

    def test_course_url_available(self):
        """Test that the course fetching url is available"""
        response = self.client.get(self.course_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(data.get("count"), 5)

    def test_course_contain_required_data(self):
        """Test that the name of university is present in the course data"""
        response = self.client.get(self.course_url)
        data = json.loads(response.content.decode("utf-8"))

        course = data.get("results", [None])[0]  # get a single course
        self.assertIn("university", course)
        self.assertIn("university_id", course)
        self.assertIn("department", course)
        self.assertIn("department_id", course)

    def test_course_search_on_course_name(self):
        """test search for given course name"""
        search_url = "{}?search={}".format(
                self.course_url, "nursing")

        response = self.client.get(search_url)
        search_data = json.loads(response.content.decode("utf-8"))

        # only one course has Nursing contained in its name
        self.assertEqual(search_data.get("count"),1)
