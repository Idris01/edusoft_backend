"""Define tests for the User Model"""
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from backend.models import AppUser
import json


class AppUserTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.registration_url = reverse("api:user_list_create")
        cls.url_name = "api:university_list_create"
        cls.url = reverse(cls.url_name)
        cls.test_password = "mypassword@1"
        cls.test_email = "idris01@gmail.com"
        cls.test_username = "adeyemi"
        user1 = AppUser.objects.filter(email=cls.test_email)
        if user1:
            user1.delete()
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

        # create  non-admin user
        cls.app_user_email = "idris01@yahoo.com"
        cls.app_user_passwd = "appUser1"

        user2 = AppUser.objects.filter(email=cls.app_user_email)
        if user2:
            user2.delete()

        cls.app_user = AppUser.objects.create_user(
            email=cls.app_user_email,
            password=cls.app_user_passwd,
            username="ade",
            first_name="yemi",
            last_name="folohunso",
        )

    @classmethod
    def tearDownClass(cls):
        cls.test_user.delete()
        cls.app_user.delete()

    def setUp(self):

        # create a list to hold all created data
        self.obj_list = []

    def tearDown(self):

        # delete all created data
        for obj in self.obj_list:
            obj.delete()

    def test_create_user(self):
        """Test new user created successfully"""
        email = "teste1@gmail.com"
        password = "@iWill9evergiveUp"

        user_count = AppUser.objects.count()

        data = dict(
            username="Tester1",
            email=email,
            is_staff=True,
            first_name="test",
            last_name="user",
            password=password,
            confirm_password="@iWill9evergiveUp",
        )

        data["confirm_password"] = "iWill9evergiveUP"
        response = self.client.post(self.registration_url, data=data)
        user = AppUser.objects.filter(email=email)
        if user:
            self.obj_list.append(user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "password mismatch",
            json.loads(response.content.decode("utf-8"))["password"][0].lower(),
        )

        data["confirm_password"] = "never"
        data["password"] = "never"

        response = self.client.post(self.registration_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "password too short",
            json.loads(response.content.decode("utf-8"))["password"][0].lower(),
        )

        data["confirm_password"] = "donot giveup"
        data["password"] = "donot giveup"

        response = self.client.post(self.registration_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "password must not include space",
            json.loads(response.content.decode("utf-8"))["password"][0].lower(),
        )

        data["confirm_password"] = "nevergiveup"
        data["password"] = "nevergiveup"

        response = self.client.post(self.registration_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "password must have lower and uppercase, number and special char",
            json.loads(response.content.decode("utf-8"))["password"][0].lower(),
        )

        data["confirm_password"] = "nevergiveUp"
        data["password"] = "nevergiveUp"

        response = self.client.post(self.registration_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "password must have lower and uppercase, number and special char",
            json.loads(response.content.decode("utf-8"))["password"][0].lower(),
        )

        data["confirm_password"] = "9evergiveUp"
        data["password"] = "9evergiveUp"

        response = self.client.post(self.registration_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "password must have lower and uppercase, number and special char",
            json.loads(response.content.decode("utf-8"))["password"][0].lower(),
        )

        data["confirm_password"] = "@9evergiveUp"
        data["password"] = "@9evergiveUp"

        response = self.client.post(self.registration_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIn(
                "registration successfull",
                response_data.get("message", []))

        # confirm the user is indeed created
        self.assertEqual(
                user_count + 1,
                AppUser.objects.count())

    def test_create_user_missing_requirements(self):
        """Test new user created successfully"""
        email = "teste1@gmail.com"
        password = "@iWill9evergiveUp"

        data = dict(
            username="Tester1",
            first_name="test",
            password=password,
            confirm_password=password,
        )

        response = self.client.post(self.registration_url, data=data)
        user = AppUser.objects.filter(email=email)
        if user:
            self.obj_list.append(user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = dict(
            username="Tester1",
            first_name="test",
            last_name="tester",
            password=password,
            confirm_password=password,
        )

        response = self.client.post(self.registration_url, data=data)
        user = AppUser.objects.filter(email=email)
        if user:
            self.obj_list.append(user)

        resp_data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", list(resp_data.keys()))

    def test_list_only_by_admin(self):
        """Test that only admin can fetch all user data"""
        self.client.login(email=self.app_user_email, password=self.app_user_passwd)
        response = self.client.get(self.registration_url)
        self.assertIn(
            response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        )
        self.client.logout()
        self.client.login(email=self.test_email, password=self.test_password)
        response = self.client.get(self.registration_url)
        self.assertTrue(response.status_code, status.HTTP_200_OK)
