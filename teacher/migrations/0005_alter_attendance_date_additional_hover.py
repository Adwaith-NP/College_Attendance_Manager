# Generated by Django 4.2.4 on 2024-03-12 14:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("teacher", "0004_attendance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendance_date",
            name="additional_hover",
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
