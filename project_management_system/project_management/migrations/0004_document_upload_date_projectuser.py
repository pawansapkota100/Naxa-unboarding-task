# Generated by Django 4.1 on 2023-11-07 08:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_management', '0003_remove_profile_id_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='upload_date',
            field=models.DateField(null=True),
        ),
        migrations.CreateModel(
            name='Projectuser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_management.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
