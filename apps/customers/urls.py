from django.urls import include, path
from sources.customer_portal.views import (
    AccountHolderListView as CustomerPortalAccountHolderListView,
)
from sources.customer_portal.views import (
    AssetListView as CustomerPortalAssetListView,
)
from sources.customer_portal.views import (
    CustomerListView as CustomerPortalCustomerListView,
)
from sources.customer_portal.views import (
    ElectricityContractListView as CustomerPortalElectricityContractListView,
)
from sources.customer_portal.views import (
    ElectricityCustomerAccountListView as CustomerPortalECAListView,
)
from sources.customer_portal.views import (
    MPANListView as CustomerPortalMPANListView,
)

urlpatterns = [
    path(
        "cp/",
        include(
            [
                path("customers/", CustomerPortalCustomerListView.as_view()),
                path(
                    "electricity-customer-accounts/",
                    CustomerPortalECAListView.as_view(),
                ),
                path(
                    "account-holders/",
                    CustomerPortalAccountHolderListView.as_view(),
                ),
                path(
                    "contracts/",
                    CustomerPortalElectricityContractListView.as_view(),
                ),
                path(
                    "sites/",
                    CustomerPortalAssetListView.as_view(),
                ),
                path(
                    "mpans/",
                    CustomerPortalMPANListView.as_view(),
                ),
            ]
        ),
    ),
]
