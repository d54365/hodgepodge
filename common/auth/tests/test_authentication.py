from unittest.mock import patch

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APITestCase, APIClient

from common.auth.authentication import JWTAuthentication
from user.models import User
from user.services import UserService


class JWTAuthenticationTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="Test@1234")
        self.auth = JWTAuthentication()

    def test_authenticate_no_user_id(self):
        response = self.client.get("/")
        request = response.wsgi_request
        with self.assertRaises(AuthenticationFailed) as cm:
            self.auth.authenticate(request)
        self.assertEqual(str(cm.exception.detail), "用户不存在")

    @patch.object(UserService, "get_user_by_id")
    def test_authenticate_user_exists(self, mock_get_user_by_id):
        mock_get_user_by_id.return_value = self.user
        response = self.client.get("/", **{"HTTP_X_USER_ID": str(self.user.id)})
        request = response.wsgi_request
        user, user_id = self.auth.authenticate(request)
        self.assertEqual(user, self.user)
        self.assertEqual(user_id, self.user.id)

    @patch.object(UserService, "get_user_by_id")
    def test_authenticate_user_does_not_exist(self, mock_get_user_by_id):
        mock_get_user_by_id.return_value = None
        response = self.client.get("/", **{"HTTP_X_USER_ID": "9999"})
        request = response.wsgi_request
        with self.assertRaises(AuthenticationFailed) as cm:
            self.auth.authenticate(request)
        self.assertEqual(str(cm.exception.detail), "用户不存在")

    @patch.object(UserService, "get_user_by_id")
    def test_get_user_exists(self, mock_get_user_by_id):
        mock_get_user_by_id.return_value = self.user
        user = self.auth.get_user(self.user.id)
        self.assertEqual(user, self.user)

    @patch.object(UserService, "get_user_by_id")
    def test_get_user_does_not_exist(self, mock_get_user_by_id):
        mock_get_user_by_id.return_value = None
        with self.assertRaises(AuthenticationFailed) as cm:
            self.auth.get_user(9999)
        self.assertEqual(str(cm.exception.detail), "用户不存在")
