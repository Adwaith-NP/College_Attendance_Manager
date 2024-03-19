# Generated by Django 4.2.4 on 2024-01-15 04:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("student", "0003_alter_student_authentication_parant_phone_and_more"),
        ("co_admin", "0008_alter_semester_access_code"),
    ]

    operations = [
        migrations.CreateModel(
            name="added_student_To_sub",
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
                (
                    "student_ForeignKry",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="student.student_authentication",
                        to_field="user_ID",
                    ),
                ),
                (
                    "subject_ForeignKey",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="co_admin.subject",
                    ),
                ),
            ],
        ),
    ]