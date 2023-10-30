"""Define tests for the User Model"""
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from backend.models import AppUser


class AppUserTest(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.registration_url = reverse("api:user_list_create")
    

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):

        # create a list to hold all created data
        self.obj_list = []

    def tearDown(self):

        # delete all created data
        for obj in self.obj_list:
            obj.delete()

    def test_create_user(self):
        """Test new user created successfully"""
        email="teste1@gmail.com"
        password="@iWill9evergiveUp"

        print(self.client.logout())
        data = dict(
                username="Tester1",
                email=email,
                first_name="test",
                last_name="user",
                password=password,
                confirm_password="@iWill9evergiveUp")
        response = self.client.post(
                self.registration_url,
                data=data)
        user = AppUser.objects.filter(email=email)
        if user:
            self.obj_list.append(user)

        print(response.content.decode("utf-8"))
        self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED)
