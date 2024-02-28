from django.urls import include, path

from .views import CustomerInvoiceView

urlpatterns = [
    path(
        "customers/",
        include(
            [
                path(
                    "<int:pk>/",
                    include(
                        [
                            path(
                                "invoices/",
                                include(
                                    [
                                        path("", CustomerInvoiceView.as_view()),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
]
