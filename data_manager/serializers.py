# serializers.py
from rest_framework import serializers
from .models import DataFile

class DataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataFile
        fields = ['id', 'file', 'uploaded_by', 'uploaded_at', 'validated', 'version', 'description']
        read_only_fields = ['uploaded_by', 'uploaded_at', 'validated', 'version']