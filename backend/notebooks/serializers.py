from rest_framework import serializers
from .models import Document, Notebook


class NotebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notebook
        fields = [
            "id",
            "name",
            "owner",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
        ]

class AnswerSubmissionSerializer(serializers.Serializer):
    answer = serializers.CharField(max_length=255)

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id",
            "notebook",
            "title",
            "file",
            "file_type",
            "page_count",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "notebook",
            "page_count",
            "status",
            "created_at",
            "updated_at",
        ]