from django.contrib import admin
from project_management.models import *
from import_export.admin import ExportActionMixin
# Register your models here.


class ProjectDetails(ExportActionMixin,admin.ModelAdmin):
    list_display=["name","department","user","start_date"]
    list_filter=["start_date"]
admin.site.register(Project, ProjectDetails)

class DepartmentDetails(admin.ModelAdmin):
    list_display=['name']
admin.site.register(Department,DepartmentDetails)

class DocumentDetails(admin.ModelAdmin):
    list_filter = ["name"]
admin.site.register(Document, DocumentDetails)

class ProfileDetails(admin.ModelAdmin):
    list_display= ['user','username','address','country','phone']
admin.site.register(Profile,ProfileDetails )
