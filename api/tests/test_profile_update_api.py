from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from backend.models import AppUser, Profile


class TestUserProfile(APITestCase):
    """define Tests for user Profile"""
    @classmethod
    def setUpClass(cls):
        cls.email="testprofile@email.com"
        cls.passwd="@9everGiveup"
        user = AppUser.objects.create_user(
                username="testprofileuser",
                email=self.email,
                password=self.passwd,
                first_name="profilefirst",
                last_name="profilelast")
        user.is_active=True
        user.save()
        cls.user = user

        cls.login_url = reverse("api:token_obtain_pair")
        cls.profile_url = reverse("api:update_profile")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.obj_list = []

    def tearDown(self):
        for obj in self.obj_list:
            obj.delete()


    def test_profile_created(self):
        """test that user can request update

        If profile doesnt exist, It is created
        """

        # login the user
        response = self.client.post(
                self.login_url,
                data=dict(
                    email=self.email,
                    password=self.passwd))

        access_token = response.content.decode("utf-8").get("access")

        # get the initial profile anonymous user
        response = self.client.get(
                self.profile_url)

        self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST)
        
        self.client.credential(
                {
                    "HTTP_AUTHORIZATION":
                    f"Bearer {access_token}"
                })

        # get profile for auth user
        response = self.client.get(
                self.profile_url)

        self.assertEqual(
                response.status_code,
                status.HTTP_200_OK)

