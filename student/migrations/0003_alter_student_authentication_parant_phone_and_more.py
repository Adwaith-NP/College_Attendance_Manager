# Generated by Django 4.2.4 on 2024-01-07 18:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("student", "0002_rename_phone_student_authentication_parant_phone_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student_authentication",
            name="Parant_phone",
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="student_authentication",
            name="Student_phone",
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="student_authentication",
            name="email",
            field=models.EmailField(max_length=254, null=True),
        ),
    ]