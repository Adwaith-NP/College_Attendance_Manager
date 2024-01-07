# Generated by Django 4.2.4 on 2024-01-07 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("co_admin", "0006_alter_semester_access_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="subject",
            name="semester_code",
            field=models.ForeignKey(
                default="3A",
                on_delete=django.db.models.deletion.CASCADE,
                to="co_admin.semester",
                to_field="access_code",
            ),
        ),
    ]
