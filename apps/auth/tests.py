from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User

AUTH_PATH = "/api/v1/auth/token/"


class AuthorizationTestCase(APITestCase):
    def setUp(self):
        self.password = "7777777aA!"
        self.user = User.objects.create_user("test@user.com", self.password)

    def test_email_login(self):
        response = self.client.post(
            AUTH_PATH, {"email": self.user.email, "password": self.password}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.keys()), ["refresh", "access"])

    def test_wrong_email(self):
        response = self.client.post(
            AUTH_PATH, {"email": "wrong@user.com", "password": "1"}
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(list(response.data.keys()), ["detail"])

    def test_refresh_token(self):
        response = self.client.post(
            AUTH_PATH, {"email": self.user.email, "password": self.password}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.keys()), ["refresh", "access"])

        response = self.client.post(
            "/api/v1/auth/token/refresh/",
            {"refresh": response.data.get("refresh")},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.keys()), ["access"])

    def test_verify_token(self):
        response = self.client.post(
            AUTH_PATH, {"email": self.user.email, "password": self.password}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.keys()), ["refresh", "access"])

        response = self.client.post(
            "/api/v1/auth/token/verify/", {"token": response.data.get("access")}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
