from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from common.tests.setup import create_user


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = create_user(
            username="admin", password="Admin@1234", is_admin=True
        )
        self.regular_user = create_user(
            username="user", password="User@1234", is_admin=False
        )
        self.client = APIClient()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_get_user_info_as_admin(self):
        self.authenticate(self.admin_user)
        response = self.client.get(reverse("user-info"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.admin_user.username)

    def test_get_user_info_as_regular_user(self):
        self.authenticate(self.regular_user)
        response = self.client.get(reverse("user-info"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.regular_user.username)
