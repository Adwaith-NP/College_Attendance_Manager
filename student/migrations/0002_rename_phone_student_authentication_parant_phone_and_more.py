# Generated by Django 4.2.4 on 2024-01-07 18:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("student", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="student_authentication",
            old_name="phone",
            new_name="Parant_phone",
        ),
        migrations.AddField(
            model_name="student_authentication",
            name="Student_phone",
            field=models.CharField(default=None, max_length=25),
        ),
    ]
