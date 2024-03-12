from rest_framework import serializers

from .models import (
    CustomerPortalAccountHolder,
    CustomerPortalAsset,
    CustomerPortalCustomer,
    CustomerPortalECA,
    CustomerPortalElectricityContract,
    CustomerPortalMpan,
)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPortalCustomer
        fields = (
            "id",
            "name",
        )


class AccountHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPortalAccountHolder
        fields = (
            "id",
            "name",
        )


class ElectricityCustomerAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPortalECA
        fields = (
            "id",
            "name",
        )


class ElectricityContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPortalElectricityContract
        fields = (
            "id",
            "name",
        )


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPortalAsset
        fields = (
            "id",
            "name",
        )


class MPANSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPortalMpan
        fields = (
            "id",
            "mpan",
        )
