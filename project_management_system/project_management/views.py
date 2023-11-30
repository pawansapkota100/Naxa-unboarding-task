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
            query_set = Project.objects.annotate(deadline=F('start_date') + timedelta(days=30), manpower=Count('document__user')).filter(department=department,manpower=manpower)
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



# from django.core.management.base import BaseCommand
# from django.contrib.gis.utils import LayerMapping
# from project_management.models import ProjectSite


# from django.views import View


# class ExportView(View):
#     def get(self, request, *args, **kwargs):
#         # Define the mapping between model fields and shapefile geometry types
#         mapping = {
#             'site_coordinates': 'POINT',
#             'site_area': 'POLYGON',
#             'way_to_home': 'LINESTRING',
#         }

#         # Create a LayerMapping instance, specifying the model, output shapefile path, and mapping
#         lm = LayerMapping(ProjectSite, 'project_management/files/shapefile .shp', mapping)

#         # Save the data to the shapefile, with strict and verbose options
#         lm.save(verbose=True)

#         # Optionally, you can also call the management command directly
#         # call_command('export_command')

    

# from django.http import HttpResponse
# from rest_framework import generics
# import geopandas as gpd
# from shapely.geometry import Point, LineString, shape
# import json
# import os
# import shutil
# import tempfile
# from .models import ProjectSite
# from project_management.serializer import ProjectSiteListSerializer

# class ExportProjectSiteDataView(generics.ListAPIView):
#     """
#     This class exports all the project sites geospatial data into a shapefile.
#     """

#     serializer_class = ProjectSiteListSerializer
#     queryset = site_coordinates.objects.all()

#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         data_points = []

#         for project_site in queryset:
#             site_name = project_site.site
#             feature = {"site": site_name}  # Initialize feature dictionary

#             # Check and add site_coordinates
#             if project_site.site_coordinates:
#                 feature["geometry"] = Point(project_site.site_coordinates)

#             # Check and add site_area
#             elif project_site.site_area:
#                 feature["geometry"] = shape(json.loads(project_site.site_area.geojson))

#             # Check and add way_to_home
#             elif project_site.way_to_home:
#                 feature["geometry"] = LineString(project_site.way_to_home)

#             # Only add features with valid geometries
#             if "geometry" in feature:
#                 if feature["geometry"].is_empty:
#                     continue
#                 data_points.append(feature)

#         temp_dir = tempfile.mkdtemp()
#         shapefile_base = "project-site-geodata"
#         shapefile_path_base = os.path.join(temp_dir, shapefile_base)

#         try:
#             os.makedirs(shapefile_path_base, exist_ok=True)
#         except OSError as e:
#             print(f"Error in creating dirs in temp dirs: {e}")

#         # Create GeoDataFrame from the list of features
#         gdf_points = gpd.GeoDataFrame(data_points, geometry="geometry", crs="EPSG:4326")

#         # Export GeoDataFrame to a Shapefile
#         gdf_points.to_file(os.path.join(shapefile_path_base, f"{shapefile_base}.shp"), driver="ESRI Shapefile")

#         # Create a ZIP file containing the Shapefile
#         shutil.make_archive(shapefile_path_base, "zip", temp_dir, shapefile_base)

#         # Prepare the response with the ZIP file
#         with open(f"{shapefile_path_base}.zip", "rb") as zip_file:
#             response = HttpResponse(zip_file.read(), content_type="application/zip")
#             response["Content-Disposition"] = f"attachment; filename={shapefile_base}.zip"

#         # Clean up temporary directory
#         shutil.rmtree(temp_dir)

#         return response


