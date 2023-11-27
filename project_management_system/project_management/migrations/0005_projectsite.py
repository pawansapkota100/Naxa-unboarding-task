# Generated by Django 4.2.7 on 2023-11-26 14:45

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0004_delete_projectsite'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_coordinates', django.contrib.gis.db.models.fields.PointField(default=None, srid=4326)),
                ('site_area', django.contrib.gis.db.models.fields.PolygonField(default=None, srid=4326)),
                ('way_to_home', django.contrib.gis.db.models.fields.LineStringField(default=None, srid=4326)),
                ('creator', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]