from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from backend.models import AppUser
import json


class TestUserProfile(APITestCase):
    """define Tests for user Profile"""

    @classmethod
    def setUpClass(cls):
        cls.email = "testprofile@email.com"
        cls.passwd = "@9everGiveup"
        user = AppUser.objects.filter(email=cls.email)
        if user:  # remove existing user
            user[0].delete()

        user = AppUser.objects.create_user(
            username="testprofileuser",
            email=cls.email,
            password=cls.passwd,
            first_name="profilefirst",
            last_name="profilelast",
        )
        user.is_active = True
        user.save()
        cls.user = user

        cls.login_url = reverse("api:token_obtain_pair")
        cls.profile_url = reverse("api:profile_detail")

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
            self.login_url, data=dict(email=self.email, password=self.passwd)
        )

        access_token = json.loads(response.content.decode("utf-8")).get("access")

        # get the initial profile anonymous user
        response = self.client.get(self.profile_url)

        self.assertIn(
            response.status_code,
            (
                status.HTTP_400_BAD_REQUEST,
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ),
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # get profile for auth user
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile(self):
        response = self.client.post(
            self.login_url, data=dict(email=self.email, password=self.passwd)
        )

        access_token = json.loads(response.content.decode("utf-8")).get("access")
        address = "No 12, Olukoko Street Ogbomoso Oyo state"
        dob = "1990-08-18"
        country = "NG"
        gender = "male"
        profile_data = dict(address=address, date_of_birth=dob, nationality=country)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # attempt to update without gender
        response = self.client.put(self.profile_url, data=profile_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = json.loads(response.content.decode("utf-8"))
        self.assertIn("gender", list(data.keys()))

        # add gender field
        profile_data["gender"] = gender

        # make request with all required fields
        response = self.client.put(self.profile_url, data=profile_data)
        data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
