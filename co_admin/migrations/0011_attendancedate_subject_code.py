# Generated by Django 4.2.4 on 2024-01-19 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("co_admin", "0010_attendancedate_teacherid"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendancedate",
            name="subject_code",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="co_admin.subject",
            ),
        ),
    ]
