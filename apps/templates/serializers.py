from rest_framework import serializers

from .models import Supplier, Template, TemplateFile


class SupplierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ("id", "name")


class TemplateListSerializer(serializers.ModelSerializer):
    supplier = SupplierListSerializer()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Template
        fields = ("id", "name", "type", "created_at", "supplier", "is_active")

    def get_is_active(self, instance):
        last_template_file = instance.template_files.last()

        if last_template_file:
            return last_template_file.is_active

        return False


class TemplateFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateFile
        fields = (
            "id",
            "name",
            "created_at",
            "created_at",
            "version",
            "is_active",
        )


class TemplateDetailsSerializer(serializers.ModelSerializer):
    template_files = TemplateFileSerializer(many=True)

    class Meta:
        model = Template
        fields = (
            "id",
            "name",
            "type",
            "created_at",
            "country",
            "supplier",
            "template_files",
        )


class CreateTemplateSerializer(serializers.Serializer):
    name = serializers.CharField()
    file = serializers.FileField()
    is_active = serializers.BooleanField()
    type = serializers.CharField()
