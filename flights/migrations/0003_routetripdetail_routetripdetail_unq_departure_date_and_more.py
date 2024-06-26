# Generated by Django 5.0.4 on 2024-05-01 00:44

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flights", "0002_route_route_unq_route_route_code"),
    ]

    operations = [
        migrations.CreateModel(
            name="RouteTripDetail",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(blank=True, null=True)),
                ("departure_date", models.DateField()),
                ("return_date", models.DateField(blank=True, null=True)),
                (
                    "fare_type",
                    models.CharField(choices=[("economy", "Economy"), ("premium", "Premium")], max_length=20),
                ),
                ("trip_type", models.CharField(choices=[("oneway", "One-way"), ("return", "Return")], max_length=20)),
                ("destination_url", models.URLField(blank=True, default="", max_length=500)),
                ("lowest_fare", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                (
                    "route",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="trip_details", to="flights.route"
                    ),
                ),
            ],
            options={
                "ordering": ["created_at"],
                "abstract": False,
            },
        ),
        migrations.AddConstraint(
            model_name="routetripdetail",
            constraint=models.UniqueConstraint(
                fields=("route", "departure_date", "fare_type", "trip_type"), name="unq_departure_date"
            ),
        ),
        migrations.AddIndex(
            model_name="routetripdetail",
            index=models.Index(fields=["departure_date"], name="idx_departure_date"),
        ),
    ]
