from django.urls import include, path

from .views import InvoiceExportXLSView, InvoicesView, InvoiceView

urlpatterns = [
    path(
        "invoices/",
        include(
            [
                path("", InvoicesView.as_view()),
                path(
                    "<int:pk>/",
                    include(
                        [
                            path("", InvoiceView.as_view()),
                            path(
                                "export-xlsx/", InvoiceExportXLSView.as_view()
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
]
