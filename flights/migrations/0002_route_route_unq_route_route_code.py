# Generated by Django 5.0.4 on 2024-05-01 00:11

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('destination_city_image_url', models.URLField(blank=True, default='', max_length=500)),
                ('route_code', models.CharField(max_length=100)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='flights.currency')),
                ('destination_city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='destination_city_routes', to='flights.city')),
                ('destination_country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='destination_country_routes', to='flights.country')),
                ('destination_station', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='destination_stating_routes', to='flights.station')),
                ('origin_city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='origin_city_routes', to='flights.city')),
                ('origin_country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='origin_country_routes', to='flights.country')),
                ('origin_station', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='origin_stating_routes', to='flights.station')),
            ],
            options={
                'ordering': ['created_at'],
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='route',
            constraint=models.UniqueConstraint(fields=('route_code',), name='unq_route_route_code'),
        ),
    ]
