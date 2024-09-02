# Generated by Django 5.0.7 on 2024-08-21 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("User", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="tuktukRequest",
            fields=[
                (
                    "requestID",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("userID", models.CharField(max_length=50)),
                ("destination", models.CharField(max_length=60)),
                ("requestDate", models.DateField()),
                ("requestTime", models.TimeField()),
                ("VehicleRegNo", models.CharField(max_length=50)),
                ("userLat", models.FloatField()),
                ("userLon", models.FloatField()),
                ("driverID", models.CharField(max_length=50)),
                ("distance", models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
