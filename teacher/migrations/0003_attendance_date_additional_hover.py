# Generated by Django 4.2.4 on 2024-03-12 08:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("teacher", "0002_attendance_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendance_date",
            name="additional_hover",
            field=models.IntegerField(default=0),
        ),
    ]