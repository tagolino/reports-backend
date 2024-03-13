from django.db.models import Q
from rest_framework.generics import ListAPIView

from .filters import (
    CustomerPortalAccountHolderFilters,
    CustomerPortalAssetFilters,
    CustomerPortalECAFilters,
    CustomerPortalElectricityContractFilters,
    CustomerPortalMpanFilters,
)
from .models import (
    CustomerPortalAccountHolder,
    CustomerPortalAsset,
    CustomerPortalCustomer,
    CustomerPortalECA,
    CustomerPortalElectricityContract,
    CustomerPortalMpan,
)
from .serializers import (
    AccountHolderSerializer,
    AssetSerializer,
    CustomerSerializer,
    ElectricityContractSerializer,
    ElectricityCustomerAccountSerializer,
    MPANSerializer,
)


class CustomerListView(ListAPIView):
    queryset = CustomerPortalCustomer.objects.all()
    serializer_class = CustomerSerializer


class AccountHolderListView(ListAPIView):
    queryset = CustomerPortalAccountHolder.objects.all()
    filterset_class = CustomerPortalAccountHolderFilters
    serializer_class = AccountHolderSerializer


class ElectricityCustomerAccountListView(ListAPIView):
    queryset = CustomerPortalECA.objects.all()
    filterset_class = CustomerPortalECAFilters
    serializer_class = ElectricityCustomerAccountSerializer


class ElectricityContractListView(ListAPIView):
    queryset = CustomerPortalElectricityContract.objects.exclude(
        Q(name__isnull=True) | Q(name="")
    )
    filterset_class = CustomerPortalElectricityContractFilters
    serializer_class = ElectricityContractSerializer


class AssetListView(ListAPIView):
    queryset = CustomerPortalAsset.objects.all()
    filterset_class = CustomerPortalAssetFilters
    serializer_class = AssetSerializer


class MPANListView(ListAPIView):
    queryset = CustomerPortalMpan.objects.all()
    filterset_class = CustomerPortalMpanFilters
    serializer_class = MPANSerializer
