# Generated by Django 4.2.4 on 2024-01-07 09:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("co_admin", "0005_rename_code_to_access_semester_access_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="semester",
            name="access_code",
            field=models.CharField(default="None", max_length=20, unique=True),
        ),
    ]
