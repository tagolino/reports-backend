from django.urls import include, path

from .views import (
    TemplateView,
    TemplateDetailsView
)

urlpatterns = [
    path(
        "templates/",
        include(
            [
                path("", TemplateView.as_view()),
                path("<int:pk>/", TemplateDetailsView.as_view()),
            ]
        ),
    ),
]
