# Generated by Django 4.2.7 on 2023-11-30 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0006_systemsummary'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Canceled', 'Canceled'), ('Completed', 'Completed'), ('On Hold', 'On Hold')], default='Active', max_length=10),
        ),
    ]
