from django.db.models import Q
from rest_framework.generics import ListAPIView

from .filters import (
    CustomerPortalAccountHolderFilters,
    CustomerPortalECAFilters,
    CustomerPortalElectricityContractFilters,
)
from .models import (
    CustomerPortalAccountHolder,
    CustomerPortalCustomer,
    CustomerPortalECA,
    CustomerPortalElectricityContract,
)
from .serializers import (
    AccountHolderSerializer,
    CustomerSerializer,
    ElectricityContractSerializer,
    ElectricityCustomerAccountSerializer,
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
