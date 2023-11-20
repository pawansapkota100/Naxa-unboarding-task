from project_management.models import Project
from project_management.serializer import *
from rest_framework.response import Response
from project_management.models import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
import django_filters.rest_framework



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

# class based apiview
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
        user = request.user
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

# generics view
class DocumentView(generics.ListCreateAPIView):
    queryset= Document.objects.all()
    serializer_class= DocumentSerializer

class Documentedit(generics.RetrieveUpdateDestroyAPIView):
    queryset= Document.objects.all()
    serializer_class= DocumentSerializer
    lookup_field='id'

# To pass the all user or specific user
class UserView(APIView):
    def get(self, request, id=None, format=None):
        if id is not None:
            try:
                user = User.objects.get(id=id)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({'msg': 'User not found'})
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    

#  To filter the Document by the user who upload the document
# class DocumentFilter(generics.ListAPIView):
#     serializer_class = DocumentSerializer
#     def get_queryset(self):
#         queryset = Document.objects.all() 
#         username = self.request.query_params.get('user_id')
#         if username is not None:
#             queryset = queryset.filter(user=username)
#             return queryset
#         return queryset

# To filter the document based on the department
class DepartmentFilter(generics.ListAPIView):
    serializer_class= DocumentSerializer
    def get_queryset(self):
        queryset = Document.objects.all()
        department_id = self.request.query_params.get('department_id')
        project_id = Project.objects.filter(department=department_id)
        if department_id is not None:
            queryset= Document.objects.filter(project__id__in=project_id)
            return queryset
        return queryset
    

# Ordering filter based on upload_date on Document model 
from rest_framework import filters
class Userstats(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields= ['upload_date']


#  using django-filter in restframework
from django_filters import rest_framework as filters
class DocumentList(generics.ListAPIView):
    queryset= Document.objects.all()
    serializer_class= DocumentSerializer
    filter_backends= (filters.DjangoFilterBackend,)



# Adding a FilterSet with filter_fields
# filter project using user and department
class ProjectList(generics.ListAPIView):
    serializer_class= ProjectSerializer
    queryset= Project.objects.all()
    filter_backends= (filters.DjangoFilterBackend,)
    filterset_fields = ('user','department')


# 
# filtering document by department, by user ... by explictly specify in generics filtering
class DocumentFilter(filters.FilterSet):
    user= filters.CharFilter(field_name='user')
    department= filters.CharFilter(field_name='project__department__id')
    upload_date= filters.DateFilter(field_name='upload_date')
    class meta:
        model = Document
        field=['user','department','upload_date']

class Document(generics.ListAPIView):
    serializer_class= DocumentSerializer
    queryset= Document.objects.all()
    filter_backends= [filters.DjangoFilterBackend]
    filterset_class=DocumentFilter

from django.db.models import Count, F
class ProjectCount(generics.ListAPIView):
    serializer_class= ProjectCountSerializer
    def get_queryset(self):
       user=self.request.user.id
       month= self.request.query_params.get('month')
       query_set=Project.objects.annotate(month=F('start_date__month')).values('month').annotate(count=Count('month')).filter(user=user, start_date__month=month)
       return query_set
    #    query_set=Project.objects.filter(user= user, start_date__month=month).annotate(count=Count('name')).order_by('count')
    #    query_set=Project.objects.filter(user= user, start_date__month=month).annotate(count=Count('id')).order_by('-count')
    #    query_set=Project.objects.annotate(month=F('start_date__month')).values('month').annotate(count=Count('month')).order_by('-count').filter(user=user)
    #    query_set=Project.objects.filter(id=user,start_date__month=month ).annotate(count=Count('id'))
       
    
from datetime import timedelta,date  
class ProjectSummary(generics.ListAPIView):
    serializer_class = ProjectSerializer
    def get_queryset(self):
        project_id = self.request.query_params.get('num')
        query_set = Project.objects.annotate(deadline=F('start_date') + timedelta(days=30), manpower=Count('user')).filter(id=project_id)
        return query_set
    

class Summary(generics.ListAPIView):
    serializer_class=ProjectSerializer
    def get_queryset(self):
        department= self.request.query_params.get('department')
        manpower= self.request.query_params.get('manpower')
        # deadline= self.request.query_params.get('deadline')
        if department is not None and manpower is not None:
            query_set = Project.objects.annotate(deadline=F('start_date') + timedelta(days=30).strftime('%y-%m-%d'), manpower=Count('document__user')).filter(department=department,manpower=manpower)
            return query_set
        else:
            return Project.objects.none()
        






#        month= self.kwargs.get('month')
#        user= self.kwargs.get('user')
#        if user is not None and month is not None:
#         start_month=datetime(datetime.now().year,month,1)
#         end_month= datetime(datetime.now().year, month+1,1)
#         queryset= Project.objects.filter(start_date__gte= start_month, start_date__lt=end_month, user_id=user)
#         return queryset
#        else:
#            queryset= Project.objects.all()
#            return queryset


    

# class UserProjectStatsView(APIView):
#     def get(self, request, user_id):
#         user_project_stats = Project.objects.filter(user=user_id) \
#     .values('user__username', TruncMonth('start_date')) \
#     .annotate(projects_count=Count('id')) \
#     .order_by('user', 'start_date')


# class userstats(generics.ListAPIView):
#     serializer_class= ProjectSerializer
#     end_date = timezone.now()
#     start_date = end_date - timezone.timedelta(days=30)  # Assuming one month is 30 days
#     queryset = Project.objects.filter(
#         start_date__gte=start_date,
#         start_date__lte=end_date
#     ).values('user__id')\
#     .annotate(projects_count=Count('id'))



# class userstats(APIView):
#     def get(self, requst, id=None,format=None):
#         if requst.method=='GET':
#             if id is not None:
#                 queryset= Project.objects.filter(id=id)
#                 serializer_data= ProjectSerializer(queryset).data
#                 return Response(serializer_data)
#             queryset= Project.objects.all()
#             serializer_data= ProjectSerializer(queryset).data
#             return serializer_data

# from django.db.models.functions import TruncMonth
# from django.db.models import Count

# class userstats(generics.ListAPIView):
#     queryset=Document.objects.all().annotate(month=TruncMonth("upload_date")) .values("month").annotate(c=Count("id"))
#     def get_serializer_class(self):
#         return self.queryset
    

# class UserProjectList(generics.ListAPIView):
#     filter_backends= (filters.DjangoFilterBackend,)
#     filterset_fields = ('user')
