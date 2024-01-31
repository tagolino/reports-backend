from django.urls import include, path

from .views import DocumentDetailsView, DocumentView

urlpatterns = [
    path(
        "documents/",
        include(
            [
                path("", DocumentView.as_view()),
                path("<int:pk>/", DocumentDetailsView.as_view()),
            ]
        ),
    ),
]
