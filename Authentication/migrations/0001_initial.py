# Generated by Django 4.2.4 on 2024-01-05 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="admin_Authentication",
            fields=[
                ("Name", models.CharField(max_length=31)),
                ("email", models.EmailField(default=None, max_length=254)),
                (
                    "user_ID",
                    models.CharField(
                        max_length=31, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("password", models.CharField(max_length=1001)),
                ("course", models.CharField(default=None, max_length=50, null=True)),
                ("admin", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="teacher_Authentication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Name", models.CharField(max_length=30)),
                ("email", models.EmailField(default=None, max_length=254)),
                ("user_ID", models.CharField(max_length=30, unique=True)),
                ("password", models.CharField(max_length=1000)),
                (
                    "co_admin",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Authentication.admin_authentication",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="student_Authentication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Name", models.CharField(max_length=30)),
                ("phone", models.CharField(default=None, max_length=25)),
                ("email", models.EmailField(default=None, max_length=254)),
                ("user_ID", models.CharField(max_length=30, unique=True)),
                ("password", models.CharField(max_length=1000)),
                (
                    "co_admin",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Authentication.admin_authentication",
                    ),
                ),
            ],
        ),
    ]
