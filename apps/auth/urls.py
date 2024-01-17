from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path(
        "auth/",
        include(
            [
                path(
                    "token/",
                    include(
                        [
                            path("", TokenObtainPairView.as_view()),
                            path("refresh/", TokenRefreshView.as_view()),
                            path("verify/", TokenVerifyView.as_view()),
                        ]
                    ),
                ),
            ]
        ),
    ),
]
