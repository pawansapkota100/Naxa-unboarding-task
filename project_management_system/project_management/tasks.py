from celery import shared_task
from django.utils import timezone
from .models import SystemSummary, Project, CustomUser
import traceback

@shared_task(bind=True)
def update_summary(self):
    try:
        count_project = Project.objects.all().count()
        count_user = CustomUser.objects.all().count()

        # Get or create the SystemSummary instance for the current month and year
        current_month = timezone.now().month
        current_year = timezone.now().year

        system_summary, created = SystemSummary.objects.get_or_create(
            month=current_month,
            year=current_year
        )

        # Update the attributes
        system_summary.total_project = count_project
        system_summary.total_user = count_user

        # Save the instance to the database
        system_summary.save()
        print("Finished updating SystemSummary")

    except Exception as e:
        print(f"Error updating SystemSummary: {e}")
        traceback.print_exc()


from io import StringIO
from celery import shared_task
from django.core.management import call_command
from project_management.models import *
import random
from datetime import timedelta
@shared_task
def generate_dummy_data():
    all_departments = Department.department_object.all()
    all_users = CustomUser.objects.all()
    for _ in range(100000):
        department = random.choice(all_departments)
        user = random.choice(all_users)
        # Adjust the following line based on your model fields and requirements
        Project.objects.create(
            name=f'Dummy Project {_}',
            start_date=timezone.now(),
            department= department,
            user=user,
            deadline = timezone.now() + timedelta(days=random.randint(7, 30)),
            status= 'Active'
        )

@shared_task
def update_project_status():
    projects = Project.objects.all()
    for project in projects:
        if project.deadline:
            print("dasdasdasdasdda")
            if timezone.now().timestamp() > project.deadline.timestamp():
                project.status = "On Hold"
            else:
                project.status = "Active"
            project.save()
