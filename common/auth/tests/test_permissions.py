from rest_framework.test import APITestCase, APIRequestFactory

from common.auth.permissions import AdminPermission
from common.tests.setup import create_user


class AdminPermissionTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin_user = create_user(
            username="admin", password="Admin@1234", is_admin=True
        )
        self.regular_user = create_user(
            username="user", password="User@1234", is_admin=False
        )
        self.permission = AdminPermission()

    def test_admin_user_has_permission(self):
        request = self.factory.get("/")
        request.user = self.admin_user
        self.assertTrue(self.permission.has_permission(request, None))

    def test_regular_user_has_no_permission(self):
        request = self.factory.get("/")
        request.user = self.regular_user
        self.assertFalse(self.permission.has_permission(request, None))

    def test_unauthenticated_user_has_no_permission(self):
        request = self.factory.get("/")
        request.user = None
        self.assertFalse(self.permission.has_permission(request, None))