from django.http import HttpResponse
from rest_framework import generics
import geopandas as gpd
from shapely.geometry import Point, LineString, shape
import json
import os
import shutil
import tempfile
from .models import ProjectSite
from project_management.serializer import ProjectSiteListSerializer
class ExportData(generics.ListAPIView):
    """
    This class export all the project sites geospatial data into shapefile.
    """

    serializer_class = ProjectSiteListSerializer
    queryset = ProjectSite.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data_points = []
        data_areas = []
        data_ways = []
        for project_site in queryset:
            if project_site.site_coordinates:
                point_geometry = Point(project_site.site_coordinates)
                points = {"geometry": point_geometry}
                data_points.append(points)

            if project_site.site_area:
                area_geometry = shape(json.loads(project_site.site_area.geojson))
                areas = { "geometry": area_geometry}
                data_areas.append(areas)

            if project_site.way_to_home:
                way_geometry = LineString(project_site.way_to_home)
                ways = { "geometry": way_geometry}
                data_ways.append(ways)
        temp_dir = tempfile.mkdtemp()
        shapefile_base = "project-site-geodata"
        shapefile_path_base = os.path.join(temp_dir, shapefile_base)
        shapefile_name_points = "project-site-points"
        shapefile_name_areas = "project-site-areas"
        shapefile_name_ways = "project-site-ways"
        shapefile_path_points = os.path.join(shapefile_path_base, shapefile_name_points)
        shapefile_path_areas = os.path.join(shapefile_path_base, shapefile_name_areas)
        shapefile_path_ways = os.path.join(shapefile_path_base, shapefile_name_ways)
        try:
            os.makedirs(shapefile_path_points, exist_ok=True)
            os.makedirs(shapefile_path_areas, exist_ok=True)
            os.makedirs(shapefile_path_ways, exist_ok=True)
        except OSError as e:
            print(f"Error in creating dirs in temp dirs: {e}")
        gdf_points = gpd.GeoDataFrame(data_points, geometry="geometry")
        gdf_points.to_file(shapefile_path_points, driver="ESRI Shapefile")

        gdf_areas = gpd.GeoDataFrame(data_areas, geometry="geometry")
        gdf_areas.to_file(shapefile_path_areas, driver="ESRI Shapefile")

        gdf_ways = gpd.GeoDataFrame(data_ways, geometry="geometry")
        gdf_ways.to_file(shapefile_path_ways, driver="ESRI Shapefile")

        shutil.make_archive(shapefile_path_base, "zip", temp_dir, shapefile_base)

        with open(f"{shapefile_path_base}.zip", "rb") as zip_file:
            response = HttpResponse(zip_file.read(), content_type="application/zip")
            response[
                "Content-Disposition"
            ] = f"attachment; filename={shapefile_base}.zip"

        shutil.rmtree(temp_dir)
        return response




# from osgeo import ogr
# import os



# class AlternativeExport(generics.ListAPIView):
#     queryset= ProjectSite.objects.all()
#     serializer_class= ProjectSiteListSerializer
#     gdf=gpd.GeoDataFrame({
#             'site_coordinate':[site.site_coordinates for site in queryset],
#             'site_line':[site.way_to_home for site in queryset],
#             'site_area':[site.site_area for site in queryset]

#         },geometry="geometry")
#     gdf.to_file('project_sites_export.shp', driver='ESRI Shapefile')




# import geopandas as gpd

# class ExportData(generics.ListAPIView):
#     serializer_class= ProjectSiteListSerializer
#     queryset= ProjectSite.objects.all()
#     def export_to_shapefile(self, queryset,filename='exported_data.shp'):
#         gdf = gpd.GeoDataFrame(queryset)
#         gdf.to_file(filename, driver='ESRI Shapefile')
    
#     point = ProjectSite.objects.values('site_coordinates')
#     point= gpd.GeoDataFrame(ProjectSite.objects.values('site_coordinates'))
#     # polygon= ProjectSite.objects.values('site_area')
#     # path= ProjectSite.objects.values('way_to_home')






class ProjectCountListApi(APIView):

    def get(self, request, *args, **kwargs):
        weekly_project_counts = {}
        current_year = date.today().year
        for month in range(1, 13):
            first_day_of_month = date(current_year, month, 1)
            for week in range(1, 6):
                start_date = first_day_of_month + timedelta(days=(week - 1) * 7)
                end_date = start_date + timedelta(days=6)
                project_count = Project.objects.filter(
                    start_date__gte=start_date, start_date__lte=end_date
                ).count()
                key = f"{first_day_of_month.strftime('%B')}_week_{week}"
                weekly_project_counts[key] = project_count
        return Response(weekly_project_counts)