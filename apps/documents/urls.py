from django.urls import include, path

from .views import (
    DataFileRequestDetailView,
    DataFileRequestView,
    DataFileXLSExportView,
    DocumentDetailsView,
    DocumentView,
)

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
    path(
        "data-file/",
        include(
            [
                path("", DataFileRequestView.as_view()),
                path(
                    "<int:pk>/",
                    include(
                        [
                            path("", DataFileRequestDetailView.as_view()),
                            path(
                                "export-xlsx/", DataFileXLSExportView.as_view()
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
]
