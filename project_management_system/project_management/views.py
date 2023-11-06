from project_management.models import Project
from project_management.serializer import *
from rest_framework.response import Response
from project_management.models import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets

@api_view(['GET','POST','PUT','DELETE'])
def ProjectView(request,id=None):
    if request.method == 'GET':
        if id is not None:
            try:
                queryset= Project.objects.get(id=id)
                serializer= ProjectSerializer(queryset)
                return Response(serializer.data)
            except:
                return Response({'msg':'Enter valid id'})
        try:
            queryset= Project.objects.all()
            serializer= ProjectSerializer(queryset,many=True)
            return Response(serializer.data)
        except:
            return Response({'msg':'Data not found'})
    elif request.method == 'POST':
        serializer= ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'your data has been updated'})
        return Response({'msg':'error'})

    elif request.method == 'PUT':
        try:
            project = Project.objects.get(id=id)
        except Project.DoesNotExist:
            return Response({'msg': 'Project not found'})

        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Your data has been updated'})
        return Response({'msg':'Fail to update data'})

    elif request.method == 'DELETE':
        try:
            project = Project.objects.get(id=id)
            project.delete()
            return Response({'msg': 'Your data has been deleted'})
        except:
            return Response({'msg': 'Project not found'})




class DepartmentView(APIView):
    def get(self, request, id=None, format=None):
        if id is not None:
            try:
                department= Department.department_object.get(id=id)
                serializer= DepartmentSerializer(department)
                return Response(serializer.data)
            except:
                return Response({'msg':'fail to obtain data'})
        project= Department.department_object.all()
        serializer= DepartmentSerializer(project, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        department= request.data
        serializer= DepartmentSerializer(data=department)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Department data has been post'})
        return Response({'msg':'Fail to post the data'})

    def put(self, request, id, format=None):
        try:
            department=Department.department_object.get(id=id)
            serializer=DepartmentSerializer(department, data= request.data)
        except:
            return Response({"fail to obtain data"})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Department data has been updated'})
        return Response({'msg':'Department data is fail to update'})

    def delete(self, request, id , format=None):
        try:
            department= Department.department_object.get(id=id)
        except:
            return Response({'msg':'fail to obtain data'})
        try:
            department.delete()
            return Response({'msg':'Data has been deleted'})
        except:
            return Response({'msg':'Failed to delete the data'})

class DocumentView(generics.ListCreateAPIView):
    queryset= Document.objects.all()
    serializer_class= DocumentSerializer

class Documentedit(generics.RetrieveUpdateDestroyAPIView):
    queryset= Document.objects.all()
    serializer_class= DocumentSerializer
    lookup_field='id'


class Userview(viewsets.ModelViewSet):
    queryset= User.objects.all()
    serializer_class= UserSerializer
