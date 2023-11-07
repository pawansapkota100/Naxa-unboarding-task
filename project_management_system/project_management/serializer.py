from rest_framework import serializers
from project_management.models import Project, Department, Document
from django.contrib.auth.models import User

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    document = DocumentSerializer(many=True, read_only=True, source='document_set')
    class Meta:
        model = Project
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True, source='project_set')   
    class Meta:
        model = User
        fields = ['id', 'username', 'projects']
