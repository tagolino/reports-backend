from django.urls import include, path

from .views import (
    SupplierView,
    TemplateDetailsView,
    TemplateTypeView,
    TemplateView,
)

urlpatterns = [
    path(
        "suppliers/",
        include(
            [
                path("", SupplierView.as_view()),
            ]
        ),
    ),
    path(
        "templates/",
        include(
            [
                path("", TemplateView.as_view()),
                path("types/", TemplateTypeView.as_view()),
                path("<int:pk>/", TemplateDetailsView.as_view()),
            ]
        ),
    ),
]
