from django.db import models
from django.contrib.auth.models import User
# Create your models here.


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
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    department= models.ForeignKey(Department, on_delete=models.CASCADE)
    name= models.CharField( max_length=50)
    start_date= models.DateField( auto_now=False, auto_now_add=False)


    def __str__(self):
        return self.name
    
class Projectuser(models.Model):
    project= models.ForeignKey(Project,on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)


class Document(models.Model):
    project= models.ForeignKey(Project, on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE,default=False)
    name= models.CharField( max_length=50)
    file= models.FileField(upload_to="document/")
    upload_date= models.DateField(auto_now=False, auto_now_add=False, null= True)           

    def __str__(self):
        return self.name

class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE, default=None,primary_key=True)
    address=models.CharField( max_length=50, null=True)
    username= models.CharField( max_length=50, null=True)
    phone= models.CharField(max_length=10, null= True)
    country= models.CharField( max_length=50, null=True)


