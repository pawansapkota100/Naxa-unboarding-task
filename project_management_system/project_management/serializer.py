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
    deadline = serializers.DateTimeField()
    manpower = serializers.IntegerField()

    class Meta:
        model = Project
        fields = '__all__'

class ProjectCountSerializer(serializers.ModelSerializer):
    count=serializers.IntegerField()
    month= serializers.IntegerField()
    class Meta:
        model= Project
        fields=['month','count']
    

class UserSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True, source='project_set')   
    class Meta:
        model = User
        fields = ['id', 'username', 'projects']

from .models import ProjectSite

class ProjectSiteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSite
        fields = ['site', 'site_coordinates', 'site_area', 'way_to_home']
