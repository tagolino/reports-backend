from rest_framework import serializers

from .models import Document, DocumentDataFile, DocumentGenerationRequest


class DocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ("id", "name", "created_at")


class CreateDocumentSerializer(serializers.Serializer):
    name = serializers.CharField()
    data_file = serializers.FileField()
    template_id = serializers.IntegerField()
    is_production = serializers.BooleanField()


class DocumentDataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentDataFile
        fields = (
            "name",
            "created_at",
        )


class DocumentGenerationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentGenerationRequest
        fields = (
            "name",
            "created_at",
            "status",
            "error",
            "file",
        )


class DocumentDetailsSerializer(serializers.ModelSerializer):
    data_documents = DocumentDataFileSerializer(many=True)
    generated_documents = DocumentGenerationRequestSerializer(many=True)

    class Meta:
        model = Document
        fields = (
            "name",
            "created_at",
            "data_documents",
            "generated_documents",
        )
