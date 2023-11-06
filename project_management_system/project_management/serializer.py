from rest_framework import serializers
from project_management.models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ['id','username','email','date_joined']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model= Project
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
     class Meta:
         model= Department
         fields= '__all__'
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Document
        fields= '__all__'
