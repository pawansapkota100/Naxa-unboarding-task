from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    home_address= models.PointField(null=True)

class ProjectSite(models.Model):
    site_coordinates= models.PointField(default=None)
    site_area= models.PolygonField(default=None)
    way_to_home= models.LineStringField(default=None)
    creator= models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=None)


class Departmentmanager(models.Manager):
    def get_it(self):
        return self.filter(name="IT")
    def get_hr(self):
        return self. filter(name="HR")


class Department(models.Model):
    name= models.CharField( max_length=50)
    department_object=Departmentmanager()

    def __str__(self):
        return self.name

class Project(models.Model):
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    department= models.ForeignKey(Department, on_delete=models.CASCADE)
    name= models.CharField( max_length=50)
    start_date= models.DateField( auto_now=False, auto_now_add=False)
    def __str__(self):
        return self.name

class Projectuser(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Use CustomUser instead of User

class Document(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)  # Use CustomUser instead of User
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to="document/")
    upload_date = models.DateField(auto_now=False, auto_now_add=False, null=True)        

    def __str__(self):
        return self.name

class Profile(models.Model):
    user= models.OneToOneField(CustomUser,on_delete=models.CASCADE, default=None,primary_key=True)
    address=models.CharField( max_length=50, null=True)
    username= models.CharField( max_length=50, null=True)
    phone= models.CharField(max_length=10, null= True)
    country= models.CharField( max_length=50, null=True)



# class ProjectSite(geomodels.Model):
#     project = geomodels.ForeignKey(
#         Project, on_delete=models.CASCADE, related_name="sites"
#     )
#     site = geomodels.CharField(max_length=100)
#     coordinate = geomodels.PointField(blank=True, null=True)
#     area = geomodels.PolygonField(blank=True, null=True)
#     way = geomodels.LineStringField(blank=True, null=True)
#     created_at = geomodels.DateTimeField(auto_now_add=True)
#     updated_at = geomodels.DateTimeField(auto_now=True)
