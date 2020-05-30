# Generated by Django 3.0.6 on 2020-05-29 15:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, verbose_name='code')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='title')),
                ('subtitle', models.CharField(blank=True, max_length=255, null=True, verbose_name='subtitle')),
                ('term_min', models.PositiveIntegerField(default=0, verbose_name='minimun term in days (inclusive)')),
                ('term_max', models.PositiveIntegerField(default=2147483647, verbose_name='maximun term in days')),
                ('amount_min', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='minimun amount in UF')),
                ('amount_max', models.FloatField(default=1.7976931348623157e+308, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='maximun amount in UF (inclusive)')),
            ],
            options={
                'verbose_name': 'operation',
                'verbose_name_plural': 'operations',
            },
        ),
    ]
