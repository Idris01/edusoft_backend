from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from backend.models import (
        AppUser, University, Department,
        Degree, Course)
from cities_light.models import Country, City

"""Test Module for the Course Model Api"""
class TestCourse(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        """ Setup general test requirements"""
        
        cls.obj_list = [] # collect object for cleanup
        # define admin user data
        cls.admin_email = "admin1@gmail.com"
        cls.admin_passwd = "@adminPas01"
        admin = AppUser.objects.create_user(
                email=cls.admin_email,
                password=cls.admin_passwd,
                username="admin1",
                first_name="adminfirstname",
                last_name="adminlastname",
                is_staff=True,
                is_superuser=True,
                is_active=True)

        cls.obj_list.append(admin)

        # define regular user data
        cls.user_email = "user1@gmail.com"
        cls.user_passwd = "@user1Passwd"
        user = AppUser.objects.create_user(
                email=cls.user_email,
                password=cls.user_passwd,
                username="userone",
                first_name="userfirstname",
                last_name="userlastname",
                is_active=True)

        cls.obj_list.append(user)

        # define Countries and Cities
        nigeria = Country.objects.get(code2__iexact="NG")
        osogbo = City.objects.get(name__iexact="Osogbo")
        uk = Country.objects.get(code2__iexact="gb")
        london  = City.objects.get(name__iexact="london")

        # define languages
        english, _ = Language.objects.get_or_create(name="English")
        youruba, _ = Language.objects.get_or_create(name="Yoruba")
        hausa, _ = Language.objects.get_or_create(name="Hausa")
        arabic, _ = Language.objects.get_or_create(name="Arabic")
        cls.obj_list.extend([english, yoruba, hausa, arabic])

        # define test universities

        uniosun = university.objects.create(
                name="osun state university",
                country=nigeria,
                city=osogbo,
                accomodation="on campus accomodation",
                history="founded in 2007",
                created_by=admin_user,
                postal_code="pmb 2000",
                languages=[english, yourba],
                website="https://www.uniosun.com")
        unilondon = university.objects.create(
                name="University of london",
                country=uk,
                city=london,
                accomodation="on campus accomodation",
                created_by=admin_user,
                history="founded in 1940",
                postal_code="pmb 7600",
                languages=[english, arabic],
                website="https://www.uniosun.com")
        cls.obj_list.extend([uniosun, unilondon])

        # create test department
        uniosun_science = Department.objects.create(
                name="Agricultural of Sciences",
                university=uniosun,
                about="Deals with science courses such as Agricultural Science")
        unilondon_medical = Department.objects.create(
                name="Medical studies",
                university=unilondon,
                about="General Medical studies such as Medicine,  Nursing")

        cls.obj_list.extend([uniosun_science, unilondon_medical])

        # create courses
        osun_animal = Course.objects.create(
                name="Animal Production and Health",
                department=uniosun_science,
                about="Study of Farm animal production and health")

        osun_crop = Course.objects.create(
                name="Crop Production",
                department=uniosun_science,
                about="Study of Crop Production")

        london_nursing = Course.objects.create(
                name="Nursing studies",
                department=unilondon_medical,
                about="Nursing and Midwifery")
        london_medical = Course.objects.create(
                name="Medical laboratory Science",
                department=unilondon_medical,
                about="Medical lab studies")
        london_medicine = Course.objects.create(
                name="General Medicine",
                department=unilondon_medical,
                about="General Studies in Medicine")
        cls.obj_list.extend([
            osun_animal, osun_crop,
            london_nursing, london_medical,
            london_medicine])

        # define the degrees for uniosun
        undergrad_crop = Degree.objects.create(
                name="Undergraduate",
                course=osun_animal,


    @classmethod
    def tearDownClass(cls):
        for obj in cls.obj_list:
            obj.delete()
