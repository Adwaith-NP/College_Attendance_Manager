# Generated by Django 4.2.4 on 2024-01-16 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Authentication", "0002_delete_student_authentication"),
        ("co_admin", "0009_attendancedate"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendancedate",
            name="teacherID",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="Authentication.teacher_authentication",
                to_field="user_ID",
            ),
        ),
    ]
