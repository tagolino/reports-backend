from rest_framework import serializers

from .models import Template, TemplateFile


class TemplateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ("id", "name", "type", "created_at")


class TemplateFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateFile
        fields = ("id", "name", "created_at", "created_at",
                  "version", "is_active")


class TemplateDetailsSerializer(serializers.ModelSerializer):
    template_files = TemplateFileSerializer(many=True)

    class Meta:
        model = Template
        fields = ("id", "name", "type", "created_at",
                  "country", "supplier", "template_files")


class CreateTemplateSerializer(serializers.Serializer):
    name = serializers.CharField()
    expression = serializers.CharField()
    file = serializers.FileField()
    is_active = serializers.BooleanField()
    type = serializers.CharField()
